import logging

from telegram import Update
from telegram.ext import ContextTypes


logger = logging.getLogger(__name__)


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
) -> None:

    logger.exception(
        "Telegram handler xatosi:",
        exc_info=context.error,
    )

    if isinstance(update, Update):

        try:

            if update.effective_message:

                await update.effective_message.reply_text(
                    "⚠️ Kutilmagan xatolik yuz berdi.\n"
                    "Iltimos, birozdan keyin qayta urinib ko‘ring."
                )

        except Exception:

            logger.exception(
                "Xatolik haqida foydalanuvchiga xabar yuborib bo‘lmadi."
            )