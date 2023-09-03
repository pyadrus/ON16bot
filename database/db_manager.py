import sqlite3
from loguru import logger

logger.add("setting/log/log.log", rotation="1 MB", compression="zip")


def recording_user_data(user_id, username, number_phone, first_name, last_name, date_now):
    """Запись данных, новых пользователей в базу данных setting/database.db
    user_id - id пользователя,
    username - username пользователя,
    number_phone - номер телефона пользователя,
    first_name - имя пользователя,
    last_name - фамилия пользователя,
    date_now - дата регистрации.
    """
    try:
        conn = sqlite3.connect("setting/database.db")
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
