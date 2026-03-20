import os
import json

BASE_DIR = os.path.dirname(__file__)  # resolves to backend/

def load_jsons(filename):
    with open(os.path.join(BASE_DIR, f"jsons/{filename}.json")) as f:
        data = json.load(f)
        return data