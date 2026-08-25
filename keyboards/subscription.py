from telegram.inlinekeyboardbuilder import InlineKeyboardBuilder
from telegram import InlineKeyboardButton

def get_subscription_keyboard(subs: list):
    builder = InlineKeyboardBuilder()
    for sub in subs:
        url = f"https://t.me/{sub.channel_username.replace('@', '')}" if sub.platform == 'telegram' else sub.channel_username
        btn_text = f"📢 {sub.channel_username}"
        builder.row(InlineKeyboardButton(text=btn_text, url=url))
    
    builder.row(InlineKeyboardButton(text="🔄 Obunani tekshirish", callback_data="check_subscription"))
    return builder.as_markup()