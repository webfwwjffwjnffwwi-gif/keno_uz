import logging
import sys
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import BOT_TOKEN
from db import init_db
from handlers.start import start_command
from handlers.subscription import check_sub_callback
from handlers.user import handle_text_messages

# Loggingni sozlash
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# ==========================================
# RENDER WEB SERVICE UCHUN PORT FIX (Server o'chib qolmasligi uchun)
# ==========================================
PORT = int(os.environ.get("PORT", 8080))

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Keno Uz Bot is active and running successfully!")

    def log_message(self, format, *args):
        pass

def run_health_server():
    try:
        server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
        logger.info(f"Health check veb-server {PORT}-portda ishga tushdi.")
        server.serve_forever()
    except Exception as e:
        logger.error(f"Veb-serverni ishga tushirishda xatolik: {e}")

# Veb-serverni alohida oqimda (thread) ishga tushiramiz ki bot bilan birga ishlayversin
server_thread = threading.Thread(target=run_health_server, daemon=True)
server_thread.start()
# ==========================================

async def post_init(application: Application):
    """Bot ishga tushganda bazani ishga tushirish"""
    try:
        await init_db()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli ulandi va jadvallar yaratildi.")
    except Exception as e:
        logger.error(f"Bazani ishga tushirishda xatolik: {e}")
        
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Xatoliklarni ushlab qolish va logga yozish"""
    logger.error(msg="Xatolik yuz berdi:", exc_info=context.error)

def main():
    if not BOT_TOKEN:
        logger.error("XATOLIK: BOT_TOKEN topilmadi! .env yoki Render environment variables tekshiring.")
        return

    # Botni yaratish
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # --- HANDLERLAR (Buyruqlar va tugmalar) ---
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CallbackQueryHandler(check_sub_callback, pattern="^check_subscription$"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text_messages))

    # Xatoliklarni boshqaruvchi
    application.add_error_handler(error_handler)

    # Botni ishga tushirish
    logger.info("Keno Uz boti ishga tushdi va xabarlarni qabul qilmoqda...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()