from aiogram import Bot, types
from aiogram.utils.keyboard import InlineKeyboardBuilder 
import json
import os
import matplotlib.pyplot as plt
from aiogram.types import FSInputFile
from config import TOKEN
import bd 
# Читаем токен из файла
API_TOKEN = TOKEN
# Объект бота
bot = Bot(token=API_TOKEN)
with open('duiz_data.json',  'r', encoding='utf-8') as json_file:
    quiz_data = json.load(json_file)


def generate_options_keyboard(answer_options):
    builder = InlineKeyboardBuilder()

    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=option
            )
        )

    builder.adjust(1)
    return builder.as_markup()


async def get_static(message):
    user = await bd.get_static_bd()
    user_static=[]
    user_key = []
    for value, key in user:
        user_static.append(value)
        user_key.append(key)
    plt.bar(user_static, user_key)

    plt.savefig('foo.JPG')

    photo = FSInputFile('./foo.JPG')
    await bot.send_photo(chat_id=message.chat.id, photo=photo)
    os.remove('./foo.JPG')


async def get_question(message, user_id):

    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index, i = await bd.get_quiz_index(user_id)

    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    # Функция генерации кнопок для текущего вопроса квиза
    # В качестве аргументов передаем варианты ответов и значение правильного ответа (не индекс!)
    kb = generate_options_keyboard(opts)
    # Отправляем в чат сообщение с вопросом, прикрепляем сгенерированные кнопки
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)



async def new_quiz(message):
    user_id = message.from_user.id
    full_name = message.chat.full_name
    current_question_index = 0
    correct_answers = 0
    await bd.update_quiz_index(user_id, full_name, current_question_index, correct_answers)
    await get_question(message, user_id)

