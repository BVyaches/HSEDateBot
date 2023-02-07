from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards import *


async def start_bot(message: types.Message):
    await message.answer('Любовь-это совершать глупости вместе🌝\nПоздравляем! Ты попал, куда нужно😏\nHSE_Love_Perm - это бот для поиска твоей судьбы в НИУ ВШЭ-Пермь❤️')
    await message.answer('Начнём?😏', reply_markup=await start_keyboard())



def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
