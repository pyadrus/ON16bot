import logging

from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
    message_text = ("<b>Приветствую тебя, сногсшибательная леди!</b>\n\n"
                    "Королевская осанка, точеный силуэт, подтянутые высокие ягодицы, плоский живот, стройные ноги - все это приятные последствия тренировок со мной, твоим персональным тренером Мещеряковой Ольгой.\n\n"
                    "Пройди регистрацию и забирай домашний комплекс полноценных видео занятий 👇🏽\n\n"
                    "« регистрация»\n\n"
                    "Так же я жду тебя на канале с чатом и обратной связью,  где я делюсь :\n"
                    "- рецептами стройности\n"
                    "- эффективными упражнениям\n"
                    "- секретами красоты\n"
                    "-огромной порцией мотивации !\n"
                    "https://t.me/body_agency\n\n"
                    "Буду рада видеть твой отзыв и фото в костюме на wB!!")
    # Создаем инлайн кнопку "Получить видео"
    get_video_button = InlineKeyboardButton("Получить видео", callback_data="get_video")
    # Создаем инлайн кнопку "О нас"
    review_button = InlineKeyboardButton("О нас", callback_data="review")
    inline_keyboard = InlineKeyboardMarkup().row(get_video_button, review_button)

    await message.reply(message_text, reply_markup=inline_keyboard)


# Обработчик нажатия на инлайн кнопку
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
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)


# Запуск бота
if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
