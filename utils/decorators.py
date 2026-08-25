from functools import wraps

from db import SessionLocal
from services.admin import is_admin


def admin_only(handler):

    @wraps(handler)
    async def wrapper(
        update,
        context,
        *args,
        **kwargs,
    ):

        user = update.effective_user

        if not user:
            return

        async with SessionLocal() as session:

            allowed = await is_admin(
                session,
                user.id,
            )

        if not allowed:

            if update.callback_query:
                await update.callback_query.answer(
                    "❌ Siz admin emassiz.",
                    show_alert=True,
                )

            elif update.message:
                await update.message.reply_text(
                    "❌ Sizda admin huquqi yo‘q."
                )

            return

        return await handler(
            update,
            context,
            *args,
            **kwargs,
        )

    return wrapper