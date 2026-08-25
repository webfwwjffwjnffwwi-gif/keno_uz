from telegram import Update
from telegram.ext import ContextTypes
from services.subscription import check_user_subscriptions
from keyboards.user import get_main_menu_keyboard

async def check_sub_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    is_subscribed = await check_user_subscriptions(context.bot, user_id)
    
    if is_subscribed:
        await query.message.delete()
        await query.message.reply_text(
            "✅ Obuna tasdiqlandi! Xush kelibsiz.",
            reply_markup=get_main_menu_keyboard()
        )
    else:
        await query.answer("❌ Siz hali hamma kanallarga obuna bo‘lmadingiz!", show_alert=True)