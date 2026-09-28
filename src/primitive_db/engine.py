import shlex

import prompt
from prettytable import PrettyTable

from cache import create_cacher
from primitive_db.constants import DB_META_JSON
from primitive_db.core import create_table, delete, drop_table, insert, select, update
from primitive_db.parse import parse_clause
from primitive_db.utils import (
    load_metadata,
    load_table_data,
    print_help,
    save_metadata,
    save_table_data,
)


def run():
    """Главный интерфейс приложения; Вызывает все функции описанные в core"""

    print_help()

    db_cache = create_cacher()

    while True:

        user_input = prompt.string('\nВведите команду: ')

        if not user_input.strip():
            continue

        try:
            args = shlex.split(user_input)
        except ValueError as e:
            print(f'Ошибка разбора команды: {e}')
            continue

        command = args[0].lower()

        metadata = load_metadata()

        if command in ("create", "drop", "insert", "update", "delete"):
            # сброс кеша
            db_cache = create_cacher()

        if command == 'create_table':
            if len(args) < 2:
                print('Ошибка: Укажите имя таблицы. Пример: create users name:str age:int')
                continue
            table_name = args[1]
            columns = args[2:]
            
            updated_meta = create_table(metadata, table_name, columns)
            if updated_meta is not None:
                save_metadata(DB_META_JSON, updated_meta)
                save_table_data(table_name, [])

        elif command == 'list_tables':
            print('- ' + '\n- '.join([table for table in metadata]))

        elif command == 'drop_table':
            if len(args) != 2:
                print('Ошибка: Укажите имя таблицы для удаления. Пример: drop users')
                continue

            table_name = args[1]
            
            updated_meta = drop_table(metadata, table_name)
            if updated_meta is not None:
                save_metadata(DB_META_JSON, updated_meta)


        elif command == 'insert':
            if len(args) < 2 or args[1].lower() != 'into' or args[3].lower() != 'values':
                print('Ошибка: Неправильный формат ввода. Пример: insert into table values (va1, val2)')
                continue

            arguments = [item.strip("(),'\"") for item in args[4:]]
            table_name = args[2]
            table_data = load_table_data(table_name)
            updated_data = insert(metadata, table_name, table_data, arguments)
            if updated_data is not None:
                save_table_data(table_name, updated_data)

        elif command == 'select':
            if len(args) < 3 or args[1].lower() != 'from':
                print('Ошибка: Неверный формат. Пример: select from users where age = 22')
                continue

            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблицы "{table_name}" не существует.')
                continue

            cache_key = user_input.strip().lower()
            
            where_dict = None
            if len(args) > 3:
                if args[3].lower() == 'where':
                    where_dict = parse_clause(args[4:])
                else:
                    print('Ошибка: Ожидалось ключевое слово "where".')
                    continue

            # одноразовая функция для функции кеша
            fetch_data = lambda t=table_name, w=where_dict: select(load_table_data(t), w)


            results = db_cache(cache_key, fetch_data)
            
            table = PrettyTable()
            table.field_names = [col['name'] for col in metadata[table_name]['columns']]
            for row in results:
                table.add_row([row.get(col) for col in table.field_names])
            print(table)


        elif command == 'update':
            if len(args) < 4 or args[2].lower() != 'set':
                print('Ошибка: Неверный формат. Пример: update users set age = 23 where name = Nikita')
                continue
            table_name = args[1]
            if table_name not in metadata:
                print(f'Ошибка: Таблицы "{table_name}" не существует.')
                continue

            try:
                where_idx = [x.lower() for x in args].index('where')
                set_tokens = args[3:where_idx]
                where_tokens = args[where_idx+1:]
            except ValueError:
                set_tokens = args[3:]
                where_tokens = []

            set_dict = parse_clause(set_tokens)
            where_dict = parse_clause(where_tokens) if where_tokens else None

            if set_dict:
                table_data = load_table_data(table_name)
                updated_data = update(table_data, set_dict, where_dict)
                save_table_data(table_name, updated_data)

        elif command == 'delete':
            if len(args) < 3 and args[1].lower() != 'from':
                print('Ошибка: Неверный формат. Пример: delete from users where age = 22')
                continue
            
            table_name = args[2]
            if table_name not in metadata:
                print(f'Ошибка: Таблицы "{table_name}" не существует.')
                continue

            where_dict = None
            if len(args) > 3 and args[3].lower() == 'where':
                where_dict = parse_clause(args[4:])


            table_data = load_table_data(table_name)
            updated_data = delete(table_data, where_dict)
            save_table_data(table_name, updated_data)

        elif command == 'info':
            if len(args) != 2:
                print('Ошибка: Неверный формат. Пример: info users')
                continue

            table_name = args[1]
            table_metadata = metadata.get(table_name, None)
            if table_metadata is None:
                print(f'Ошибка: Таблицы "{table_name}" не существует.')
                continue

            table_metadata = [f'{item['name']}:{item['type']}' for item in table_metadata['columns']]
            len_data = len(load_table_data(table_name))


            print(f'Таблица {table_name}')
            print(f'Столбцы: {", ".join(table_metadata)}')
            print(f'Количество записей: {len_data}')


        elif command == 'help':
            print_help()

        elif command == 'exit':
            print('Выход из программы')
            break

        else:
            print(f'Функции <{command}> нет. Попробуйте снова.')
