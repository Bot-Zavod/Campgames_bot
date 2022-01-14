import json
from collections import defaultdict
from typing import Dict

with open("text.json", "r") as fp:
    demo_text: Dict[str, Dict[str, str]] = json.load(fp)

    # before keys where ints, but after migrating to json theu turn strings
    # so we itarate turning them back to ints
    text: Dict[str, Dict[int, str]] = defaultdict(dict)
    for k, v in demo_text.items():
        text[k][0] = demo_text[k]["0"]
        text[k][1] = demo_text[k]["1"]
