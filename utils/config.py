from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN : str
    DB_NAME : str
    USER : str
    IMAGES_PATH: str
    PASSWORD : str
    PORT_NAME: str
    HOST_NAME : str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
