import logging
import logging.handlers
from CTFd.utils.user import get_ip, get_user_manager

# Configure the logging format


def log(logger, event, message, **kwargs):
    user = get_user_manager()
    logger = logging.getLogger(logger)

    log_levels = {
            "DEBUG": logging.DEBUG,
            "INFO": logging.INFO,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL
    }
    #if kwargs contains a log level, use it, otherwise default to INFO
    level = log_levels.get(kwargs.pop("level", "INFO"), logging.INFO)

    extra_data = {
        "ip": get_ip(),
        **kwargs
    }
    if user:
        if hasattr(user, 'active_c'):
            extra_data['stage_id'] = user.active_c
        if hasattr(user, 'id'):
            extra_data['user_id'] = user.id

    extra = {
        "extra_data": extra_data,
        "trace_id": 123123,
        "event": event,

    }

    logger.log(level, message, extra=extra)

