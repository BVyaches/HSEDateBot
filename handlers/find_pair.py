from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup

from SQL_funcs import *
from keyboards import *

"""
                name TEXT,'
               'gender TEXT,'
               'want_to_find TEXT,'
               'age INTEGER,'
               'faculty TEXT,'
               'photo TEXT,'
               'about TEXT,'
               'email TEXT,'
               """


class RegisterUser(StatesGroup):
    waiting_name = State()
    waiting_gender = State()
    waiting_want_to_find = State()
    waiting_age = State()
    waiting_faculty = State()
    waiting_photo = State()
    waiting_about = State()
    waiting_email = State()


async def register_user_start(message: types.Message):
    await message.answer('Как к вам обращаться?', reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_name.set()


async def register_user_name(message: types.Message, state: FSMContext):
    await state.update_data(waiting_name=message.text)
    await message.answer('Выберите ваш пол', reply_markup=await gender_keyboard())
    await RegisterUser.waiting_gender.set()


async def register_user_gender(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ['Парень', 'Девушка']:
        await message.answer('Пожалуйста, выберите пол из предложенных на клавиатуре',
                             reply_markup=await gender_keyboard())
        return True

    if gender == 'Парень':
        gender = 'm'
    else:
        gender = 'f'
    await state.update_data(waiting_gender=gender)
    await message.answer('Укажите, кого вы хотите найти')
    await RegisterUser.waiting_want_to_find.set()


async def register_user_want_to_find(message: types.Message, state: FSMContext):
    print(await state.get_data())

def register_handler_find_pair(dp: Dispatcher):
    dp.register_message_handler(register_user_start, Text(equals='Регистрация'), state='*')
    dp.register_message_handler(register_user_name, state=RegisterUser.waiting_name)
    dp.register_message_handler(register_user_gender, state=RegisterUser.waiting_gender)
    dp.register_message_handler(register_user_want_to_find, state=RegisterUser.waiting_want_to_find)
