import configparser
import types
import aiogram.utils.markdown as fmt
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from SQL_funcs import *
from formats import showing_user, show_love_user
from handlers.states import VerUser, ProfileViewer, Complaint, BanUser, LoveLetter
from initialization import bot, dp
from keyboards import *

config = configparser.ConfigParser()
config.read('config.ini')
group_id = int(config.get('CHAT_IDs', 'group_id'))


async def start_love_letter(message: types.Message, state: FSMContext):
    await message.answer('Данная функция позволяет отправить письмо любви в группу https://t.me/HSELoveGroup\n'
                         'Продолжим?',
                         reply_markup=await back_to_menu())
    await LoveLetter.waiting_for_decision.set()


async def ask_for_letter(message: types.Message):
    await message.answer(
        'Сейчас отправь сообщение, которое хочешь опубликовать в группе. '
        'Если хочешь отправить фото - прикрепи его и подпись к нему', reply_markup=types.ReplyKeyboardRemove())
    await LoveLetter.waiting_for_letter.set()


async def create_love_letter(message: types.Message, state: FSMContext):
    letter_text = message.text
    if letter_text is None:
        letter_text = message.caption
    letter_photo = message.photo
    print(message)
    print(letter_text)
    await state.update_data(waiting_for_letter=letter_text, letter_photo=letter_photo)
    await message.answer('Выбери, как хочешь опубликовать письмо:', reply_markup=await post_category_keyboard())
    await LoveLetter.waiting_for_category.set()


async def set_category(message: types.Message, state: FSMContext):
    category = message.text
    if category not in ['Анонимно', 'С ником']:
        await message.answer('Пожалуйста, выбери один пункт из меню')
        return True

    await message.answer('Письмо для отправки:')
    letter_data = await state.get_data()
    letter_text = letter_data.get('waiting_for_letter')
    print(letter_text)
    letter_photo = letter_data.get('letter_photo')
    final_text = letter_text
    if category == 'С ником':
        final_text += f'\n\n<a href="tg://user?id={message.from_user.id}">Написать автору</a>'
    await state.update_data(waiting_for_letter=final_text)
    if letter_photo:
        await message.answer_photo(photo=letter_photo[0].file_id, caption=final_text, parse_mode='html')
    else:
        await message.answer(final_text, parse_mode='html')
    await message.answer('Всё верно?', reply_markup=await agree_keyboard())
    await LoveLetter.waiting_for_approvement.set()


async def send_letter(message: types.Message, state: FSMContext):
    approvement = message.text
    if approvement not in ['Да', 'Нет']:
        await message.answer('Пожалуйста, выбери один пункт из меню')
        return True

    if approvement == 'Да':
        letter_data = await state.get_data()
        letter_text = letter_data.get('waiting_for_letter')
        letter_photo = letter_data.get('letter_photo')
        if letter_photo:
            await bot.send_photo(chat_id=group_id, photo=letter_photo[0].file_id, caption=letter_text,
                                 parse_mode='html')
        else:
            await bot.send_message(chat_id=group_id, text=letter_text, parse_mode='html')
        await message.answer('Письмо успешно отправлено!', reply_markup=await main_menu_keyboard())
        await state.finish()
        await VerUser.is_verified.set()
    else:
        await state.finish()
        await start_love_letter(message, state)


def register_handler_anon_post(dp: Dispatcher):
    dp.register_message_handler(start_love_letter, Text(equals='Письмо любви'),
                                state=VerUser.is_verified)
    dp.register_message_handler(ask_for_letter, Text(equals='Да!'), state=LoveLetter.waiting_for_decision)
    dp.register_message_handler(create_love_letter, state=LoveLetter.waiting_for_letter,
                                content_types=['photo', 'text'])
    dp.register_message_handler(set_category, state=LoveLetter.waiting_for_category)
    dp.register_message_handler(send_letter, state=LoveLetter.waiting_for_approvement)
