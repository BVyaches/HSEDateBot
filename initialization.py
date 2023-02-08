from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
# Place bot here to use it in various files
bot = Bot(token=config.get('BOT_TOKEN', 'Bot_token'))
dp = Dispatcher(bot, storage=MemoryStorage())
