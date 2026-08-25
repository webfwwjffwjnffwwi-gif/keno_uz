from telegram import Update
from telegram.ext import ContextTypes
from keyboards.user import get_profile_keyboard

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "👤 Profil":
        user = update.effective_user
        profile_text = (
            f"👤 **PROFIL**\n\n"
            f"🆔 ID: `{user.id}`\n"
            f"👤 Username: @{user.username if user.username else 'mavjud emas'}\n\n"
            f"💰 Balans: 0 so'm\n"
            f"🎯 O'yinlar: 0\n"
            f"🏆 G'alabalar: 0"
        )
        await update.message.reply_text(profile_text, reply_markup=get_profile_keyboard(), parse_mode="Markdown")
    elif text == "ℹ️ Yordam":
        await update.message.reply_text("ℹ️ Yordam olish uchun adminga murojaat qiling.")
    elif text == "🎯 KENO":
        await update.message.reply_text("🎯 KENO o'yini tez orada ishga tushadi!")
    elif text == "💰 Balans":
        await update.message.reply_text("💰 Sizning balansingiz: 0 so'm")
    elif text == "🏆 Reyting":
        await update.message.reply_text("🏆 Top o'yinchilar reytingi tez orada qo'shiladi.")
    elif text == "📊 Statistika":
        await update.message.reply_text("📊 Sizning statistikangiz bo'sh.")