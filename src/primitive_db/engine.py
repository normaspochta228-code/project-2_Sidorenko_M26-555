import shlex

import prompt

from primitive_db.core import create_table, drop_table
from primitive_db.utils import DB_META_JSON, load_metadata, print_help, save_metadata


def run():

    print_help()

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

        if command == 'create_table':
            if len(args) < 2:
                print('Ошибка: Укажите имя таблицы. Пример: create users name:str age:int')
                continue
            table_name = args[1]
            columns = args[2:]
            
            updated_meta = create_table(metadata, table_name, columns)
            if updated_meta is not None:
                save_metadata(DB_META_JSON, updated_meta)

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


        elif command == 'help':
            print_help()


        elif command == 'exit':
            print('Выход из программы')
            break

        else:
            print(f'Функции <{command}> нет. Попробуйте снова.')
