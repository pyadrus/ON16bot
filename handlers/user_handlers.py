from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboards.user_keyboards import welcome_keyboard
from messages.user_messages import message_text
from system.dispatcher import dp, bot


@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    inline_keyboard = welcome_keyboard()
    await message.reply(message_text, reply_markup=inline_keyboard)


async def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text="📱 Отправить", request_contact=True)
    markup.add(first_button)
    return markup


@dp.message_handler(content_types=types.ContentType.CONTACT)
async def get_contact(message: types.Message):
    contact = message.contact
    await message.answer(f"Спасибо, {contact.full_name}.\nЗа регистрацию")

    send_video_text = ("Отправляем вам видео...\n"
                       "<a href='https://youtu.be/JXRep76T4yU'>Видео 1</a>\n"
                       "<a href='https://youtu.be/59npEilTIjg'>Видео 2</a>\n\n"
                       "Для возврата нажмите /start")
    await bot.send_message(message.chat.id, send_video_text, disable_web_page_preview=True)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "get_video")
async def get_video(callback_query: types.CallbackQuery):
    """Ответ на нажатие inline кнопки get_video"""
    text_message = ("📹 Для получения видео, необходимо пройти короткую регистрацию.\n\n"
                    "🔐 Регистрация проводится один раз.\n\n"
                    "<i>Для регистрации, пожалуйста, нажмите кнопку ниже, чтобы отправить контакт. 📱</i>")
    await bot.send_message(callback_query.message.chat.id, text_message, reply_markup=await contact_keyboard())


def greeting_handler():
    """Регистрируем handlers для бота"""
    dp.register_message_handler(start_command)  # Обработчик команды /start, он же пост приветствия
