# custom_components/awxpress/sensor.py

"""
Sensor platform for AWXpress status.
"""
import logging
from datetime import datetime

from croniter import croniter
from homeassistant.helpers.entity import Entity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the AWXpress status sensor."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AWXStatusSensor(hass, coordinator)], True)


class AWXStatusSensor(Entity):
    """
    Reports connectivity (connected/unavailable), template count,
    next poll time, and preserves last_job_id/status.
    """

    def __init__(self, hass, coordinator):
        self.hass = hass
        self.coordinator = coordinator
        self._state = None
        self._attr = {}

    @property
    def name(self) -> str:
        return f"awx_{DOMAIN}_status"

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_status"

    @property
    def state(self) -> str:
        return self._state

    @property
    def extra_state_attributes(self) -> dict:
        return self._attr

    async def async_update(self):
        """
        Poll AWX templates.  
        State: "connected" on success, "unavailable" on failure.  
        Attributes: templates_count, next_poll, last_job_id, last_job_status.
        """
        now = datetime.now()
        # attempt to refresh
        try:
            await self.coordinator.async_request_refresh()
            self._state = "connected"
            templates = self.coordinator.data or {}
        except Exception as err:
            _LOGGER.error("AWXpress fetch failed: %s", err)
            self._state = "unavailable"
            templates = {}

        # compute next poll
        itr = croniter(self.coordinator.cron_schedule, now)
        next_run = itr.get_next(datetime)

        # preserve last job info from HA state
        entity_id = self.entity_id or f"sensor.{self.name}"
        old = self.hass.states.get(entity_id)
        old_attrs = dict(old.attributes) if old else {}

        # build attributes (no more last_update)
        self._attr = {
            "templates_count": len(templates),
            "next_poll": next_run.isoformat(timespec="seconds"),
            "last_job_id": old_attrs.get("last_job_id", "Unknown"),
            "last_job_status": old_attrs.get("last_job_status", "Unknown"),
        }
        _LOGGER.debug(
            "AWXStatusSensor updated: state=%s, attrs=%s",
            self._state,
            self._attr,
        )
