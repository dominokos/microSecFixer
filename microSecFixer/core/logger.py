"""Logger implemented here. Other methods call this one when writing messages to log to have a single logger."""

from logging.handlers import RotatingFileHandler
import os
import logging
from datetime import date, datetime


log_formatter = logging.Formatter("%(asctime)s %(levelname)-8s %(message)s",
                                  datefmt="%Y-%m-%d %H:%M:%S")  # your logging format
LOG_PATH = "./output/logs/"
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
file_name = LOG_PATH + "microSecFixer.log"

log_handler = RotatingFileHandler(file_name, mode="a", maxBytes=1024, backupCount=10, encoding="utf-8")
log_handler.setFormatter(log_formatter)
#file = "./output/logs/test.log"
logger = logging.getLogger("tool")
logger.addHandler(log_handler)
logger.setLevel(logging.DEBUG) 

# Set log levels of all imported modules to ERROR
logging.getLogger("github").setLevel(logging.ERROR)
logging.getLogger("requests").setLevel(logging.ERROR)
logging.getLogger("urllib.request").setLevel(logging.ERROR)
logging.getLogger("os").setLevel(logging.ERROR)
logging.getLogger("json").setLevel(logging.ERROR)
logging.getLogger("yaml").setLevel(logging.ERROR)
logging.getLogger("io").setLevel(logging.ERROR)
logging.getLogger("Github").setLevel(logging.ERROR)


def write_log_message(message: str, level: str) -> None:
    """
    Writes passed message as passed level to log file
    """
    
    level = str(level)
    message = str(message)
    eval("logger." + level + "(message)")