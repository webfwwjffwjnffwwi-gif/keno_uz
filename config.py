import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
# Admin idlarini ro'yxat ko'rinishida olish
ADMIN_IDS = [int(admin_id.strip()) for admin_id in os.getenv("ADMIN_IDS", "").split(",") if admin_id.strip()]
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME", "@kanal_username") # Majburiy obuna kanali