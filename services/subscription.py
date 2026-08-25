from sqlalchemy.future import select
from db import async_session
from database.models import MandatorySubscription
from telegram import Bot

async def get_active_subscriptions():
    async with async_session() as session:
        result = await session.execute(select(MandatorySubscription).where(MandatorySubscription.is_active == True))
        return result.scalars().all()

async def check_user_subscriptions(bot: Bot, user_id: int) -> bool:
    subs = await get_active_subscriptions()
    for sub in subs:
        if sub.platform == 'telegram':
            try:
                chat_member = await bot.get_chat_member(chat_id=sub.channel_username, user_id=user_id)
                if chat_member.status in ['left', 'kicked']:
                    return False
            except Exception:
                return False
    return True