import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


class SetLogs:
    """
    Rotate Log By File Size
    """

    def __init__(self, name=None, size=20 * 1024 * 1024, backup=3):
        """
        :param name: log name
        :param size: rotate size default: 20M
        :param backup: backup nums default: 3
        """
        log_path = Path(__file__).parents[2] / 'logs'
        if not log_path.exists():
            log_path.mkdir()
        if name is None:
            self.path = log_path / 'defaults.log'
        else:
            self.path = log_path / name
        self.size = size
        self.backup = backup

    def set_rotate(self, name=__name__, stream=None):
        """
        :param name: set logger name
        :param stream: open StreamHandler default: not open
        :return: logger
        """
        # createLogger
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        # createHandler
        file_handler = RotatingFileHandler(filename=self.path,
                                           maxBytes=self.size,
                                           backupCount=self.backup,
                                           encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        # createFormatter & bindLogger
        fmt = '%(asctime)s %(name)s %(threadName)s %(filename)s[%(lineno)d]: ' \
              '%(levelname)s %(funcName)s %(message)s'
        formatter = logging.Formatter(fmt, datefmt='%F %T')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        # StreamTest
        if stream is not None:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(formatter)
            logger.addHandler(stream_handler)

        return logger


if __name__ == '__main__':
    # StreamTest
    logger = SetLogs().set_rotate(__name__, stream=True)
    logger.info('info msg')
    logger.warning('warning msg')
