"""
The AWXpress integration.
"""
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN
from .coordinator import AWXCoordinator
from .notifications import setup_log_rotation

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up AWXpress from a config entry."""
    _LOGGER.debug("Setting up AWXpress entry: %s", entry.data)
    hass.data.setdefault(DOMAIN, {})

    # Initialize coordinator
    coordinator = AWXCoordinator(hass, entry)
    await coordinator.async_refresh()
    await coordinator.schedule_poll()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Start weekly log rotation
    setup_log_rotation(hass)

    # Forward setup to sensor and switch platforms
    await hass.config_entries.async_forward_entry_setups(
        entry, ["sensor", "switch"]
    )

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry and cancel polling."""
    coordinator = hass.data[DOMAIN].pop(entry.entry_id)
    coordinator.cancel_poll()
    return await hass.config_entries.async_unload_platforms(entry, ["sensor", "switch"])