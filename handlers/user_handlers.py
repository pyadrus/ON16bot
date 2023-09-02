from aiogram import types

from keyboards.user_keyboards import welcome_keyboard
from messages.user_messages import message_text
from system.dispatcher import dp, bot


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    inline_keyboard = welcome_keyboard()
    await message.reply(message_text, reply_markup=inline_keyboard)


# Обработчик нажатия на InlineKey кнопку
@dp.callback_query_handler(lambda callback_query: callback_query.data == "get_video")
async def get_video(callback_query: types.CallbackQuery):
    """Ответ на нажатие inline кнопки get_video"""
    await bot.answer_callback_query(callback_query.id, "Отправляем вам видео...")
    # Здесь можно добавить логику отправки видео пользователю


@dp.callback_query_handler(lambda callback_query: callback_query.data == "about_us")
async def about_us(callback_query: types.CallbackQuery):
    """Ответ на нажатие inline кнопки about_us"""
    about_us_text = "Отзывы"
    await bot.answer_callback_query(callback_query.id, about_us_text)


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(start_command)  # Обработчик команды /start, он же пост приветствия
