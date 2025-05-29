# duplicate_checker.py
import json
import os

def load_processed_items(log_file='bundles_log.json') -> set:
    """
    Return a set of bundle names already processed.
    If the file is empty, missing, or malformed JSON, return an empty set.
    """
    if not os.path.exists(log_file):
        return set()

    try:
        with open(log_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return set(data)
    except json.JSONDecodeError:
        print(f"[!] {log_file} is empty or invalid JSON — resetting.")
    except Exception as e:
        print(f"[!] Could not read {log_file}: {e}")

    # If we get here, treat as empty and reset file
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump([], f)
    return set()

def save_processed_item(item_name: str, log_file='bundles_log.json'):
    processed = load_processed_items(log_file)
    processed.add(item_name)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(list(processed), f, ensure_ascii=False, indent=2)
