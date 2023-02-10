import logging
import asyncio

from initialization import dp

from SQL_funcs import *
from handlers.common import register_handlers_common
from handlers.register import register_handler_register
from handlers.finding_pair import register_handler_finding_pair
from  handlers.anon_post import register_handler_anon_post

async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers_common(dp)
    register_handler_register(dp)
    register_handler_finding_pair(dp)
    register_handler_anon_post(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
