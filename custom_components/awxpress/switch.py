"""
Switch platform to launch AWX job templates."""
import logging
import time
import requests

from homeassistant.components.switch import SwitchEntity
from homeassistant.components.persistent_notification import create as create_notification
from .const import DOMAIN, CONF_TOWER_URL, CONF_TOKEN, CONF_VERIFY_SSL

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    """
    Set up one switch per AWX Job Template.
    coordinator.data is { template_id: template_name_string }.
    """
    coordinator = hass.data[DOMAIN][entry.entry_id]
    templates = coordinator.data or {}
    switches = [
        AWXTemplateSwitch(hass, entry, tpl_id, tpl_name)
        for tpl_id, tpl_name in templates.items()
    ]
    async_add_entities(switches, True)


class AWXTemplateSwitch(SwitchEntity):
    """
    Represents an AWX Job Template as a switch in Home Assistant.
    Turning it on will POST /api/v2/job_templates/{id}/launch/,
    then poll /api/v2/jobs/{job_id}/ until completion.
    """

    def __init__(self, hass, entry, template_id: int, template_name: str):
        self.hass = hass
        self.entry = entry
        self.template_id = template_id
        self.template_name = template_name
        self._is_on = False
        self._job_id = None

    @property
    def unique_id(self) -> str:
        return f"{DOMAIN}_{self.template_id}"

    @property
    def name(self) -> str:
        safe = self.template_name.replace(" ", "_").lower()
        return f"awx_{self.template_id}_{safe}"

    @property
    def is_on(self) -> bool:
        return self._is_on

    async def async_turn_on(self, **kwargs):
        """Launch the template and wait in a background thread."""
        _LOGGER.debug("Launching AWX template %s (%s)", self.template_id, self.template_name)
        self._is_on = True

        def _launch_and_wait():
            cfg = self.entry.data
            base = cfg[CONF_TOWER_URL].rstrip("/")
            token = cfg[CONF_TOKEN]
            verify = cfg.get(CONF_VERIFY_SSL, True)

            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json",
            }

            # 1) Launch the job
            url = f"{base}/api/v2/job_templates/{self.template_id}/launch/"
            r = requests.post(url, headers=headers, verify=verify)
            r.raise_for_status()
            job_id = r.json().get("job")
            if not job_id:
                raise RuntimeError("AWX did not return job ID on launch")

            # 2) Poll until terminal state
            job_url = f"{base}/api/v2/jobs/{job_id}/"
            while True:
                jr = requests.get(job_url, headers=headers, verify=verify)
                jr.raise_for_status()
                status = jr.json().get("status")
                if status in ("successful", "failed", "error", "canceled"):
                    return jr.json()
                time.sleep(2)

        # Run HTTP + polling off the event loop
        job_result = await self.hass.async_add_executor_job(_launch_and_wait)

        # Once done:
        self._is_on = False
        self._job_id = job_result.get("id", job_result.get("job"))
        status = job_result.get("status")
        msg = f"AWX job {self._job_id} completed with status {status}"
        _LOGGER.info(msg)

        # Persist notification in HA UI
        create_notification(
            self.hass,
            title="AWXpress",
            message=msg,
            notification_id=f"{DOMAIN}_{self._job_id}",
        )

        # Update the status sensor attributes
        sensor = f"sensor.awx_{DOMAIN}_status"
        st = self.hass.states.get(sensor)
        if st:
            attrs = dict(st.attributes)
            attrs.update({
                "last_job_id": self._job_id,
                "last_job_status": status,
            })
            self.hass.states.async_set(sensor, st.state, attrs)

    async def async_update(self):
        """No periodic updates for these switches."""
        pass