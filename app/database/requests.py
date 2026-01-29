from database.models import async_session
from database.models import User
from sqlalchemy import select


async def set_user(from_user) -> None:
    async with async_session() as session:
        user = await get_user(session, from_user.id)

        if not user:
            session.add(User(
                tg_id = from_user.id,
                username = from_user.username,
                first_name = from_user.first_name,
                last_name = from_user.last_name
            ))
            await session.commit()


async def get_user(session, tg_id):
    return await session.scalar(select(User).where(User.tg_id == tg_id))
