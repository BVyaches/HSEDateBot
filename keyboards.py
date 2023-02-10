from aiogram import types


async def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = [
        'Давай попробуем😼']  # Здесь была 'Регистрация'. Заменил по требованию заказчика
    keyboard.add(*buttons)
    return keyboard


async def gender_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['🧑🏻‍Парень',
               '👩🏻‍🦱Девушка']  # 🧑🏻‍Парень, 👩🏻‍🦱Девушка Добавил смайлики в кнопки. Надеюсь ничего не сломает (Виталий)
    keyboard.add(*buttons)
    return keyboard


async def email_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Ввести другой email']  # Здесь ничего не менял
    keyboard.add(*buttons)
    return keyboard


async def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Смотреть анкеты', 'Письмо любви', 'Моя анкета']
    keyboard.add(*buttons)
    return keyboard


async def profile_view_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['❤', '👎🏻', 'Жалоба', 'Меню📌']
    keyboard.add(*buttons)
    return keyboard


async def response_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="❤",
                                          callback_data=f"Love{user_id}"),
               types.InlineKeyboardButton(text='👎🏻', callback_data='No')]
    keyboard.add(*buttons)
    return keyboard


async def is_responsed():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Отправлено",
                                          callback_data=f"Sended"), ]
    keyboard.add(*buttons)
    return keyboard


async def user_profile_view_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Анкета с нуля✏', 'Изменить описание📝', 'Отключить анкету🔓', 'Меню📌']
    keyboard.add(*buttons)
    return keyboard


async def complaint_to_admin_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text='Забанить',
                                          callback_data=f'BAN {user_id}'),
               types.InlineKeyboardButton(text='Помиловать',
                                          callback_data='GOOD')]
    keyboard.add(*buttons)
    return keyboard


async def complaint_response_done_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text='Сделано',
                                          callback_data=f"SENDED"), ]
    keyboard.add(*buttons)
    return keyboard


async def start_from_ban_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['/start']
    keyboard.add(*buttons)
    return keyboard


async def agree_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Да', 'Нет']
    keyboard.add(*buttons)
    return keyboard


async def post_category_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Анонимно', 'С ником']
    keyboard.add(*buttons)
    return keyboard

async def back_to_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=False)
    buttons = ['Да!', 'Назад в меню📌']
    keyboard.add(*buttons)
    return keyboard
