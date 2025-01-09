import aiosqlite
from config import DB_NAME

async def get_quiz_index(user_id):
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index, correct_answers FROM quiz_state WHERE user_id = (?)', (user_id, )) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                 return results[0], results[1]
            else:
                return 0

async def get_static_bd():
     # Подключаемся к базе данных
     async with aiosqlite.connect(DB_NAME) as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT full_name, correct_answers FROM quiz_state') as cursor:
            # massive = db.fetchone()
            # Возвращаем результат
            results = await cursor.fetchall()
            if results is not None:
                 return results
            else:
                return 0

async def update_quiz_index(user_id, full_name, index, correct_answers):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, full_name, question_index, correct_answers) VALUES (?, ?, ?, ?)', (user_id, full_name, index, correct_answers))
        # Сохраняем изменения
        await db.commit()



async def create_table():
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect(DB_NAME) as db:
        # Создаем таблицу
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, full_name TEXT NOT NULL, question_index, correct_answers INTEGER)''')
        # Сохраняем изменения
        await db.commit()
