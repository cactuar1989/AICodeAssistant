import os
import json


CONFIG_FILE = 'config.json'

def save_api_key(api_key):
    with open(CONFIG_FILE, 'w') as f:
        json.dump({'OPENAI_API_KEY': api_key}, f)

def load_api_key():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            data = json.load(f)
            return data.get('OPENAI_API_KEY')
    return None