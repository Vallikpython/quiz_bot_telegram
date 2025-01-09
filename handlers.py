from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
from quizion import quiz_data
import bd
import quizion

# Диспетчер
dp = Dispatcher()


    
@dp.callback_query()
async def right_answer(callback : types.CallbackQuery):
    user_id = callback.from_user.id
    # Запрашиваем из базы текущий индекс для вопроса
    current_question_index, i = await bd.get_quiz_index(user_id)
    # Получаем индекс правильного ответа для текущего вопроса
    correct_index = quiz_data[current_question_index]['correct_option']
    # Получаем список вариантов ответа для текущего вопроса
    opts = quiz_data[current_question_index]['options']

    if callback.data == opts[correct_index]:

        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )

        # Получение текущего вопроса из словаря состояний пользователя
        current_question_index, correct_answers = await bd.get_quiz_index(callback.from_user.id)
        correct_option = quiz_data[current_question_index]['correct_option']


        await callback.message.answer(f"Ваш ответ: {quiz_data[current_question_index]['options'][correct_option]}")
        current_question_index, correct_answers = await bd.get_quiz_index(callback.from_user.id)
        # Обновление номера текущего вопроса в базе данных
        current_question_index += 1
        correct_answers += 1
        await bd.update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, correct_answers)


        if current_question_index < len(quiz_data):
            await quizion.get_question(callback.message, callback.from_user.id)
        else:
            await callback.message.answer("Это был последний вопрос. Квиз завершен!")
    else:
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )

        # Получение текущего вопроса из словаря состояний пользователя
        current_question_index, i = await bd.get_quiz_index(callback.from_user.id)

        await callback.message.answer(f"Ваш ответ: {callback.data}")

        # Обновление номера текущего вопроса в базе данных
        current_question_index += 1
        await bd.update_quiz_index(callback.from_user.id, callback.from_user.full_name, current_question_index, i)


        if current_question_index < len(quiz_data):
             await quizion.get_question(callback.message, callback.from_user.id)
        else:
            await callback.message.answer("Это был последний вопрос. Квиз завершен!")



# Хэндлер на команду /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Узнать статистику"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))


# Хэндлер на команду /quiz
@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await message.answer(f"Давайте начнем квиз!")
    await quizion.new_quiz(message)

@dp.message(F.text=="Узнать статистику")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):

    await quizion.get_static(message)