import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Установка уровня логирования
logging.basicConfig(level=logging.INFO)

# Токен вашего бота, полученный от @BotFather в Telegram
BOT_TOKEN = '6465724490:AAGTUbCQ5CqfeWwEQQmkpsApU2n80heFh5w'

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я простой бот. Напиши мне что-нибудь.")


# Обработчик текстовых сообщений
@dp.message_handler(content_types=types.ContentTypes.TEXT)
async def echo_message(message: types.Message):
    await message.reply(message.text)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
