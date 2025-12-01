# memory.py - simple file-backed memory for user profiles and past trips
import json, os
PATH = os.path.join(os.path.dirname(__file__), '..', 'memory_store.json')

def _load():
    try:
        with open(PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}

def _save(data):
    with open(PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_user(user_id='default'):
    mem = _load()
    return mem.get(user_id, {})

def update_user(user_id, data):
    mem = _load()
    mem[user_id] = data
    _save(mem)
