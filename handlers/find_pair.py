from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from initialization import bot
from SQL_funcs import *
from keyboards import *
from verification import check_hse_mail, SendVerificationCode

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
    await message.answer('Выбери ваш пол', reply_markup=await gender_keyboard())
    await RegisterUser.waiting_gender.set()


async def register_user_gender(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ['Парень', 'Девушка']:
        await message.answer('Пожалуйста, выбери пол из предложенных на клавиатуре',
                             reply_markup=await gender_keyboard())
        return True

    if gender == 'Парень':
        gender = 'm'
    else:
        gender = 'f'
    await state.update_data(waiting_gender=gender)

    if gender == 'f':
        await state.update_data(waiting_want_to_find='m')
    else:
        await state.update_data(waiting_want_to_find='f')

    await message.answer('Сколько тебе лет?', reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_age.set()


async def register_user_age(message: types.Message, state: FSMContext):
    age = message.text

    if not age.isnumeric():
        await message.answer('Пожалуйста, введи число')
        return True

    await state.update_data(waiting_age=int(age))

    await message.answer('Укажи ваш факультет')

    await bot.send_message(message.from_user.id, await state.get_data())
    await RegisterUser.waiting_faculty.set()


async def register_user_faculty(message: types.Message, state: FSMContext):
    faculty = message.text
    await state.update_data(waiting_faculty=faculty)
    await message.answer('Отправь 1 фото для анкеты')
    await RegisterUser.waiting_photo.set()


async def register_user_photo(message: types.Message, state: FSMContext):
    photo = message.photo[0].file_id
    await RegisterUser.waiting_about.set()

    await state.update_data(waiting_photo=photo)
    await message.answer('Расскажи о себе')


async def register_user_about(message: types.Message, state: FSMContext):
    about = message.text
    await state.update_data(waiting_about=about)
    await message.answer('Отправь свою @hse почту, чтобы мы могли подтвердить, что ты студент вышки')
    await RegisterUser.waiting_email.set()

async def register_user_email(message: types.Message, state: FSMContext):
    email = message.text
    if not check_hse_mail(email):
        await message.answer('Пожалуйста, введи твою личную почту с доменом @hse')
        return True

    code = await SendVerificationCode(email)



def register_handler_find_pair(dp: Dispatcher):
    dp.register_message_handler(register_user_start, Text(equals='Регистрация'), state='*')
    dp.register_message_handler(register_user_name, state=RegisterUser.waiting_name)
    dp.register_message_handler(register_user_gender, state=RegisterUser.waiting_gender)
    dp.register_message_handler(register_user_age, state=RegisterUser.waiting_age)
    dp.register_message_handler(register_user_faculty, state=RegisterUser.waiting_faculty)
    dp.register_message_handler(register_user_photo, state=RegisterUser.waiting_photo, content_types=['photo'])
