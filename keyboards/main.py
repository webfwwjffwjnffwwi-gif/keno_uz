from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:

    keyboard = [
        [
            InlineKeyboardButton(
                "🎯 KENO",
                callback_data="menu_keno",
            ),
            InlineKeyboardButton(
                "👤 Profil",
                callback_data="menu_profile",
            ),
        ],
        [
            InlineKeyboardButton(
                "🏆 Reyting",
                callback_data="menu_rating",
            ),
            InlineKeyboardButton(
                "💰 Balans",
                callback_data="menu_balance",
            ),
        ],
        [
            InlineKeyboardButton(
                "📊 Statistika",
                callback_data="menu_statistics",
            ),
            InlineKeyboardButton(
                "ℹ️ Yordam",
                callback_data="menu_help",
            ),
        ],
    ]

    return InlineKeyboardMarkup(keyboard)