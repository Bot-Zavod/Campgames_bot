import os
from typing import List


admins_str: str = os.getenv("ADMINS", "")
ADMINS: List[int] = list(map(int, admins_str.split(" ")))
