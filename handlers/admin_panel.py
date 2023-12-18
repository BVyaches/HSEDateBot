import configparser
import aiogram.utils.markdown as fmt
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.utils.exceptions import BotBlocked
from SQL_funcs import *
from handlers.states import AdminMassPost, VerUser
from initialization import bot, dp
from keyboards import *

config = configparser.ConfigParser()
config.read('config.ini')
admin_ids = list(map(int, config.get('CHAT_IDs', 'admin_ids').split(',')))


@dp.message_handler(commands=['admin'], state=VerUser.is_verified)
async def admin_start(message: types.Message):
    if message.from_user.id in admin_ids:
        await message.answer(fmt.bold('Что требуется?'), reply_markup=await admin_keyboard())


@dp.message_handler(Text(equals='Статистика'), state=VerUser.is_verified)
async def get_stats(message: types.Message):
    if message.from_user.id in admin_ids:
        all_users = await get_all_users()
        await message.answer(fmt.bold(f'Количество пользователей: {len(all_users)}'))
        await message.answer(fmt.bold('Что требуется?'), reply_markup=await admin_keyboard())


@dp.message_handler(Text(equals='Массовая рассылка'), state=VerUser.is_verified)
async def start_sending(message: types.Message):
    if message.from_user.id in admin_ids:
        await message.answer(
            fmt.bold('Отправьте сообщение, которое хотите разослать всем. Если с фото, то отправьте его с подписью'),
            reply_markup=types.ReplyKeyboardRemove())
        await AdminMassPost.waiting_for_post.set()


@dp.message_handler(state=AdminMassPost.waiting_for_post, content_types=['photo', 'text'])
async def get_post_info(message: types.Message, state: FSMContext):
    post_text = message.text
    post_photo = ''
    if post_text is None:
        post_text = message.caption
        if message.caption is None:
            post_text = ''
        post_photo = message.photo[0]
    post_text = make_parsable(post_text)

    await AdminMassPost.waiting_for_approvement.set()
    print(message)
    print(post_text)
    await state.update_data(waiting_for_post=post_text, post_photo=post_photo)

    await message.answer(fmt.bold('Пост для рассылки:'))

    if post_photo:
        await message.answer_photo(photo=post_photo.file_id, caption=post_text)
    else:
        await message.answer(post_text)
    await message.answer(fmt.bold('Разослать всем пользователям?'), reply_markup=await agree_keyboard())


async def send_message_with_exc(user, post_photo, post_text):
    try:
        if post_photo:
            await bot.send_photo(chat_id=user, photo=post_photo.file_id, caption=post_text)
        else:
            await bot.send_message(chat_id=user, text=post_text)
    except BotBlocked:
        await delete_user(user)


@dp.message_handler(Text(equals='Да'), state=AdminMassPost.waiting_for_approvement)
async def mass_post(message: types.Message, state: FSMContext):
    post_data = await state.get_data()
    post_text = post_data.get('waiting_for_post')
    post_photo = post_data.get('post_photo')
    all_users = await get_all_users()
    await state.finish()
    await message.answer(fmt.bold('Рассылка началась'))
    for user in all_users:
        if user:
            await send_message_with_exc(user, post_photo, post_text)

    await message.answer(fmt.bold('Рассылка прошла успешно'))

    await message.answer(fmt.bold('Что требуется?'), reply_markup=await admin_keyboard())
    await VerUser.is_verified.set()


@dp.message_handler(Text(equals='Нет'), state=AdminMassPost.waiting_for_approvement)
async def cancel_post(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer(fmt.bold('Что требуется?'), reply_markup=await admin_keyboard())
    await VerUser.is_verified.set()
