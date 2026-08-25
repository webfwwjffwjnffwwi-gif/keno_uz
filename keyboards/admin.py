from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_admin_panel_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users"),
            InlineKeyboardButton(text="📢 Xabar yuborish", callback_data="admin_broadcast")
        ],
        [
            InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
            InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="admin_settings")
        ],
        [
            InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_to_main")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)