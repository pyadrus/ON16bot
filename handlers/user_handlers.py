from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from messages.user_messages import message_text
from system.dispatcher import dp, bot


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    # Создаем InlineKey кнопку "Получить видео"
    get_video_button = InlineKeyboardButton("Получить видео", callback_data="get_video")
    # Создаем InlineKey кнопку "О нас"
    review_button = InlineKeyboardButton("О нас", callback_data="review")
    inline_keyboard = InlineKeyboardMarkup().row(get_video_button, review_button)

    await message.reply(message_text, reply_markup=inline_keyboard)


# Обработчик нажатия на InlineKey кнопку
@dp.callback_query_handler(lambda callback_query: callback_query.data == "get_video")
async def get_video(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, "Отправляем вам видео...")
    # Здесь можно добавить логику отправки видео пользователю


@dp.callback_query_handler(lambda callback_query: callback_query.data == "about_us")
async def about_us(callback_query: types.CallbackQuery):
    about_us_text = "Отзывы"

    await bot.answer_callback_query(callback_query.id, about_us_text)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(start_command)  # Обработчик команды /start, он же пост приветствия
