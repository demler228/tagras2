from loguru import logger
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from .config import settings
from sqlalchemy import create_engine, String

def connection_db():
    dbname = settings.DB_NAME
    user = settings.USER
    password = settings.PASSWORD
    host = settings.HOST_NAME
    port = settings.PORT_NAME
    try:
        # for creating connection string
        connection_str = f'postgresql://{user}:{password}@{host}:{port}/{dbname}'
        # SQLAlchemy engine
        engine = create_engine(connection_str)
        # you can test if the connection is made or not
        Session = sessionmaker(engine)
        return Session
    except Exception as ex:
        logger.error(f'Sorry failed to connect: {ex}')
        return None

