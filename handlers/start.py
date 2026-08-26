import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.users import upsert_user
from services.subscription import check_user_subscriptions, get_active_subscriptions
from keyboards.user import get_main_menu_keyboard
from keyboards.subscription import get_subscription_keyboard

logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    try:
        # 1. Bazaga foydalanuvchini yozish yoki yangilash
        await upsert_user(user.id, user.username, user.first_name, user.last_name)
    except Exception as e:
        logger.error(f"Foydalanuvchini bazaga yozishda xatolik (ID: {user.id}): {e}")

    try:
        # 2. Majburiy obunani tekshirish
        is_subscribed = await check_user_subscriptions(context.bot, user.id)
    except Exception as e:
        logger.error(f"Obunani tekshirishda xatolik: {e}")
        is_subscribed = True  # agar xatolik bo'lsa, foydalanuvchini to'xtatib qo'ymaslik uchun True deb olamiz
    try:
        if not is_subscribed:
            subs = await get_active_subscriptions()
            await update.message.reply_text(
                "📢 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                reply_markup=get_subscription_keyboard(subs)
            )
        else:
            await update.message.reply_text(
                f"Salom, {user.first_name}! Xush kelibsiz.",
                reply_markup=get_main_menu_keyboard()
            )
    except Exception as e:
        logger.error(f"Start xabarini yuborishda xatolik: {e}")