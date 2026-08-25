import logging
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import BOT_TOKEN
from db import init_db
from handlers.start import start_command
from handlers.admin import admin_command, admin_panel_callback
from handlers.subscription import check_sub_callback
from handlers.user import handle_text_messages

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

async def post_init(application: Application):
    await init_db()
    logger.info("Database initialized successfully and tables created.")

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN topilmadi! .env faylini tekshiring.")
        return

    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_command))
    
    # Callbacks
    application.add_handler(CallbackQueryHandler(check_sub_callback, pattern="^check_subscription$"))
    application.add_handler(CallbackQueryHandler(admin_panel_callback, pattern="^(admin_|back_to_main)"))
    
    # Text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    logger.info("Bot ishga tushdi...")
    application.run_polling()

if __name__ == "__main__":
    main()