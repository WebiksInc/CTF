import logging
import logging.handlers
import time
from flask import session
from CTFd.utils.user import get_ip, get_user_manager
# Configure the logging format

   

def log(event, message, **kwargs):
    user = get_user_manager()
    logger = logging.getLogger('ctfd')
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

    print('now logging')
    logger.info(message, extra=extra)
    

#[12/11/2024 10:45:03] 127.0.0.1 - tomer3 registered with tomerp20@gmail.com
# 2024-12-10T14:45:30.123456|INFO|setup_stage|stage_id=stage_123|user_id=user_456|resource_id=resource_789|resource_type=server|trace_id=trace_abc123