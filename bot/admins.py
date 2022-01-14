import os
from typing import List

from loguru import logger


admins_str: str = os.getenv("ADMINS", "")
logger.info(f"admin ids: {admins_str}")
ADMINS: List[int] = list(map(int, admins_str.split(" ")))
