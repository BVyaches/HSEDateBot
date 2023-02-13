from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser
from aiogram import types

config = configparser.ConfigParser()
config.read('config.ini')
# Place bot here to use it in various files
bot = Bot(token=config.get('BOT_TOKEN', 'Bot_token'), parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=MemoryStorage())
