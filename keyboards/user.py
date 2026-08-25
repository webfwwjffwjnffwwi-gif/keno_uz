from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

def get_main_menu_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="🎯 KENO"),
        KeyboardButton(text="👤 Profil")
    )
    builder.row(
        KeyboardButton(text="🏆 Reyting"),
        KeyboardButton(text="💰 Balans")
    )
    builder.row(
        KeyboardButton(text="📊 Statistika"),
        KeyboardButton(text="ℹ️ Yordam")
    )
    return builder.as_markup(resize_keyboard=True)

def get_profile_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="💰 Balansni to'ldirish", callback_data="top_up_balance"),
        InlineKeyboardButton(text="📋 Tarix", callback_data="history")
    )
    builder.row(
        InlineKeyboardButton(text="🏆 Reyting", callback_data="leaderboard"),
        InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
    )
    return builder.as_markup()