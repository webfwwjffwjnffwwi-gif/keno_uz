from sqlalchemy.future import select
from db import async_session
from database.models import User

async def upsert_user(user_id: int, username: str, first_name: str, last_name: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(User.id == user_id))
            user = result.scalar_one_or_none()
            
            if user:
                user.username = username
                user.first_name = first_name
                user.last_name = last_name
                user.is_blocked = False
            else:
                user = User(
                    id=user_id,
                    username=username,
                    first_name=first_name,
                    last_name=last_name
                )
                session.add(user)
            await session.commit()
            return user