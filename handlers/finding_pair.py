import configparser
import aiogram.utils.markdown as fmt
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from SQL_funcs import *
from formats import showing_user, show_love_user
from handlers.states import VerUser, ProfileViewer, Complaint, BanUser
from initialization import bot, dp
from keyboards import *

config = configparser.ConfigParser()
config.read('config.ini')
admin_ids = list(map(int, config.get('CHAT_IDs', 'admin_ids').split(',')))


async def show_next_profile(message: types.Message, state: FSMContext):
    await state.reset_state(False)
    if message.text == 'Смотреть анкеты':
        await activate_profile(message.from_user.id)

    next_data = await get_next_person(message.from_user.id)
    if not next_data:
        await VerUser.is_verified.set()
        await message.answer(fmt.bold(
            'Похоже, пока что нет подходящих пользователей. Уверены, они скоро появятся, а пока чем займемся?'),
                             reply_markup=await main_menu_keyboard())
    else:
        await state.update_data(waiting_profile=next_data[0])
        profile_text = await showing_user(next_data)
        await message.answer_photo(photo=next_data[4], caption=profile_text,
                                   reply_markup=await profile_view_keyboard())
        await ProfileViewer.waiting_response.set()


async def profile_repsonse(message: types.Message, state: FSMContext):
    response = message.text
    if response not in ['❤', '👎🏻', 'Жалоба', 'Меню📌']:
        await message.answer(fmt.bold('Пожалуйста, выбери пункт из меню'))
        return True

    data = await get_user_data(message.from_user.id)
    profile_text = await showing_user(data)

    send_to_user = await state.get_data()
    send_to_user = send_to_user.get('waiting_profile')
    if response == '❤':
        try:
            await bot.send_message(chat_id=send_to_user, text=fmt.bold('Кто-то тебя оценил:'))
            await bot.send_photo(chat_id=send_to_user, photo=data[4],
                                 caption=profile_text,
                                 reply_markup=await response_keyboard(
                                     message.from_user.id))
            await message.answer(fmt.bold('Твой лайк отправлен!'))
        except BotBlocked:
            await message.answer(fmt.bold('Похоже, данный пользователь перестал пользоваться ботом'))
            await delete_user(send_to_user)

        await ProfileViewer.waiting_profile.set()
        await show_next_profile(message, state)

    elif response == '👎🏻':
        await ProfileViewer.waiting_profile.set()
        await show_next_profile(message, state)

    elif response == 'Жалоба':
        await message.answer(fmt.bold('Опиши причину жалобы'),
                             reply_markup=types.ReplyKeyboardRemove())
        await Complaint.waiting_message.set()
        await state.update_data(complaint_user=send_to_user)

    elif response == 'Меню📌':
        await VerUser.is_verified.set()
        await message.answer(fmt.bold('Что делаем?😎'),
                             reply_markup=await main_menu_keyboard())


async def user_was_liked(call: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    if current_state != 'VerUser:not_verified':

        user_first = int(call.from_user.id)
        user_first_data = await get_user_data(user_first)
        user_second = int(call.data.replace('Love', ''))
        await call.message.edit_reply_markup(reply_markup=await is_responsed())
        print(user_first, user_second)

        await bot.send_message(user_first,
                               'У вас взаимная симпатия! ' + await show_love_user(
                                   user_second),
                               parse_mode='html')
        await bot.send_message(user_second,
                               'У вас взаимная симпатия! ' + await show_love_user(
                                   user_first),
                               parse_mode='html')
        await bot.send_photo(user_second, photo=user_first_data[4],
                             caption=await showing_user(user_first_data))
    else:
        await call.message.answer(fmt.bold('Пожалуйста, пройди регистрацию для ответа'))


async def user_no_love(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await is_responsed())


async def wait_for_complaint(message: types.Message, state: FSMContext):
    complaint_id = await state.get_data()
    complaint_id = complaint_id.get('complaint_user')
    user_data = await get_all_user_data(complaint_id)
    user_email = user_data[-1]
    text = f'Жалоба на пользователя с почтой {user_email} и с ' \
           f'id <a href="tg://user?id={complaint_id}">{complaint_id}</a> \n' \
           f'{message.text}'

    for admin_id in admin_ids:
        await bot.send_message(admin_id, text, parse_mode='html')
        await bot.send_photo(admin_id, photo=user_data[4],
                             caption=await showing_user(user_data[:-1]),
                             reply_markup=await complaint_to_admin_keyboard(
                                 complaint_id))
    await state.finish()
    await message.answer(fmt.bold('Ваша жалоба отправлена'))
    await show_next_profile(message, state)


async def ban_user_start(call: types.CallbackQuery, state: FSMContext):
    user_id = int(call.data.replace('BAN', ''))
    print(101)
    await call.message.edit_reply_markup(reply_markup=None)
    await BanUser.waiting_comment.set()
    await state.update_data(user_to_ban_id=user_id)
    await call.message.answer(
        'Введите пояснительный комментарий для заблокированного пользователя')


async def ban_user_finish(message: types.Message, state: FSMContext):
    ban_comment = message.text
    state_data = await state.get_data()
    user_to_ban_id = state_data.get('user_to_ban_id')
    user_state = dp.current_state(user=user_to_ban_id)
    try:
        await bot.send_message(user_to_ban_id, fmt.bold(
            f'Вы были заблокированы по следующей причине:\n'
            f'{ban_comment}\n'
            f'Ваша анкета была удалена. Для продолжения '
            f'пользования ботом введите команду /start и '
            f'пройдите регистрацию заново'),
                               reply_markup=await start_from_ban_keyboard())
        await user_state.set_state(VerUser.not_verified)
        await delete_user(user_to_ban_id)
        await message.answer('Пользователь заблокирован')
    except BotBlocked:
        await delete_user(user_to_ban_id)
        await message.answer('Похоже, данный пользователь заблокировал бота. Его анкета удалена')

    await state.finish()


async def show_pass_keyboard(call: types.CallbackQuery):
    await call.message.edit_reply_markup(reply_markup=await pass_keyboard())


def register_handler_finding_pair(dp: Dispatcher):
    dp.register_message_handler(show_next_profile,
                                Text(equals='Смотреть анкеты'),
                                state=VerUser.is_verified)
    dp.register_message_handler(show_next_profile,
                                state=ProfileViewer.waiting_profile)
    dp.register_message_handler(profile_repsonse,
                                state=ProfileViewer.waiting_response)
    dp.register_callback_query_handler(user_was_liked, Text(startswith='Love'), state='*')
    dp.register_message_handler(wait_for_complaint,
                                state=Complaint.waiting_message)
    dp.register_callback_query_handler(user_no_love, Text(equals='No'), state='*')
    dp.register_callback_query_handler(ban_user_start, Text(startswith='BAN'), state='*')
    dp.register_message_handler(ban_user_finish, state=BanUser.waiting_comment)
    dp.register_callback_query_handler(show_pass_keyboard, Text(equals='PASS'), state='*')
