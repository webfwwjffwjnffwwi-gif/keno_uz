import asyncio
import asyncpg

# Siz bergan bazaga ulanish havolasi
DATABASE_URL = "postgresql://anime_db_n2d3_user:0MTajYZoT0ai3AXU7iyTcdsaLnF4oTEl@dpg-da3dvtajnfac73cagpj0-a.oregon-postgres.render.com/anime_db_n2d3"

async def add_column():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        # Mavjud ma'lumotlarga ziyon yetkazmasdan ustun qo'shish
        await conn.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;")
        print("Muvaffaqiyatli qo'shildi: full_name ustuni yaratildi!")
    except Exception as e:
        print(f"Xatolik: {e}")
    finally:
        await conn.close()

asyncio.run(add_column())
