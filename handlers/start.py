from aiogram import types # yoki telegram.ext (PTB versiyasiga qarab)
# Biz python-telegram-bot (v20+) ishlatayotganimiz uchun quyidagicha yozamiz:
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ContextTypes
from config import CHANNEL_USERNAME
from database import async_session, User
from sqlalchemy import select

async def check_user_subscription(bot, user_id: int) -> bool:
    """Foydalanuvchi kanalga obuna bo'lganini tekshiradi"""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
    except Exception:
        pass
    return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    bot = context.bot
    
    # Bazaga foydalanuvchini saqlash (Agar yo'q bo'lsa)
    async with async_session() as session:
        result = await session.execute(select(User).where(User.telegram_id == user.id))
        db_user = result.scalar_one_or_none()
        if not db_user:
            new_user = User(telegram_id=user.id, full_name=user.full_name, username=user.username)
            session.add(new_user)
            await session.commit()

    # Obunani tekshiramiz
    is_subscribed = await check_user_subscription(bot, user.id)
    
    if not is_subscribed:
        # Obuna bo'lmasa, kanalga o'tish tugmasini beramiz
        keyboard = [
            [InlineKeyboardButton("📢 Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton("✅ Obunani tekshirish", callback_data="check_subscription")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"👋 Assalomu alaykum, {user.first_name}!\n\n"
            f"Botdan foydalanish uchun quyidagi kanalimizga obuna bo'ling:",
            reply_markup=reply_markup
        )
    else:
        # Obuna bo'lgan bo'lsa, asosiy menyuni chiqarish
        await send_main_menu(update)

async def send_main_menu(update: Update):
    """Asosiy menyuni yuborish"""
    # Pastki (Reply) tugmalar menyusi
    keyboard = [
        [KeyboardButton("🎵 Qo'shiq topish")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    text = (
        "🤖 **Keno Uz** botiga xush kelibsiz!\n\n"
        "Qo'shiq qidirish uchun quyidagi tugmani bosing yoki YouTube/Instagram havolasini yuboring 🎧"
    )
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    elif update.callback_query:
        await update.callback_query.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")