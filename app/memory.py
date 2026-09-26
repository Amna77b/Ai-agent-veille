import json
import os

MEMORY_FILE = "app/seen_articles.json"

def load_seen() -> set:
    if not os.path.exists(MEMORY_FILE):
        return set()
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return set(json.load(f))

def save_seen(seen: set):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(list(seen), f)