import json


DB_META_JSON = "db_meta.json"



def load_metadata(filepath: str = DB_META_JSON) -> list | dict:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: list | dict) -> None:
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
