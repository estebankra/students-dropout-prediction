import logging
from logging.handlers import TimedRotatingFileHandler

from app.config import settings

logging.basicConfig(level=logging.NOTSET)
# Create a formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Create a logger
logger = logging.getLogger()


# Custom filter to filter log records based on severity level
class SeverityFilter(logging.Filter):
    def __init__(self, severity):
        super().__init__()
        self.severity = severity

    def filter(self, record):
        return record.levelno == self.severity


def setup_logger_by_level(
    level: logging.DEBUG | logging.INFO | logging.WARNING | logging.ERROR, filename: str
):
    # Create a TimedRotatingFileHandler for each level and attach filter
    handler = TimedRotatingFileHandler(
        filename=filename, when="midnight", backupCount=7
    )
    handler.setLevel(level)
    handler.setFormatter(formatter)
    handler.addFilter(SeverityFilter(level))
    logger.addHandler(handler)


# Create a TimedRotatingFileHandler for each level and attach filter
if settings.ENVIRONMENT == "development":
    setup_logger_by_level(level=logging.DEBUG, filename="logs/debug/debug.log")

setup_logger_by_level(level=logging.INFO, filename="logs/info/info.log")
setup_logger_by_level(level=logging.WARNING, filename="logs/warning/warning.log")
setup_logger_by_level(level=logging.ERROR, filename="logs/error/error.log")
