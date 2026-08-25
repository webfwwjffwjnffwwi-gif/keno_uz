from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def get_main_menu_keyboard():
    keyboard = [
        [KeyboardButton(text="🎯 KENO"), KeyboardButton(text="👤 Profil")],
        [KeyboardButton(text="🏆 Reyting"), KeyboardButton(text="💰 Balans")],
        [KeyboardButton(text="📊 Statistika"), KeyboardButton(text="ℹ️ Yordam")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def get_profile_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="💰 Balansni to'ldirish", callback_data="top_up_balance"),
            InlineKeyboardButton(text="📋 Tarix", callback_data="history")
        ],
        [
            InlineKeyboardButton(text="🏆 Reyting", callback_data="leaderboard"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)