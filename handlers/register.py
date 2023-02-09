from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from SQL_funcs import *
from formats import showing_user
from handlers.States import VerUser, RegisterUser
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


async def register_user_start(message: types.Message):
    await message.answer('Как к вам обращаться?',
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_name.set()


async def register_user_name(message: types.Message, state: FSMContext):
    await state.update_data(waiting_name=message.text)
    await message.answer('Выбери ваш пол', reply_markup=await gender_keyboard())
    await RegisterUser.waiting_gender.set()


async def register_user_gender(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ['🧑🏻‍Парень', '👩🏻‍🦱Девушка']:
        await message.answer(
            'Пожалуйста, выбери пол из предложенных на клавиатуре',
            reply_markup=await gender_keyboard())
        return True

    if gender == '🧑🏻‍Парень':
        gender = 'm'
    else:
        gender = 'f'
    await state.update_data(waiting_gender=gender)

    if gender == 'f':
        await state.update_data(waiting_want_to_find='m')
    else:
        await state.update_data(waiting_want_to_find='f')

    await message.answer('Сколько тебе лет?',
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_age.set()


async def register_user_age(message: types.Message, state: FSMContext):
    age = message.text

    if not age.isnumeric():
        await message.answer('Пожалуйста, введи число')
        return True

    await state.update_data(waiting_age=int(age))

    await message.answer('Укажи ваш факультет')

    await RegisterUser.waiting_faculty.set()


async def register_user_faculty(message: types.Message, state: FSMContext):
    faculty = message.text
    await state.update_data(waiting_faculty=faculty)
    await message.answer('Отправь 1 фото для анкеты')
    await RegisterUser.waiting_photo.set()


async def register_user_photo(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != 'VerUser:is_verified':
        photo = message.photo[0].file_id

        await state.update_data(waiting_photo=photo)

    await message.answer('Расскажи о себе')
    await RegisterUser.waiting_about.set()


async def register_user_about(message: types.Message, state: FSMContext):
    about = message.text
    await state.update_data(waiting_about=about)

    user_id = message.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        new_data = await state.get_data()
        print(new_data.values())
        if len(new_data) == 1:
            new_about = new_data.get('waiting_about')
            await update_user_about(user_id, new_about)
        else:
            new_data = list(new_data.values())

            await update_user_data(user_id, new_data)
        current_data = await get_user_data(user_id)
        await message.answer('Анкета успешно обновлена:')
        await message.answer_photo(photo=current_data[4],
                                   caption=await showing_user(current_data))

        await VerUser.is_verified.set()
        await message.answer('Чем займемся?',
                             reply_markup=await main_menu_keyboard())
    else:
        await message.answer(
            'Отправь свою @hse почту, чтобы мы могли подтвердить, что ты студент вышки')
        await RegisterUser.waiting_email.set()


async def register_user_email(message: types.Message, state: FSMContext):
    await RegisterUser.waiting_email.set()
    email = message.text
    print(email)
    print(await check_hse_mail(email))
    if await check_hse_mail(email) is None:
        await message.answer(
            'Пожалуйста, введи твою личную почту с доменом @hse')
        return True
    await state.update_data(waiting_email=email)

    code = await SendVerificationCode(email)
    await state.update_data(waiting_code=code)
    await message.answer(
        'На указанную почту отправлен код верификации. Отправь его.\n'
        'Проверьте папку спам', reply_markup=await email_keyboard())
    await RegisterUser.waiting_code.set()


async def register_user_code(message: types.Message, state: FSMContext):
    entered_code = message.text
    verification = await state.get_data()
    verification_code = verification['waiting_code']
    if entered_code != verification_code:
        await message.answer(
            'Похоже, введен не тот код. Попробуй еще раз или введи другую почту')
        return True

    data = await state.get_data()
    data = [message.from_user.id] + list(data.values())
    await add_user(*data[:-1])
    await message.answer('Регистрация успешна!',
                         reply_markup=types.ReplyKeyboardRemove())
    await message.answer('Чем займемся?',
                         reply_markup=await main_menu_keyboard())
    await state.finish()
    await VerUser.is_verified.set()


async def show_user_profile(message: types.Message, state: FSMContext):
    await message.answer('Ваша анкета:')
    user_data = await get_user_data(message.from_user.id)
    profile_text = await showing_user(user_data)
    await message.answer_photo(user_data[4], profile_text,
                               reply_markup=await user_profile_view_keyboard())


def register_handler_register(dp: Dispatcher):
    dp.register_message_handler(register_user_start,
                                Text(equals='Давай попробуем😼'),
                                state=VerUser.not_verified)
    dp.register_message_handler(register_user_name,
                                state=RegisterUser.waiting_name)
    dp.register_message_handler(register_user_gender,
                                state=RegisterUser.waiting_gender)
    dp.register_message_handler(register_user_age,
                                state=RegisterUser.waiting_age)
    dp.register_message_handler(register_user_faculty,
                                state=RegisterUser.waiting_faculty)
    dp.register_message_handler(register_user_photo,
                                state=RegisterUser.waiting_photo,
                                content_types=['photo'])
    dp.register_message_handler(register_user_about,
                                state=RegisterUser.waiting_about)
    dp.register_message_handler(register_user_email,
                                state=RegisterUser.waiting_email)
    dp.register_message_handler(register_user_email,
                                Text(equals='Ввести другой email'),
                                state=RegisterUser.waiting_code)
    dp.register_message_handler(register_user_code,
                                state=RegisterUser.waiting_code)
    dp.register_message_handler(show_user_profile, Text(equals='Моя анкета'),
                                state=VerUser.is_verified)
    dp.register_message_handler(register_user_start,
                                Text(equals='Заполнить заново'),
                                state=VerUser.is_verified)
    dp.register_message_handler(register_user_photo,
                                Text(equals='Поменять текст'),
                                state=VerUser.is_verified)
    # в коллы стейт *
