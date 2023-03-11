import json
import logging

from aiogram import Bot, Dispatcher, executor, types
import requests_async as requests
from aiogram.types import ParseMode

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = '6143073321:AAH1PbTZHibKqAgwrw6tNoltpdJ0UCsM6YQ'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    logging.info(f'{user_id} Hi !!')
    await message.reply(f'Hi {user_id}')


@dp.message_handler(commands=['get_task'])
async def get_data(message: types.Message):
    response = await requests.get("http://localhost:8000/tasks/tasks_by_name?name=The%20way%20home")
    data = response.json()

    json_formatted_str = json.dumps(data, indent=2)
    await message.answer(f"Here's the data: \n"
                         f"{json_formatted_str}")


if __name__ == '__main__':
    executor.start_polling(dp)
