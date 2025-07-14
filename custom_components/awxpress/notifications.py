"""
Helper for notifications and weekly log cleanup."""
import logging
from datetime import timedelta
from homeassistant.helpers.event import async_track_time_interval
from .const import LOG_ROTATION_DAYS

_LOGGER = logging.getLogger(__name__)

def setup_log_rotation(hass):
    """Schedule weekly log cleanup."""
    interval = timedelta(days=LOG_ROTATION_DAYS)
    async_track_time_interval(hass, _cleanup_logs, interval)

async def _cleanup_logs(now):
    _LOGGER.info(f"AWXpress weekly log cleanup at {now}")