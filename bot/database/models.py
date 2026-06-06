from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, index=True)
    language = Column(String(2), default="he")
    is_business = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CommandLog(Base):
    __tablename__ = "command_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    command = Column(String)
    params = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    inviter_id = Column(Integer)
    clicks = Column(Integer, default=0)
