from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from database import requests as rq
from handlers import messages


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await rq.set_user(message.from_user)
    await message.answer(text=messages.start
                                      .format(message.from_user.first_name))
