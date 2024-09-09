import logging
import logging.handlers
import os
from datetime import datetime

class LogUtil:
    def __init__(self, log_dir='logs'):
        self.logger = self._setup_logger(log_dir)

    def _setup_logger(self, base_log_dir):

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

        # 获取当前日期
        current_date = datetime.now().strftime('%Y-%m-%d')

        # 配置日志记录器
        logger = logging.getLogger('UtilsLogger')
        logger.setLevel(logging.DEBUG)

        levels = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warning': logging.WARNING,
            'error': logging.ERROR
        }
        # 创建日志处理器，按日期拆分日志文件
        for level_name, level_value in levels.items():
            handler = logging.handlers.TimedRotatingFileHandler(
                filename=os.path.join(log_dirs[level_name], f'{current_date}.log'),
                when='midnight',
                interval=1,
                backupCount=7
            )
            handler.suffix = "%Y-%m-%d"
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            handler.setLevel(level_value)
            logger.addHandler(handler)
        return logger
    def d(self, message):
        self.logger.debug(message)

    def i(self, message):
        self.logger.info(message)

    def w(self, message):
        self.logger.warning(message)

    def e(self, message):
        self.logger.error(message)

log_util = LogUtil()
