from telegram import InlineKeyboardButton, InlineKeyboardMarkup

def get_subscription_keyboard(channel_username: str = None):
    keyboard = []
    
    if channel_username:
        keyboard.append([
            InlineKeyboardButton(text="📢 Kanalga obuna bo'lish", url=f"https://t.me/{channel_username}")
        ])
    
    keyboard.append([
        InlineKeyboardButton(text="✅ Obunani tekshirish", callback_data="check_subscription")
    ])
    
    return InlineKeyboardMarkup(keyboard)