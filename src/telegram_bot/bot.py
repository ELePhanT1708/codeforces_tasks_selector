import json
import logging

from aiogram import Bot, Dispatcher, executor, types
import requests_async as requests
from requests import JSONDecodeError

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
    logging.info(f'Hi {user_id} !!')
    await message.reply(f'Hi {user_id}')


@dp.message_handler(commands=['get_task_by_name'], )
async def get_data(message: types.Message):
    await message.answer('>>>> Loading...')
    try:
        name = " ".join(message.text.split()[1:])  # Название задачи
        response = await requests.get(f"http://localhost:8000/tasks/tasks_by_name?name={name}")
        print(response.text)
        if response.text:
            data = response.json()
            json_formatted_str = json.dumps(data, indent=2)
            logging.info(f"Here's the data about '{name}' task: \n"
                         f"{json_formatted_str}")
            await message.answer(f"Here's the data about '{name}' task: \n"
                                 f"{json_formatted_str}")
        else:
            await message.answer(f"Не нашлось заданной задачи в базе данных !")

    except UnboundLocalError:
        await message.answer('Не ввели название задачи !!\n'
                             'Прочитайте описание команды')
    except JSONDecodeError:
        await message.answer('Не ввели название задачи !!\n'
                             'Прочитайте описание команды')


@dp.message_handler(commands=['get_all_tags'], )
async def get_data(message: types.Message):
    await message.answer('>>>> Loading...')
    response = await requests.get(f"http://localhost:8000/tasks/get_tags")
    data = response.json()

    json_formatted_str = json.dumps(data, indent=2)
    logging.info(f"Here's the data about all tags: \n"
                 f"{json_formatted_str}")
    await message.answer(f"Here's the data about all tags: \n"
                         f"{json_formatted_str}")


@dp.message_handler(commands=['get_tasks_by_tag_and_rating'], )
async def get_data(message: types.Message):
    await message.answer('>>>> Loading...')
    try:
        tag_name = " ".join(message.text.split()[1:-1])  # Название темы
        rating = int(message.text.split()[-1])  # Рейтинг задачи
        response = await requests.get(f"http://localhost:8000/tasks/tasks_by_tag_and_rating?tag_name={tag_name}"
                                      f"&rating={rating}")
        data = response.json()
        json_formatted_str = json.dumps(data, indent=2)
        logging.info(f"Here's the tasks with '{tag_name}' and rating = {rating}: \n"
                     f"{json_formatted_str}")
        await message.answer(f"Here's the tasks with '{tag_name}' and rating = {rating}: \n"
                             f"{json_formatted_str}")
    except ValueError:
        await message.answer('Не ввели параметры для поиска , либо ввели их некорректно!!\n'
                             'Прочитайте описание команды!')
    except JSONDecodeError:
        await message.answer('Не ввели параметры для поиска , либо ввели их некорректно!!\n'
                             'Прочитайте описание команды!')


if __name__ == '__main__':
    executor.start_polling(dp)
    # print(check())
