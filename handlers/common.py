from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *
from handlers.register import VerUser
from SQL_funcs import *


async def start_bot(message: types.Message, state: FSMContext):
    user_data = await get_user_data(message.from_user.id)
    if not user_data:
        await VerUser.not_verified.set()
        await message.answer('Это бот для знакомств вышки. Пока тестовый')
        await message.answer('Познакомимся?', reply_markup=await start_keyboard())
    else:
        await VerUser.is_verified.set()
        await message.answer('Похоже, ты уже зарегистрирован! Чем займемся?', reply_markup=await main_menu_keyboard())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
