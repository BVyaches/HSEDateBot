import logging
import asyncio

from initialization import dp

from SQL_funcs import *
from handlers.common import register_handlers_common

from handlers.finding_pair import register_handler_finding_pair
import handlers.anon_post
import handlers.register
import handlers.admin_panel


async def main():
    logging.basicConfig(level=logging.INFO)
    register_handlers_common(dp)
    register_handler_finding_pair(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
