import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.music import download_audio_from_link

logger = logging.getLogger(__name__)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # 🎵 Qo'shiq topish tugmasi
    if text == "🎵 Qo'shiq topish":
        await update.message.reply_text(
            "🎧 Marhamat, menga **YouTube** yoki **Instagram (Shorts)** havolasini yuboring (masalan: `https://youtu.be/...`), "
            "yoki qidirmoqchi bo'lgan qo'shiq nomini yozib yuboring.\n\n"
            "Men uni tezda topib beraman! ⚡",
            parse_mode="Markdown"
        )
        return

    # 📢 Reklama berish tugmasi
    if text == "📢 Reklama berish":
        ad_text = (
            "📢 **Botimizda reklama joylashtirish narxlari va turlari:**\n\n"
            "1️⃣ **1-tur (Oddiy post):** Kanal lentasida 24 soat turadi — **10,000 so'm**\n"
            "2️⃣ **2-tur (Top post):** Kanal lentasida 1-o'rinda 48 soat turadi va 1 soat tepada qadaladi — **25,000 so'm**\n"
            "3️⃣ **3-tur (VIP / Maxsus):** Bot start oynasida va kanalda doimiy turadi, notification yuboriladi — **40,000 so'm**\n\n"
            "👨‍💻 Reklama berish uchun admin bilan bog'laning:\n"
            "👉 **Admin lichkasi:** @Masariddin"
        )
        await update.message.reply_text(ad_text, parse_mode="Markdown")
        return

    # 👤 Profil tugmasi
    if text == "👤 Profil":
        user = update.effective_user
        await update.message.reply_text(
            f"👤 **Sizning profilingiz:**\n\n"
            f"🆔 ID: `{user.id}`\n"
            f"ism: {user.first_name}\n"
            f"Username: @{user.username if user.username else 'Mavjud emas'}",
            parse_mode="Markdown"
        )
        return

    # ℹ️ Yordam tugmasi
    if text == "ℹ️ Yordam":
        await update.message.reply_text(
            "ℹ️ **Yordam markazi:**\n\n"
            "Botdan foydalanish uchun YouTube yoki Instagram havolasini tashlang. "
            "Agar savollar bo'lsa, adminga murojaat qiling: @Masariddin",
            parse_mode="Markdown"
        )
        return

    # Havolalarni qayta ishlash (Musiqa yuklash)
    if text.startswith("http://") or text.startswith("https://"):
        processing_msg = await update.message.reply_text("⏳ Audio qidirilmoqda va yuklanmoqda, biroz kuting...")
        
        try:
            audio_path = await download_audio_from_link(text)
            
            if audio_path and os.path.exists(audio_path):
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        caption="🎵 **Keno Uz** boti orqali topildi!",
                        parse_mode="Markdown"
                    )
                os.remove(audio_path)
                await processing_msg.delete()
            else:
                await processing_msg.edit_text("❌ Kechirasiz, bu havoladan audio topib bo'lmadi.")
                
        except Exception as e:
            logger.error(f"Linkni qayta ishlashda xatolik: {e}")
            await processing_msg.edit_text("⚠️ Xatolik yuz berdi. Boshqa havola yuborib ko'ring.")
    else:
        await update.message.reply_text(
            "🔍 Tushunarli. Iltimos, musiqa topish uchun **YouTube** yoki **Instagram** havolasini yuboring yoki menyudan kerakli bo'limni tanlang. 🎧",
            parse_mode="Markdown"
        )