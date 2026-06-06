from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    language = Column(String(2), default="he")
    is_business = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CommandLog(Base):
    __tablename__ = "command_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    command = Column(String)
    params = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    code = Column(String, unique=True)
    inviter_id = Column(BigInteger)
    clicks = Column(Integer, default=0)

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    monthly_income = Column(Float, default=0.0)
    family_size = Column(Integer, default=1)
    city = Column(String(100))
    opt_in_data = Column(Boolean, default=False)

class UserExpense(Base):
    __tablename__ = "user_expenses"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    category = Column(String(50))
    amount = Column(Float)
    frequency = Column(String(20))
    potential_ton_savings = Column(Float, default=0.0)
    notes = Column(String(200))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

