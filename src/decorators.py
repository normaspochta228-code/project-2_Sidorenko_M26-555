import functools
import time
import traceback

import prompt


def handle_db_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print('Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.')
        except KeyError as e:
            print(f'Ошибка: Таблица или столбец {e} не найден.')
        except ValueError as e:
            print(f'Ошибка валидации: {e}')
        except Exception as e: # noqa: BLE001
            print(f'Произошла непредвиденная ошибка: {traceback.format_exc()}{e}')
    return wrapper

def confirm_action(action_name: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            answer = prompt.string(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ')
            
            if answer.strip().lower() == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                return None
        return wrapper
    return decorator


def log_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        
        # Выполняем саму функцию
        result = func(*args, **kwargs)
        
        finish_time = time.monotonic()
        exc_time = finish_time - start_time
        
        print(f"Функция <{func.__name__}> выполнилась за {exc_time:.3f} секунд.")
        
        return result
    return wrapper