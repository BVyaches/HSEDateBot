import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from SQL_funcs import *
from handlers.common import register_handlers_common
from handlers.find_pair import register_handler_find_pair

bot = Bot(token='6187865134:AAHE06t470l40uSFCvJptACntvh1uNMkjxo')
dp = Dispatcher(bot, storage=MemoryStorage())


async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers_common(dp)
    register_handler_find_pair(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
