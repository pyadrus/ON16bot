from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def welcome_keyboard():
    """Клавиатура приветствия"""
    get_video_button = InlineKeyboardButton("Получить видео", callback_data="get_video")
    inline_keyboard = InlineKeyboardMarkup().row(get_video_button)

    return inline_keyboard


def contact_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    first_button = KeyboardButton(text="📱 Отправить", request_contact=True)
    markup.add(first_button)
    return markup


if __name__ == "__main__":
    welcome_keyboard()
