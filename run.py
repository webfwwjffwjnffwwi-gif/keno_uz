import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgresql://anime_db_n2d3_user:0MTajYZoT0ai3AXU7iyTcdsaLnF4oTEl@dpg-da3dvtajnfac73cagpj0-a.oregon-postgres.render.com/anime_db_n2d3')
    await conn.execute('ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR;')
    await conn.close()
    print("Bajarildi! full_name ustuni qo'shildi.")

asyncio.run(main())
