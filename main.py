import logging
from initialization import bot, dp

from SQL_funcs import *
from handlers.common import register_handlers_common
from handlers.find_pair import register_handler_find_pair




async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers_common(dp)
    register_handler_find_pair(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
