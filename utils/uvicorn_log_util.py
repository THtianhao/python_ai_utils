import logging
import os
from datetime import datetime
from typing import Any
# 设置报警日志
# error_in_file(app, log_uv,url)
# 使用方法
# uvicorn.run(app,
#             host="0.0.0.0",
#             port=10090,
#             log_level="debug",
#             access_log=True,
#             log_config=get_uvicorn_log_config(os.path.join(root_path, "logs")), )
def get_uvicorn_log_config(base_log_dir):
    log_dirs = {
        'debug': os.path.join(base_log_dir, 'debug'),
        'info': os.path.join(base_log_dir, 'info'),
        'warning': os.path.join(base_log_dir, 'warning'),
        'error': os.path.join(base_log_dir, 'error')
    }
    # 创建日志目录
    for dir_path in log_dirs.values():
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
    current_date = datetime.now().strftime('%Y-%m-%d')
    info_log_path = os.path.join(base_log_dir, 'info')
    file_info_name = os.path.join(info_log_path, f'{current_date}.log')
    error_log_path = os.path.join(base_log_dir, 'error')
    file_error_name = os.path.join(error_log_path, f'{current_date}.log')
    LOGGING_CONFIG: dict[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "uvicorn.logging.DefaultFormatter",
                "fmt": "%(levelprefix)s %(message)s",
                "use_colors": None,
            },
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s',  # noqa: E501
            },
            "custom": {
                "()": "logging.Formatter",
                'fmt': "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            },
            "time": {
                "()": "logging.Formatter",
                'fmt': "%(asctime)s : %(message)s"
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stderr",
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
            },
            "file_info": {
                "formatter": "time",
                "level": "INFO",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": file_info_name,
                "when": "midnight",
                "interval": 1,
                "backupCount": 7
            },
            "file_error": {
                "formatter": "time",
                "level": "ERROR",
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": file_error_name,
                "when": "midnight",
                "interval": 1,
                "backupCount": 7
            },
        },
        "loggers": {
            # 全局配置，error和access都会生效
            "uvicorn": {"handlers": ["default"], "level": "INFO", "propagate": False},
            "uvicorn.error": {"handlers": ["file_error"], "level": "ERROR"},
            # 普通日志生效 只适用于 uvicorn自身，因为对adder进行format等操作
            "uvicorn.access": {"handlers": ["access", "file_info"], "level": "INFO", "propagate": False},
            "uvicorn.custom": {"handlers": ["default", "file_info"], "level": "INFO", "propagate": False},
        },
    }
    return LOGGING_CONFIG

log_uve = logging.getLogger('uvicorn.error')
log_uv = logging.getLogger('uvicorn.custom')
