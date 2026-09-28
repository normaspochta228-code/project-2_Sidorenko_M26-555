import json
import os

from primitive_db.constants import DATA_DIR, DB_META_JSON


def load_metadata(filepath: str = DB_META_JSON) -> list | dict:
    """Load Database metadata"""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_metadata(filepath: str, data: list | dict) -> None:
    """Save Database metadata"""
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_table_data(table_name: str) -> list:
    """Load table data"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f'{table_name}.json')
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_table_data(table_name: str, data: list) -> None:
    """Save table data"""
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f'{table_name}.json')
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def print_help():
    '''Prints the help message for the current mode.'''
   
    print('\n***Процесс работы с таблицей***')
    print('Функции:')
    print('<command> create_table <имя_таблицы> <столбец1:тип> .. - создать таблицу')
    print('<command> list_tables - показать список всех таблиц')
    print('<command> drop_table <имя_таблицы> - удалить таблицу')

    print('\n***Операции с данными***')
    print('Функции:')
    print('<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.')
    print('<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.')
    print('<command> select from <имя_таблицы> - прочитать все записи.')
    print('<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.')

    print('<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить записи по условию.')
    print('<command> delete from <имя_таблицы> - удалить все записи.')
    print('<command> info <имя_таблицы> - вывести информацию о таблице.')
    
    print('\nОбщие команды:')
    print('<command> exit - выход из программы')
    print('<command> help - справочная информация')



