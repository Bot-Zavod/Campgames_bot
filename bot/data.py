import json
from collections import defaultdict
from typing import Dict

from bot.config import settings

text_path = settings.APP_DIR / "data" / "text.json"

with text_path.open() as fp:
    demo_text: Dict[str, Dict[str, str]] = json.load(fp)

    # before keys where ints, but after migrating to json theu turn strings
    # so we itarate turning them back to ints
    text: Dict[str, Dict[int, str]] = defaultdict(dict)
    for k, v in demo_text.items():
        text[k][0] = demo_text[k]["0"]
        text[k][1] = demo_text[k]["1"]
