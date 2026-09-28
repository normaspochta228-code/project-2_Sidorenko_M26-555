import os

from primitive_db.utils import DATA_DIR

VALID_TYPES = {'int', 'str', 'bool'}

def create_table(metadata: dict, table_name: str, columns: list[str]) -> dict | None:
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return None

    parsed_columns = []
    parsed_columns.append({'name': 'ID', 'type': 'int'})

    for col in columns:
        if ':' not in col:
            print(f'Ошибка: Неверный формат колонки "{col}". Используйте формат name:type')
            return None
        
        col_name, col_type = col.split(':')
        col_name = col_name.strip()
        col_type = col_type.strip().lower()

        if col_type not in VALID_TYPES:
            print(f'Ошибка: Неподдерживаемый тип данных "{col_type}" для колонки "{col_name}". Разрешены только: {VALID_TYPES}')
            return None
        
        if col_name.lower() == 'id':
            continue

        parsed_columns.append({'name': col_name, 'type': col_type})

    metadata[table_name] = {
        'columns': parsed_columns,
    }

    
    print(f'Таблица "{table_name}" успешно создана со столбцами: {', '.join(columns)}')
    return metadata


def drop_table(metadata: dict, table_name: str) -> dict | None:
    try:
        metadata.pop(table_name)
        os.remove(os.path.join(DATA_DIR, f'{table_name}.json'))
        print(f'Таблица "{table_name}" успешно удалена.')
        return metadata
    except (KeyError, FileNotFoundError):
        print(f'Ошибка: Таблицы "{table_name}" не существует.')
        return None



def insert(metadata: dict, table_name: str, table_data: list, values: list[str]) -> list | None:
    if table_name not in metadata:
        print(f'Ошибка: Таблицы "{table_name}" не существует.')
        return None

    columns = metadata[table_name]['columns']

    expected_cols = columns[1:]

    if len(values) != len(expected_cols):
        print(f'Ошибка: Неверное количество значений. Ожидается: {len(expected_cols)}, передано: {len(values)}.')
        return None

    new_row = {}
    
    if table_data:
        new_id = max(row['ID'] for row in table_data) + 1
    else:
        new_id = 1
    new_row['ID'] = new_id

    # Валидация и приведение типов
    for col, val_str in zip(expected_cols, values):
        col_name = col['name']
        col_type = col['type']
        
        # Убираем лишние кавычки
        val_cleaned = val_str.strip("'\"")

        try:
            if col_type == 'int':
                new_row[col_name] = int(val_cleaned)

            elif col_type == 'bool':
                if val_cleaned.lower() in ('true', '1'):
                    new_row[col_name] = True

                elif val_cleaned.lower() in ('false', '0'):
                    new_row[col_name] = False
                else:
                    raise ValueError

            elif col_type == 'str':
                new_row[col_name] = str(val_cleaned)

            else: 
                raise ValueError

        except ValueError:
            print(f'Ошибка: Значение "{val_str}" не соответствует типу "{col_type}" для колонки "{col_name}".')
            return None

    table_data.append(new_row)
    print('Запись успешно добавлена.')
    return table_data

def select(table_data: list, where_clause: dict | None = None) -> list:
    if not where_clause:
        return table_data

    filtered_data = []
    for row in table_data:
        match = True
        for key, value in where_clause.items():
            if row.get(key) != value:
                match = False
                break
        if match:
            filtered_data.append(row)
    return filtered_data

def update(table_data: list, set_clause: dict, where_clause: dict | None = None) -> list:
    updated_count = 0
    for row in table_data:
        match = True
        if where_clause:
            for key, value in where_clause.items():
                if row.get(key) != value:
                    match = False
                    break
        
        if match:
            for key, value in set_clause.items():
                if key in row:
                    row[key] = value
            updated_count += 1
            
    print(f'Обновлено записей: {updated_count}.')
    return table_data

def delete(table_data: list, where_clause: dict | None = None) -> list:
    if not where_clause:
        count = len(table_data)
        table_data.clear()
        print(f'Удалено записей: {count}.')
        return table_data

    initial_count = len(table_data)
    table_data = [
        row for row in table_data 
        if not all(row.get(k) == v for k, v in where_clause.items())
    ]
    deleted_count = initial_count - len(table_data)
    print(f'Удалено записей: {deleted_count}.')
    return table_data

    
