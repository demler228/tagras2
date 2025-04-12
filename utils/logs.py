import sys

from loguru import logger

from utils.constants import adminlogpath, userlogpath, programlogpath


def make_filter(name):
    def filter(record):
        return record["extra"].get("name") == name
    return filter
logger.add(
    adminlogpath,
    format="{time} - {level} - {message}",
    level="DEBUG",
    filter=make_filter("admin"),
    rotation="1500 MB",
    retention="7 days",
    enqueue=True
)

logger.add(
    userlogpath,
    format="{time} - {level} - {message}",
    level="INFO",
    filter=make_filter("user"),
    rotation="1500 MB",
    retention="7 days",
    enqueue=True
)

logger.add(
    programlogpath,
    format="{time} - {level} - {message}",
    level="INFO",
    filter=make_filter("program"),
    rotation="500 MB",
    retention="1 days",
    enqueue=True
)
#logger.add(sys.stderr)

user_logger = logger.bind(name="user")
program_logger = logger.bind(name="program")
admin_logger = logger.bind(name="admin")

program_logger.info('test')