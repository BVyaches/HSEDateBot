from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
import aiogram.utils.markdown as fmt
from keyboards import *
from handlers.states import VerUser
from SQL_funcs import *


async def start_bot(message: types.Message, state: FSMContext):
    await state.finish()
    user_data = await get_user_data(message.from_user.id)
    if not user_data:
        await VerUser.not_verified.set()
        await message.answer(fmt.bold('Новые знакомства - это совершать глупости вместе🌝\nПоздравляем! '
                                      'Ты попал, куда нужно😏\n'
                                      'LovePerm - это бот для поиска твоей судьбы среди студентов Перми❤\n'
                                      'Вступай в группу Fenix: t.me/hse_phoenix ️\n\n'
                                      'P.S. Включи пересылку сообщений в настройках конфиденциальности, '
                                      'чтобы можно было октрывать чат с другими людьми!\n'
                                      'Заходи в Настройки➡️Конфиденциальность➡️Пересылка сообщений🔜Все'))
        await message.answer(fmt.bold('Начнём?😏'), reply_markup=await start_keyboard())
    else:
        await VerUser.is_verified.set()
        await message.answer(fmt.bold('Похоже, ты уже зарегистрирован! Чем займемся?'),
                             reply_markup=await main_menu_keyboard())


def register_handlers_common(dp: Dispatcher):
    dp.register_message_handler(start_bot, commands='start', state='*')
