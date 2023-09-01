import logging
from aiogram import executor
import configparser
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from messages.user_messages import message_text

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

config = configparser.ConfigParser(empty_lines_in_values=False, allow_no_value=True)
config.read("setting/config.ini")  # Чтение файла
bot_token = config.get('BOT_TOKEN', 'BOT_TOKEN')  # Получение токена

# Инициализация бота и диспетчера
bot = Bot(token=bot_token)
dp = Dispatcher(bot)


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
    about_us_text = ("Мы команда профессионалов, посвятивших свою жизнь созданию качественных продуктов и обучению.\n"
                     "Наша миссия - помочь вам достичь ваших целей и раскрыть ваш потенциал.\n"
                     "С нами вы можете быть уверены в качестве и надежности каждого нашего продукта.\n"
                     "Спасибо, что выбрали нас!")

    await bot.answer_callback_query(callback_query.id, about_us_text)


# Запуск бота
if __name__ == '__main__':


    executor.start_polling(dp, skip_updates=True)
