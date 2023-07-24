import json
from typing import Dict

from bot.config import settings

text_path = settings.APP_DIR / "data" / "text.json"
with text_path.open() as fp:
    text: Dict[str, str] = json.load(fp)
