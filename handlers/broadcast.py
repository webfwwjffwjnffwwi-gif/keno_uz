from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
)

from db import SessionLocal
from database.models import User


WAITING_BROADCAST = 100


async def broadcast_start_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    query = update.callback_query

    if not query:
        return ConversationHandler.END

    await query.answer()

    await query.edit_message_text(
        "📢 <b>BROADCAST</b>\n\n"
        "Barcha foydalanuvchilarga yuboriladigan "
        "xabarni yuboring.\n\n"
        "❌ Bekor qilish: /cancel",
        parse_mode="HTML",
    )

    return WAITING_BROADCAST


async def broadcast_message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    if not update.message:
        return WAITING_BROADCAST

    admin_message = update.message

    async with SessionLocal() as session:

        from sqlalchemy import select

        result = await session.execute(
            select(User).where(
                User.is_active.is_(True),
                User.is_blocked.is_(False),
            )
        )

        users = list(result.scalars().all())

    successful = 0
    failed = 0

    for user in users:

        try:

            await context.bot.copy_message(
                chat_id=user.telegram_id,
                from_chat_id=admin_message.chat_id,
                message_id=admin_message.message_id,
            )

            successful += 1

        except Exception:

            failed += 1

    await admin_message.reply_text(
        "📊 <b>Broadcast yakunlandi</b>\n\n"
        f"👥 Jami: <b>{len(users)}</b>\n"
        f"✅ Yuborildi: <b>{successful}</b>\n"
        f"❌ Xatolik: <b>{failed}</b>",
        parse_mode="HTML",
    )

    return ConversationHandler.END


async def broadcast_cancel_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
) -> int:

    if update.message:

        await update.message.reply_text(
            "❌ Broadcast bekor qilindi."
        )

    return ConversationHandler.END