import asyncio

from aiogram import Bot, Dispatcher
from decouple import config
import logging

from handlers import start, text_request


async def main():
    bot = Bot(config('TOKEN'))
    dp = Dispatcher()

    dp.include_routers(start.router)
    dp.include_router(text_request.router)  # include last

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logfile = open('bot.log', 'w')
    format = "%(asctime)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s"
    logging.basicConfig(stream=logfile, level=logging.DEBUG, format=format)
    logger = logging.getLogger(__name__)

    asyncio.run(main())
