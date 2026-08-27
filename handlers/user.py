# from telegram import Update
# from telegram.ext import ContextTypes
# from keyboards.user import get_profile_keyboard

# async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     text = update.message.text
    
#     if text == "👤 Profil":
#         user = update.effective_user
#         profile_text = (
#             f"👤 **PROFIL**\n\n"
#             f"🆔 ID: `{user.id}`\n"
#             f"👤 Username: @{user.username if user.username else 'mavjud emas'}\n\n"
#             f"💰 Balans: 0 so'm\n"
#             f"🎯 O'yinlar: 0\n"
#             f"🏆 G'alabalar: 0"
#         )
#         await update.message.reply_text(profile_text, reply_markup=get_profile_keyboard(), parse_mode="Markdown")
#     elif text == "ℹ️ Yordam":
#         await update.message.reply_text("ℹ️ Yordam olish uchun adminga murojaat qiling.")
#     elif text == "🎯 KENO":
#         await update.message.reply_text("🎯 KENO o'yini tez orada ishga tushadi!")
#     elif text == "💰 Balans":
#         await update.message.reply_text("💰 Sizning balansingiz: 0 so'm")
#     elif text == "🏆 Reyting":
#         await update.message.reply_text("🏆 Top o'yinchilar reytingi tez orada qo'shiladi.")
#     elif text == "📊 Statistika":
#         await update.message.reply_text("📊 Sizning statistikangiz bo'sh.")

import os
import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.music import download_audio_from_link

logger = logging.getLogger(__name__)

async def handle_text_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    # "🎵 Qo'shiq topish" tugmasi bosilganda
    if text == "🎵 Qo'shiq topish":
        await update.message.reply_text(
            "🎧 Marhamat, menga **YouTube** yoki **Instagram (Shorts)** havolasini yuboring (masalan: `https://youtu.be/...`), "
            "yoki qidirmoqchi bo'lgan **qo'shiq nomini** yozib yuboring. \n\n"
            "Men uni 3-5 soniya ichida topib beraman! ⚡",
            parse_mode="Markdown"
        )
        return

    # Agar foydalanuvchi havola (link) tashlasa
    if text.startswith("http://") or text.startswith("https://"):
        processing_msg = await update.message.reply_text("⏳ Audio qidirilmoqda va yuklanmoqda, biroz kuting...")
        
        try:
            # Musiqani yuklab olish funksiyasini chaqiramiz
            audio_path = await download_audio_from_link(text)
            
            if audio_path and os.path.exists(audio_path):
                # Audioni foydalanuvchiga yuborish
                with open(audio_path, 'rb') as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        caption="🎵 **Keno Uz** boti orqali topildi!",
                        parse_mode="Markdown"
                    )
                # Yuborilgandan keyin serverdan faylni o'chirib tashlaymiz (joy tejash uchun)
                os.remove(audio_path)
                await processing_msg.delete()
            else:
                await processing_msg.edit_text("❌ Kechirasiz, bu havoladan audio topib bo'lmadi yoki xatolik yuz berdi.")
                
        except Exception as e:
            logger.error(f"Linkni qayta ishlashda xatolik: {e}")
            await processing_msg.edit_text("⚠️ Xatolik yuz berdi. Iltimos boshqa havola yuborib ko'ring.")
            
    else:
        # Agar oddiy matn (qo'shiq nomi) yozilgan bo'lsa
        await update.message.reply_text(
            f"🔍 '{text' bo'yicha qidiruv hozircha ishlab chiqilmoqda. Tez orada qo'shiq nomi bo'yicha ham qidirish qo'shiladi!\n\n"
            "Hozircha faqat YouTube yoki Instagram havolalarini yuborib, musiqasini 3-5 soniyada olishingiz mumkin. 🎧",
            parse_mode="Markdown"
        )