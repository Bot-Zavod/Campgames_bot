import os
from typing import List

from dotenv import load_dotenv
from loguru import logger


load_dotenv()
admins_str: str = os.getenv("ADMINS", "")
logger.info(f"admin ids: {admins_str}")
ADMINS: List[int] = list(map(int, admins_str.split(" ")))
