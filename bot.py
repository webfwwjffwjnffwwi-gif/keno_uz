import logging
import sys
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN
from db import init_db
from handlers.start import start_command
from handlers.admin import admin_command, admin_panel_callback
from handlers.subscription import check_sub_callback
from handlers.user import handle_text_messages

# Loggingni sozlash
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

async def post_init(application: Application):
    """Bot ishga tushganda bazani ishga tushirish"""
    try:
        await init_db()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli ulandi va jadvallar yaratildi.")
    except Exception as e:
        logger.error(لf"Bazani ishga tushirishda xatolik: {e}")

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Bot ichida qandaydir xatolik ketsa, uni ushlab logga yozish (bot jim qolishining oldini oladi)"""
    logger.error(msg="Xatolik yuz berdi:", exc_info=context.error)
    
    # Agar xatolik foydalanuvchiga tegishli bo'lsa, unga xabar berish mumkin
    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ Kechirasiz, tizimda vaqtinchalik xatolik yuz berdi. Iltimos, birozdan so'ng qayta urinib ko'ring."
            )
        except Exception:
            pass

def main():
    if not BOT_TOKEN:
        logger.error("XATOLIK: BOT_TOKEN topilmadi! .env yoki Render Environment Variables ni tekshiring.")
        return

    # Application qurish
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # --- HANDLERLARNI QO'SHISH ---
    
    # 1. Buyruqlar
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    # 2. Inline tugmalar (Callback queries)
    application.add_handler(CallbackQueryHandler(check_sub_callback, pattern="^check_subscription$"))
    application.add_handler(CallbackQueryHandler(admin_panel_callback, pattern="^(admin_|back_to_main)"))
    
    # 3. Oddiy matnli xabarlar
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    # Xatoliklarni boshqaruvchini ulash
    application.add_error_handler(error_handler)

    logger.info("Bot muvaffaqiyatli ishga tushdi va xabarlarni qabul qilmoqda...")
    
    # Botni ishga tushirish (Polling)
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()