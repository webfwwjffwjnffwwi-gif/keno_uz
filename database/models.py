from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Boolean, DateTime, Float, ForeignKey, Text
from db import Base

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, index=True) # Telegram User ID
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    language = Column(String, default="uz")
    balance = Column(Float, default=0.0)
    is_blocked = Column(Boolean, default=False)
    last_activity = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)

class MandatorySubscription(Base):
    __tablename__ = "mandatory_subscriptions"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    channel_username = Column(String, unique=True, nullable=False) # Masalan: @username yoki https://t.me/...
    channel_title = Column(String, nullable=True)
    channel_id = Column(BigInteger, nullable=True)
    platform = Column(String, default="telegram") # telegram yoki instagram
    is_active = Column(Boolean, default=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    __table_args__ = {'extend_existing': True}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    admin_id = Column(BigInteger, nullable=False)
    action = Column(String, nullable=False)
    target = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)