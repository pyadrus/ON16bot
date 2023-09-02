from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def welcome_keyboard():
    """Клавиатура приветствия"""
    get_video_button = InlineKeyboardButton("Получить видео", callback_data="get_video")
    # Создаем InlineKey кнопку "О нас"
    review_button = InlineKeyboardButton("О нас", callback_data="review")
    inline_keyboard = InlineKeyboardMarkup().row(get_video_button, review_button)

    return inline_keyboard


if __name__ == "__main__":
    welcome_keyboard()
