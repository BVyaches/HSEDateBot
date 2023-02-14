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
admin_ids = list(map(int, config.get('CHAT_IDs', 'admin_ids').split(',')))


async def start_love_letter(message: types.Message, state: FSMContext):
    await message.answer(fmt.bold('Данная функция позволяет отправить письмо любви в группу https://t.me/HSELoveGroup\n'
                                  'Продолжим?'),
                         reply_markup=await back_to_menu())
    await LoveLetter.waiting_for_decision.set()


async def ask_for_letter(message: types.Message):
    await message.answer(
        fmt.bold('Сейчас отправь сообщение, которое хочешь опубликовать в группе. '
                 'Если хочешь отправить фото - прикрепи его и подпись к нему'),
        reply_markup=types.ReplyKeyboardRemove())
    await LoveLetter.waiting_for_letter.set()


async def create_love_letter(message: types.Message, state: FSMContext):
    letter_text = message.text
    letter_photo = ''
    if letter_text is None:
        letter_text = message.caption
        if message.caption is None:
            letter_text = ''
        letter_photo = message.photo[0]
    await LoveLetter.waiting_for_category.set()
    letter_text = make_parsable(letter_text)
    await state.update_data(waiting_for_letter=letter_text, letter_photo=letter_photo)
    await message.answer(fmt.bold('Выбери, как хочешь опубликовать письмо:'),
                         reply_markup=await post_category_keyboard())


async def set_category(message: types.Message, state: FSMContext):
    category = message.text
    if category not in ['Анонимно', 'С ником']:
        await message.answer(fmt.bold('Пожалуйста, выбери один пункт из меню'))
        return True

    await message.answer(fmt.bold('Письмо для отправки:'))
    letter_data = await state.get_data()
    letter_text = letter_data.get('waiting_for_letter')
    letter_photo = letter_data.get('letter_photo')
    final_text = letter_text
    if category == 'С ником':
        final_text += f'\n\n' + f'[Написать автору](tg://user?id={message.from_user.id})'
    await state.update_data(waiting_for_letter=final_text)
    if letter_photo:
        await message.answer_photo(photo=letter_photo.file_id, caption=final_text)
    else:
        await message.answer(final_text)
    await message.answer(fmt.bold('Всё верно?'), reply_markup=await agree_keyboard())
    await LoveLetter.waiting_for_approvement.set()


async def send_letter(message: types.Message, state: FSMContext):
    approvement = message.text
    if approvement not in ['Да', 'Нет']:
        await message.answer(fmt.bold('Пожалуйста, выбери один пункт из меню'))
        return True

    if approvement == 'Да':
        letter_data = await state.get_data()
        letter_text = letter_data.get('waiting_for_letter')
        letter_photo = letter_data.get('letter_photo')
        if letter_photo:
            for i in admin_ids:
                await bot.send_photo(chat_id=i, photo=letter_photo.file_id, caption=letter_text,
                                     reply_markup=await post_letter_keyboard())
        else:
            for i in admin_ids:
                await bot.send_message(chat_id=i, text=letter_text,
                                       reply_markup=await post_letter_keyboard())
        await message.answer(fmt.bold('Письмо скоро будет опубликовано сразу после одобрения модераторами!'),
                             reply_markup=await main_menu_keyboard())
        await state.finish()
        await VerUser.is_verified.set()
    else:
        await state.finish()
        await start_love_letter(message, state)


async def post_letter(call: types.CallbackQuery):
    print(call)
    letter_photo = ''
    letter_text = call.message.text
    if letter_text is None:
        letter_text = call.message.caption
        letter_photo = call.message.photo[0]
    letter_text = make_parsable(letter_text)
    data = {}
    if 'Написать автору' in letter_text:
        try:
            data = eval(str(call.message.entities[0]).replace('false', 'False'))
        except IndexError:
            try:
                data = eval(str(call.message.caption_entities[0]).replace('false', 'False'))
            except IndexError:
                data = {}
    if data:
        print(data)
        user_id = data.get('user').get('id')

        letter_text = letter_text.replace('Написать автору',
                                              f'[Написать автору](tg://user?id={user_id})')
    if letter_photo:
        await bot.send_photo(chat_id=group_id, photo=letter_photo.file_id, caption=letter_text)
    else:
        await bot.send_message(chat_id=group_id, text=letter_text)
    await call.message.edit_reply_markup(reply_markup=await pass_keyboard())
    await call.message.answer(fmt.bold('Письмо успешно опубликовано'))


def register_handler_anon_post(dp: Dispatcher):
    dp.register_message_handler(start_love_letter, Text(equals='Письмо любви'),
                                state=VerUser.is_verified)
    dp.register_message_handler(ask_for_letter, Text(equals='Да!'), state=LoveLetter.waiting_for_decision)
    dp.register_message_handler(create_love_letter, state=LoveLetter.waiting_for_letter,
                                content_types=['photo', 'text'])
    dp.register_message_handler(set_category, state=LoveLetter.waiting_for_category)
    dp.register_message_handler(send_letter, state=LoveLetter.waiting_for_approvement)
    dp.register_callback_query_handler(post_letter, Text(startswith='POST'), state='*')
