from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from database import async_session, User
from sqlalchemy import select

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    # Bazaga foydalanuvchini saqlash
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            new_user = User(telegram_id=user.id, full_name=user.full_name, username=user.username)
            session.add(new_user)
            await session.commit()

    # Instagram sahifasiga o'tish va tekshirish tugmalari
    keyboard = [
        [InlineKeyboardButton("📸 Instagram sahifamizga o'tish", url="https://instagram.com/aneblok_n1")],
        [InlineKeyboardButton("✅ Obuna bo'ldim", callback_data="check_insta_sub")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Assalomu alaykum, {user.first_name}!\n\n"
        f"Botdan foydalanish uchun avval Instagram sahifamizga obuna bo'ling va so'ng **"✅ Obuna bo'ldim"** tugmasini bosing:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def check_insta_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Asosiy menyu tugmalari
    keyboard = [
        [KeyboardButton("🎵 Qo'shiq topish"), KeyboardButton("📢 Reklama berish")],
        [KeyboardButton("👤 Profil"), KeyboardButton("ℹ️ Yordam")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await query.message.reply_text(
        "Rahmat! Endi kerakli bo'limni tanlashingiz yoki YouTube / Instagram havolasini yuborishingiz mumkin 🎧",
        reply_markup=reply_markup
    )