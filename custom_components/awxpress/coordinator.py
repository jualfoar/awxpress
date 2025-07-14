"""
DataUpdateCoordinator for AWXpress with cron scheduling.
"""
import logging
from datetime import datetime
from typing import Any, Dict

from croniter import croniter

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator,
    UpdateFailed,
)

from awxkit.api.client import Connection
from awxkit.api.pages.api import ApiV2

from .const import (
    DOMAIN,
    CONF_TOWER_URL,
    CONF_TOKEN,
    CONF_VERIFY_SSL,
    CONF_POLL_SCHEDULE,
)

_LOGGER = logging.getLogger(__name__)


class AWXCoordinator(DataUpdateCoordinator[Dict[int, Any]]):
    """Coordinator to poll AWX Tower for job templates on a cron schedule."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the AWX Coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_coordinator",
            update_interval=None,  # manual cron scheduling
            update_method=self._async_update_data,
        )

        self.hass = hass
        self.entry = entry
        config = entry.data

        # 1) Build the Connection (server + SSL) and inject the Bearer token
        conn = Connection(
            config[CONF_TOWER_URL],
            verify=config.get(CONF_VERIFY_SSL, True),
        )
        conn.session.headers.update({"Authorization": f"Bearer {config[CONF_TOKEN]}"})

        # 2) Use ApiV2 to talk to /api/v2/
        self.client = ApiV2(conn)

        # Cron schedule string, e.g. "0 * * * *"
        self.cron_schedule = config.get(CONF_POLL_SCHEDULE)

        # Handle to the scheduled timer
        self._timer = None

        # Kick off the initial fetch and schedule recurring runs
        hass.async_create_task(self.async_refresh())
        self._schedule_next_refresh()

    async def _async_update_data(self) -> Dict[int, Any]:
        """
        Fetch data from AWX in the executor pool.

        Returns a dict mapping template ID to the AWXKit template resource.
        """
        try:
            return await self.hass.async_add_executor_job(self._get_templates)
        except Exception as err:
            _LOGGER.error("Error fetching AWX templates: %s", err)
            raise UpdateFailed(err) from err

    def _get_templates(self) -> Dict[int, str]:
        """
        Blocking call to AWX API to retrieve all job templates.

        Returns:
            dict mapping template ID to template name (string).
        """
        # 1) Fetch the /api/v2/ root
        root = self.client.get()
        # 2) Retrieve **all** pages of job_templates
        page = root.job_templates.get(all_pages=True)
        # 3) Build our map of ID → name (string)
        templates = {tmpl.id: tmpl.name for tmpl in page.results}
        _LOGGER.debug("Fetched %d AWX template names", len(templates))
        return templates

    def _schedule_next_refresh(self) -> None:
        """Calculate next cron trigger and schedule a refresh."""
        try:
            now = datetime.now()
            itr = croniter(self.cron_schedule, now)
            next_run = itr.get_next(datetime)
            delay = (next_run - now).total_seconds()
            _LOGGER.debug(
                "Scheduling next AWX refresh at %s (in %.0f sec)",
                next_run,
                delay,
            )
            if self._timer:
                self._timer.cancel()
            self._timer = self.hass.loop.call_later(delay, self._on_timer)
        except Exception as err:
            _LOGGER.error("Failed to schedule AWX refresh: %s", err)

    def _on_timer(self) -> None:
        """Cron timer callback: trigger refresh then reschedule."""
        _LOGGER.debug("AWX cron timer fired, refreshing now")
        self.hass.async_create_task(self.async_refresh())
        self._schedule_next_refresh()

    async def schedule_poll(self) -> None:
        """Public method to (re)start the cron schedule."""
        self._schedule_next_refresh()

    def cancel_poll(self) -> None:
        """Cancel the scheduled cron timer, if any."""
        if self._timer:
            self._timer.cancel()
            self._timer = None