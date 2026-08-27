import os
import asyncio
import yt_dlp
import logging

logger = logging.getLogger(__name__)

async def download_audio_from_link(url: str) -> str | None:
    """
    YouTube, Instagram yoki boshqa platformalar linkidan audioni yuklab olib,
    fayl yo'lini (path) qaytaradi.
    """
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)
    
    # yt-dlp sozlamalari (faqat mp3/m4a audio tortish uchun)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(id)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'no_warnings': True,
    }

    def download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                # Kengaytmani mp3 ga o'zgartiramiz chunki FFmpeg uni mp3 qiladi
                base, _ = os.path.splitext(filename)
                mp3_file = base + ".mp3"
                return mp3_file
        except Exception as e:
            logger.error(f"Audio yuklashda xatolik ({url}): {e}")
            return None

    # Bloklovchi funksiyani alohida oqimda (thread) ishlatamiz (bot qotib qolmasligi uchun)
    loop = asyncio.get_running_loop()
    file_path = await loop.run_in_executor(None, download)
    return file_path