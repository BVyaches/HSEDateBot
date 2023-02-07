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

