import aiogram.utils.markdown as fmt
from aiogram import types
from SQL_funcs import get_user_data


async def showing_user(data: list):
    user_id, name, age, faculty, university, photo, about = data
    first_field = name + ', ' + str(age) + ', ' + university + ', ' + faculty
    second_field = about
    result = first_field + '\n' + second_field
    return result


async def show_love_user(user_id):
    user_id = int(user_id)
    result = fmt.text(f'[Перейти к диалогу](tg://user?id={user_id})')
    return result


async def bold(text):
    result = fmt.bold(text)
