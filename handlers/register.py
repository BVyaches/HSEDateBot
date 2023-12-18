from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import aiogram.utils.markdown as fmt
from SQL_funcs import *
from formats import showing_user
from handlers.states import VerUser, RegisterUser, ProfileViewer, LoveLetter, DeactivateProfile
from keyboards import *
from initialization import dp

"""
                name TEXT,'
               'gender TEXT,'
               'want_to_find TEXT,'
               'age INTEGER,'
               'faculty TEXT,'
               'university TEXT'
               'photo TEXT,'
               'about TEXT,'
"""


@dp.message_handler(Text(equals='Анкета с нуля✏'), state=VerUser.is_verified)
@dp.message_handler(Text(equals='Давай попробуем😼'), state=VerUser.not_verified)
async def register_user_start(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(fmt.bold('📌Напиши своё имя, как к тебе обращаться?📌'),
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_name.set()


@dp.message_handler(state=RegisterUser.waiting_name)
async def register_user_name(message: types.Message, state: FSMContext):
    await state.update_data(waiting_name=message.text)
    await message.answer(fmt.bold('Выбери свой пол'), reply_markup=await gender_keyboard())
    await RegisterUser.waiting_gender.set()


@dp.message_handler(state=RegisterUser.waiting_gender)
async def register_user_gender(message: types.Message, state: FSMContext):
    gender = message.text
    if gender not in ['🧑🏻‍Парень', '👩🏻‍🦱Девушка']:
        await message.answer(
            fmt.bold('❗️Пожалуйста, выбери пол из предложенных на клавиатуре❗️'),
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

    await message.answer(fmt.bold('Сколько тебе лет?'),
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_age.set()


@dp.message_handler(state=RegisterUser.waiting_age)
async def register_user_age(message: types.Message, state: FSMContext):
    age = message.text

    if not age.isnumeric():
        await message.answer(fmt.bold('Пожалуйста, введи число'))
        return True

    await state.update_data(waiting_age=int(age))

    await message.answer(fmt.bold('🎓Твой университет?🎓'), reply_markup=types.ReplyKeyboardRemove())

    await RegisterUser.waiting_university.set()


@dp.message_handler(state=RegisterUser.waiting_university)
async def register_user_university(message: types.Message, state: FSMContext):
    university = message.text
    await state.update_data(waiting_university=university)
    await message.answer(fmt.bold('🎓Твой факультет?🎓'), reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_faculty.set()


@dp.message_handler(state=RegisterUser.waiting_faculty)
async def register_user_faculty(message: types.Message, state: FSMContext):
    faculty = message.text
    await state.update_data(waiting_faculty=faculty)
    await message.answer(fmt.bold('📸Оставь фоточку для анкеты📸'), reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_photo.set()


@dp.message_handler(state=RegisterUser.waiting_photo, content_types=['photo'])
@dp.message_handler(Text(equals='Изменить описание📝'), state=VerUser.is_verified)
async def register_user_photo(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state != 'VerUser:is_verified':
        photo = message.photo[0].file_id

        await state.update_data(waiting_photo=photo)

    await message.answer(fmt.bold('✏️Расскажи о себе (Одно-два предложения)✏️'),
                         reply_markup=types.ReplyKeyboardRemove())
    await RegisterUser.waiting_about.set()


@dp.message_handler(state=RegisterUser.waiting_about)
async def register_user_about(message: types.Message, state: FSMContext):
    about = message.text
    await state.update_data(waiting_about=about)

    user_id = message.from_user.id
    user_data = await get_user_data(user_id)

    if user_data:
        new_data = await state.get_data()
        print(new_data)
        if len(new_data) == 1:
            print()
            new_about = about
            await update_user_about(user_id, new_about)
        else:
            new_data = list(new_data.values())

            await update_user_data(user_id, new_data)
        current_data = await get_user_data(user_id)

        await message.answer(fmt.bold('Анкета успешно обновлена:'))
        await message.answer_photo(photo=current_data[5],
                                   caption=await showing_user(current_data))

        await show_menu(message, state)
    else:
        data = await state.get_data()
        data = [message.from_user.id] + list(data.values())
        await add_user(*data)
        await message.answer(fmt.bold('Регистрация успешна!'))
        await show_user_profile(message, state)
        await show_menu(message, state)


@dp.message_handler(Text(equals='Моя анкета'), state=VerUser.is_verified)
async def show_user_profile(message: types.Message, state: FSMContext):
    await message.answer(fmt.bold('Твоя анкета:'))
    user_data = await get_user_data(message.from_user.id)
    profile_text = await showing_user(user_data)
    await message.answer_photo(user_data[5], profile_text,
                               reply_markup=await user_profile_view_keyboard())


@dp.message_handler(Text(equals='Нет'), state=DeactivateProfile.waiting_for_approvement)
@dp.message_handler(Text(equals='Меню📌'), state=VerUser.is_verified)
@dp.message_handler(Text(equals='Меню📌'), state=ProfileViewer.waiting_response)
@dp.message_handler(Text(equals='Назад в меню📌'), state=LoveLetter.waiting_for_decision)
async def show_menu(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(fmt.bold('Что делаем?😎'),
                         reply_markup=await main_menu_keyboard())
    await VerUser.is_verified.set()


@dp.message_handler(Text(equals='Отключить анкету🔓'), state=VerUser.is_verified)
async def deactivate_user_profile_start(message: types.Message, state: FSMContext):
    await message.answer(
        fmt.bold('При отключении анкеты твой профиль больше не будет предлагаться другим пользователям. '
                 'Однако ты всегда сможешь активировать его обратно, просто начав просматривать анкеты\n'
                 'Отключить анкету?'),
        reply_markup=await agree_keyboard())
    await DeactivateProfile.waiting_for_approvement.set()


@dp.message_handler(Text(equals='Да'), state=DeactivateProfile.waiting_for_approvement)
async def deactivate_user_profile_finish(message: types.Message, state: FSMContext):
    await deactivate_profile(message.from_user.id)
    await message.answer(fmt.bold('Твоя анкета успешно отключена, ждём тебя снова!'))
    await show_menu(message, state)
