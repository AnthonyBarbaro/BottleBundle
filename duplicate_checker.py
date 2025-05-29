# duplicate_checker.py

import json
import os

def load_processed_items(log_file='processed_log.json') -> set:
    """
    Loads a JSON list from log_file and returns a set of item names.
    """
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return set(data)
    return set()

def save_processed_item(item_name: str, log_file='processed_log.json'):
    """
    Adds a single item_name to the log_file to mark it as processed.
    """
    processed = load_processed_items(log_file)
    processed.add(item_name)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(list(processed), f, ensure_ascii=False, indent=2)
