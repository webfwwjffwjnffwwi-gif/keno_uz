import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, BigInteger, DateTime
from datetime import datetime
from dotenv import load_dotenv

from .database import engine, Base, async_session, User, init_db

load_dotenv()

# Render yoki .env dagi PostgreSQL URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Agar DATABASE_URL postgres:// bilan boshlansa, postgresql+asyncpg:// ga o'zgartiramiz (Render uchun muhim)
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

# Asinxron dvigatel (engine)
engine = create_async_engine(DATABASE_URL, echo=False)

# Sessiya fabrikasi
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# Foydalanuvchilar jadvali (User modeli)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    full_name = Column(String, nullable=True)
    username = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

async def init_db():
    """Jadvallarni bazada yaratish"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)