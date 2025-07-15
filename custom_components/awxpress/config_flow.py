"""
Config flow for AWXpress integration.
"""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from .const import (
    DOMAIN,
    CONF_TOWER_URL,
    CONF_TOKEN,
    CONF_VERIFY_SSL,
    CONF_POLL_SCHEDULE,
    CONF_DEBUG_LEVEL,
    DEFAULT_VERIFY_SSL,
    DEFAULT_POLL_SCHEDULE,
    DEFAULT_DEBUG_LEVEL,
)

class AWXConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AWXpress."""

    VERSION = 1


    async def async_step_user(self, user_input=None):
        """
        Handle the initial step when the user adds the integration via the UI.
        Presents a form to collect AWX connection info and options.
        """
        if user_input is None:
            schema = vol.Schema({
                vol.Required(CONF_TOWER_URL): str,
                vol.Required(CONF_TOKEN): str,
                vol.Optional(CONF_VERIFY_SSL, default=DEFAULT_VERIFY_SSL): bool,
                vol.Optional(CONF_POLL_SCHEDULE, default=DEFAULT_POLL_SCHEDULE): str,
                vol.Optional(
                    CONF_DEBUG_LEVEL,
                    default=DEFAULT_DEBUG_LEVEL
                ): vol.In(["DEBUG", "INFO", "WARNING", "ERROR"]),
            })
            return self.async_show_form(
                step_id="user",
                data_schema=schema,
            )

        # User has submitted the form; create the entry
        return self.async_create_entry(
            title=user_input[CONF_TOWER_URL],
            data=user_input,
        )