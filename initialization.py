from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Place bot here to use it in various files
bot = Bot(token='6187865134:AAHE06t470l40uSFCvJptACntvh1uNMkjxo')
dp = Dispatcher(bot, storage=MemoryStorage())
