from aiogram import types


async def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Давай попробуем😼'] # Здесь была 'Регистрация'. Заменил по требованию заказчика
    keyboard.add(*buttons)
    return keyboard


async def gender_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['🧑🏻‍Парень', '👩🏻‍🦱Девушка'] # 🧑🏻‍Парень, 👩🏻‍🦱Девушка Добавил смайлики в кнопки. Надеюсь ничего не сломает (Виталий)
    keyboard.add(*buttons)
    return keyboard


async def email_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Ввести другой email'] # Здесь ничего не менял
    keyboard.add(*buttons)
    return keyboard


async def main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Смотреть анкеты', 'Отправить анонимное послание', 'Моя анкета']
    keyboard.add(*buttons)
    return keyboard


async def profile_view_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Лайк', 'Следующий', 'Жалоба', 'Меню']
    keyboard.add(*buttons)
    return keyboard


async def response_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Взаимно",
                                          callback_data=f"Love{user_id}"),
               types.InlineKeyboardButton(text='Мимо', callback_data='No')]
    keyboard.add(*buttons)
    return keyboard


async def is_responsed():
    keyboard = types.InlineKeyboardMarkup()
    buttons = [types.InlineKeyboardButton(text="Принято",
                                          callback_data=f"Sended"), ]
    keyboard.add(*buttons)
    return keyboard


async def user_profile_view():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True,
                                         one_time_keyboard=True)
    buttons = ['Заполнить заново', 'Поменять текст', 'Выключить анкету', 'Меню']
    keyboard.add(*buttons)
    return keyboard