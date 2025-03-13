import psycopg2
from loguru import logger
from psycopg2 import Error

from .config import settings


def connection_db():
    dbname = settings.DB_NAME
    user = settings.USER
    password = settings.PASSWORD
    host = settings.HOST_NAME
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        return conn
    except Exception as e:
        logger.error(e)
        return None