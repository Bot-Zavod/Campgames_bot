from pathlib import Path

from loguru import logger
from pydantic import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    # sum of all rates must be less than 30
    ADMINS: str
    GAMES_TABLE_KEY: str

    LOG_CHANNEL: str

    TIME_ZONE: str = "Europe/Kiev"

    APP_DIR: Path = Path(__file__).parent.parent

    class Config:
        # load avaliable vars
        env_file = ".env"
        case_sensitive = True


settings = Settings()  # type: ignore
logger.debug("Enviroment variables loaded to config")
