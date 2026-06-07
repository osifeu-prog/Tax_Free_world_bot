# -*- coding: utf-8 -*-
from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String, Float, DateTime, Boolean
from sqlalchemy.orm import DeclarativeBase
import datetime

class Base(DeclarativeBase):
    pass


class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True)
    creator_id = Column(BigInteger)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class HouseholdMember(Base):
    __tablename__ = "household_members"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    telegram_id = Column(BigInteger)

class SharedExpense(Base):
    __tablename__ = "shared_expenses"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    telegram_id = Column(BigInteger)
    category = Column(String(50))
    amount = Column(Float)
    frequency = Column(String(20))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Chore(Base):
    __tablename__ = "chores"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    assigned_to = Column(BigInteger)
    title = Column(String(200))
    done = Column(Boolean, default=False)

class ShoppingListItem(Base):
    __tablename__ = "shopping_items"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    added_by = Column(BigInteger)
    item = Column(String(200))
    bought = Column(Boolean, default=False)
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    language = Column(String(2), default="he")
    is_business = Column(Boolean, default=False)
    points = Column(Integer, default=0)
    last_gift_date = Column(String)
    gift_shares_today = Column(Integer, default=0)
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

class UserMemory(Base):
    __tablename__ = "user_memory"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    last_command = Column(String(50))
    last_params = Column(String(200))
    last_result = Column(String(500))
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)


class AdminRequest(Base):
    __tablename__ = "admin_requests"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    status = Column(String(20), default="pending")  # pending/approved/rejected
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    role = Column(String(50))
    password_hash = Column(String(200))


# bot/database/models.py (הוספה לסוף הקובץ)
class BotGroup(Base):
    __tablename__ = "bot_groups"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(BigInteger, unique=True, nullable=False)
    title = Column(String, nullable=True)

