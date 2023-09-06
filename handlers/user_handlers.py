import datetime
import sqlite3
from aiogram import types
from loguru import logger
import openpyxl
from openpyxl.utils import get_column_letter
from database.db_manager import recording_user_data, check_user_data_exists, database
from keyboards.user_keyboards import welcome_keyboard, contact_keyboard
from messages.user_messages import message_text
from system.dispatcher import dp, bot

# Настройка логирования
logger.add("setting/log/log.log", rotation="1 MB", compression="zip")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    inline_keyboard = welcome_keyboard()
    await message.reply(message_text, reply_markup=inline_keyboard)


# Обработчик для получения контакта
@dp.message_handler(content_types=types.ContentType.CONTACT, state="*")
async def get_contact(message: types.Message):
    contact = message.contact

    # Получение информации о пользователе
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    # Проверка наличия данных о пользователе в базе данных на основе user_id
    user_data_exists = check_user_data_exists(user_id)

    if user_data_exists:
        # Данные о пользователе уже существуют, номер телефона не запрашиваем
        await message.answer(f"Спасибо, {contact.full_name}.\nВы уже зарегистрированы.")

        send_video_text = ("Отправляем вам видео...\n"
                           "<a href='https://youtu.be/JXRep76T4yU'>Видео 1</a>\n"
                           "<a href='https://youtu.be/59npEilTIjg'>Видео 2</a>\n\n"
                           "Для возврата нажмите /start")
        await bot.send_message(message.chat.id, send_video_text, disable_web_page_preview=True)
    else:
        # Данные о пользователе отсутствуют, запрашиваем номер телефона и записываем данные
        number_phone = contact.phone_number
        date_now = datetime.datetime.now()

        # Запись данных о пользователе в базу данных
        recording_user_data(user_id, username, number_phone, first_name, last_name, date_now)

        send_video_text = (f"Спасибо, {contact.full_name}.\nЗа регистрацию"
                           "Отправляем вам видео...\n"
                           "<a href='https://youtu.be/JXRep76T4yU'>Видео 1</a>\n"
                           "<a href='https://youtu.be/59npEilTIjg'>Видео 2</a>\n\n"
                           "Для возврата нажмите /start")

        # Удаляем клавиатуру после получения номера
        await bot.send_message(message.chat.id, send_video_text, reply_markup=types.ReplyKeyboardRemove(),
                               disable_web_page_preview=True)


# Обработчик для кнопки "Получить видео"
@dp.callback_query_handler(lambda callback_query: callback_query.data == "get_video")
async def get_video(callback_query: types.CallbackQuery):
    """Ответ на нажатие inline кнопки get_video"""

    # Получение информации о пользователе
    user_id = callback_query.from_user.id

    # Проверка наличия данных о пользователе в базе данных на основе user_id
    user_data_exists = check_user_data_exists(user_id)

    if user_data_exists:
        # Данные о пользователе уже существуют, сразу отправляем видео
        send_video_text = ("Отправляем вам видео...\n"
                           "<a href='https://youtu.be/JXRep76T4yU'>Видео 1</a>\n"
                           "<a href='https://youtu.be/59npEilTIjg'>Видео 2</a>\n\n"
                           "Для возврата нажмите /start")
        await bot.send_message(callback_query.message.chat.id, send_video_text, disable_web_page_preview=True)
    else:
        text_message = ("📹 Для получения видео, необходимо пройти короткую регистрацию.\n\n"
                        "🔐 Регистрация проводится один раз.\n\n"
                        "<i>Для регистрации, пожалуйста, нажмите кнопку ниже, чтобы отправить контакт. 📱</i>")
        await bot.send_message(callback_query.message.chat.id, text_message, reply_markup=contact_keyboard())


# Обработчик команды export_user
@dp.message_handler(commands=['export_user'])
async def export_command(message: types.Message):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    # Получаем данные всех пользователей из базы данных
    cursor.execute('SELECT * FROM user_data')
    data = cursor.fetchall()
    # Создаем файл Excel и записываем данные
    wb = openpyxl.Workbook()
    sheet = wb.active
    # Записываем заголовки
    headers = ["user_id", "username", "number_phone", "first_name", "last_name", "date_now"]
    for col_num, header in enumerate(headers, 1):
        col_letter = get_column_letter(col_num)
        sheet[f'{col_letter}1'] = header
    # Записываем данные пользователей
    for row_num, row_data in enumerate(data, 2):
        for col_num, cell_data in enumerate(row_data, 1):
            col_letter = get_column_letter(col_num)
            sheet[f'{col_letter}{row_num}'] = cell_data
    # Сохраняем файл Excel
    wb.save('users.xlsx')
    # Отправляем файл пользователю
    with open('users.xlsx', 'rb') as file:
        await bot.send_document(message.from_user.id, file, caption='Данные пользователей в формате Excel')
    # Удаляем файл Excel
    import os
    os.remove('users.xlsx')


# Функция для регистрации обработчиков сообщений
def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(start_command)  # Обработчик команды /start, он же пост приветствия
