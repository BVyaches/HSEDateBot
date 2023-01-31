from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *


async def start_bot(message: types.Message):
    await message.answer('Это бот для знакомств вышки. Пока тестовый')
    await message.answer('Познакомимся?', reply_markup=await start_keyboard())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
