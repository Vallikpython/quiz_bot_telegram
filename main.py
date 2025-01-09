import asyncio
import logging
from aiogram import Bot
from config import TOKEN
from bd import create_table
from handlers import dp
# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Читаем токен из файла
API_TOKEN = TOKEN
# Объект бота
bot = Bot(token=API_TOKEN)

# Присваиваем объект бота диспетчеру
dp.bot = bot



# Запуск процесса поллинга новых апдейтов
async def main():

    # Запускаем создание таблицы базы данных
    await create_table()

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())