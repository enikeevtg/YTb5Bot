import asyncio

from aiogram import Router, F
from aiogram.types import ContentType, Message
import logging
from random import random

from handlers import messages
from utils import YouTubeScraper


logger = logging.getLogger(__name__)

router = Router()
scraper = YouTubeScraper()


@router.message(F.content_type == ContentType.TEXT)
async def request_handler(message: Message):
    logger.debug(f'{message.from_user.first_name} ' + \
                 f'{message.from_user.last_name} отправил запрос:\n' + \
                 f'{message.text}')
    result = await scraper.ytb_search_request(message.text)
    n = min(5, len(result))
    for i in range(n):
        await message.answer(text=result[i])
        logger.debug(f'{message.from_user.first_name} ' + \
                     f'{message.from_user.last_name}:\n' + \
                     f'{result[i]}')
        await asyncio.sleep(random())


@router.message(F.content_type != ContentType.TEXT)
async def other_messages_handler(message: Message):
    content_type = messages.content_types[str(message.content_type)]
    await message.answer(text=messages.incorrect_type.format(content_type))
