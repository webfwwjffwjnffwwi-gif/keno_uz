from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_IDS
from keyboards.admin import get_admin_panel_keyboard

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMIN_IDS:
        await update.message.reply_text("⛔ Sizda bu buyruqni ishlatish uchun huquq yo'q.")
        return
    
    await update.message.reply_text(
        "👑 **ADMIN PANEL**\nKerakli bo'limni tanlang:",
        reply_markup=get_admin_panel_keyboard(),
        parse_mode="Markdown"
    )

async def admin_panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    if user_id not in ADMIN_IDS:
        await query.answer("⛔ Ruxsat yo'q!", show_alert=True)
        return
        
    await query.answer()
    data = query.data
    
    if data == "admin_stats":
        await query.edit_message_text("📊 Bot statistikasi bo'limi hozircha bo'sh.", reply_markup=get_admin_panel_keyboard())
    elif data == "admin_subscriptions":
        await query.edit_message_text("📢 Majburiy obunalar boshqaruvi.", reply_markup=get_admin_panel_keyboard())
    elif data == "back_to_main":
        await query.message.delete()
        await query.message.reply_text("Asosiy menyu:", reply_markup=get_main_menu_keyboard())