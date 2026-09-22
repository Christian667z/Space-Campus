import json
from pathlib import Path

CONFIG_FILE = Path("config/settings.json")

def load_settings():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"theme": "dark", "language": "fr", "zoom": 100}

def save_settings(settings):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4)
