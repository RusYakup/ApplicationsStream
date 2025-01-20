from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
import logging

log = logging.getLogger(__name__)


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    LOG_LEVEL: str = "INFO"
    KAFKA_BOOTSTRAP_SERVERS: str
    HOST_CONSUMER: str

    model_config = SettingsConfigDict(env_file="../.env")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"



@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


def logging_config(log_level: str) -> None:
    """
    A function that configures logging based on the input log level.

    :param log_level: The log level to set for the logging configuration.
    :return: None
    """
    numeric_level = getattr(logging, log_level.upper())
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    log.info("Logging Configured")