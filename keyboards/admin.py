from telegram.inlinekeyboardbuilder import InlineKeyboardBuilder
from telegram import InlineKeyboardButton

def get_admin_panel_keyboard():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="admin_stats"),
        InlineKeyboardButton(text="👥 Foydalanuvchilar", callback_data="admin_users")
    )
    builder.row(
        InlineKeyboardButton(text="📢 Majburiy obunalar", callback_data="admin_subscriptions"),
        InlineKeyboardButton(text="👑 Adminlar", callback_data="admin_list")
    )
    builder.row(
        InlineKeyboardButton(text="📨 Reklama / Broadcast", callback_data="admin_broadcast"),
        InlineKeyboardButton(text="📋 Loglar", callback_data="admin_logs")
    )
    builder.row(
        InlineKeyboardButton(text="🔙 Asosiy menyu", callback_data="back_to_main")
    )
    return builder.as_markup()