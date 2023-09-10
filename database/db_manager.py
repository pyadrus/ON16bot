import sqlite3
from loguru import logger

logger.add("setting/log/log.log", rotation="1 MB", compression="zip")
database = "setting/database.db"


def check_user_data_exists(user_id):
    """Функция для проверки наличия данных о пользователе в базе данных"""
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        # Выполняем запрос к базе данных для проверки наличия данных о пользователе
        cursor.execute("SELECT COUNT(*) FROM user_data WHERE user_id=?", (user_id,))
        result = cursor.fetchone()
        conn.close()
        # Если результат больше 0, значит, данные уже существуют, если результат равен 0, значит, данные отсутствуют
        return result[0] > 0
    except Exception as e:
        logger.exception(e)
        print("Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
        return False  # Возвращаем False в случае ошибки


def record_user_to_db(user_id, username, first_name, last_name, date_now):
    """
    Записывает информацию о пользователе в базу данных SQLite.
    Параметры:
    - user_id (int): Идентификатор пользователя.
    - username (str): Логин пользователя (если доступен).
    - first_name (str): Имя пользователя.
    - last_name (str): Фамилия пользователя.
    - date_now (datetime.datetime): Дата и время регистрации пользователя.
    Внутренние действия:
    1. Устанавливает соединение с базой данных (или создает базу данных, если её нет).
    2. Создает курсор для выполнения SQL-запросов.
    3. Вставляет данные пользователя в таблицу user_data.
    4. Выполняет коммит и закрывает соединение с базой данных.
    Пример использования:
    record_user_to_db(user_id, username, first_name, last_name, date_now)
    """
    try:
        conn = sqlite3.connect(database)  # Замените 'your_database.db' на имя вашей базы данных
        cursor = conn.cursor()
        # Создаем таблицу user_data, если она ещё не существует
        cursor.execute('''CREATE TABLE IF NOT EXISTS user_run_bot 
                          (user_id, username, first_name, last_name, date_now)''')
        # Вставляем данные пользователя в таблицу
        cursor.execute('''INSERT INTO user_run_bot 
                               (user_id, username, first_name, last_name, date_now) VALUES (?, ?, ?, ?, ?) ''',
                       (user_id, username, first_name, last_name, date_now))
        conn.commit()
    except Exception as e:
        print(f"Ошибка при записи пользователя в базу данных: {str(e)}")
    finally:
        conn.close()


def recording_user_data(user_id, username, number_phone, first_name, last_name, date_now):
    """
    Запись данных, новых пользователей в базу данных setting/database.db
    user_id - id пользователя,
    username - username пользователя,
    number_phone - номер телефона пользователя,
    first_name - имя пользователя,
    last_name - фамилия пользователя,
    date_now - дата регистрации.
    """
    try:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS user_data "
                       "(user_id, username, number_phone, first_name, last_name, date_now)")
        cursor.execute("INSERT INTO user_data (user_id, username, number_phone, first_name, last_name, date_now) "
                       "VALUES (?, ?, ?, ?, ?, ?)", (user_id, username, number_phone, first_name, last_name, date_now))
        conn.commit()
        conn.close()
    except Exception as e:
        logger.exception(e)
        print("Произошла ошибка, для подробного изучения проблемы просмотрите файл log.log")
