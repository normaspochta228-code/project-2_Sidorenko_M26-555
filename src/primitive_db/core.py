VALID_TYPES = {"int", "str", "bool"}

def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict | None:
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    parsed_columns = []
    parsed_columns.append({'name': 'ID', 'type': 'int'})

    for col in columns:
        if ":" not in col:
            print(f'Ошибка: Неверный формат колонки "{col}". Используйте формат name:type')
            return None
        
        col_name, col_type = col.split(":")
        col_name = col_name.strip()
        col_type = col_type.strip().lower()

        if col_type not in VALID_TYPES:
            print(f'Ошибка: Неподдерживаемый тип данных "{col_type}" для колонки "{col_name}". Разрешены только: {VALID_TYPES}')
            return None
        
        if col_name.lower() == "id":
            continue

        parsed_columns.append({"name": col_name, "type": col_type})

    metadata[table_name] = {
        "columns": parsed_columns,
        "data": []  
    }
    
    print(f'Таблица "{table_name}" успешно создана со столбцами: {', '.join(columns)}')
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict | None:
    try:
        metadata.pop(table_name)
        print(f'Таблица "{table_name}" успешно удалена.')
        return metadata
    except KeyError:
        print(f'Ошибка: Таблицы "{table_name}" не существует.')
        return None
    
    
