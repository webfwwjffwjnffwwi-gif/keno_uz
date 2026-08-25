from telegram import Update
from telegram.ext import ContextTypes
from services.users import upsert_user
from services.subscription import check_user_subscriptions, get_active_subscriptions
from keyboards.user import get_main_menu_keyboard
from keyboards.subscription import get_subscription_keyboard
from config import ADMIN_IDS

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Bazaga yozish
    await upsert_user(user.id, user.username, user.first_name, user.last_name)
    
    # Obunani tekshirish
    is_subscribed = await check_user_subscriptions(context.bot, user.id)
    
    if not is_subscribed:
        subs = await get_active_subscriptions()
        # Agar bazada obunalar bo'lmasa, default qo'shamiz yoki ko'rsatamiz
        await update.message.reply_text(
            "📢 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
            reply_markup=get_subscription_keyboard(subs)
        )
    else:
        await update.message.reply_text(
            f"Salom, {user.first_name}! Keno UZ botiga xush kelibsiz.",
            reply_markup=get_main_menu_keyboard()
        )