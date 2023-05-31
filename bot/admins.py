from typing import List

from loguru import logger

from bot.config import settings


admins_str: str = settings.ADMINS
ADMINS: List[int] = list(map(int, admins_str.split(" ")))
logger.info(f"admin ids: {ADMINS}")
