"""
Constants for the AWXpress integration.
"""
DOMAIN = "awxpress"

# Configuration keys
CONF_TOWER_URL = "tower_url"
CONF_TOKEN = "token"
CONF_VERIFY_SSL = "verify_ssl"
CONF_POLL_SCHEDULE = "poll_schedule"
CONF_DEBUG_LEVEL = "debug_level"

# Defaults
DEFAULT_VERIFY_SSL = True
DEFAULT_POLL_SCHEDULE = "0 * * * *"
DEFAULT_DEBUG_LEVEL = "INFO"

# Notifications
NOTIFY_JOB_COMPLETE = "awxpress_job_complete"

# Log rotation interval (days)
LOG_ROTATION_DAYS = 7