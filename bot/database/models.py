from sqlalchemy import Column, Integer, BigInteger, String, Float, DateTime, Boolean, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func
import datetime

class Base(DeclarativeBase):
    pass

class Household(Base):
    __tablename__ = "households"
    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True)
    creator_id = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now())
    email = Column(String(255), nullable=True, unique=True)
    google_id = Column(String(255), nullable=True, unique=True)
    password_hash = Column(String(255), nullable=True)

class SharedExpense(Base):
    __tablename__ = "shared_expenses"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    category = Column(String(50))
    amount = Column(Float)
    frequency = Column(String(20))
    created_at = Column(DateTime, server_default=func.now())

class Chore(Base):
    __tablename__ = "chores"
    id = Column(Integer, primary_key=True)
    household_id = Column(Integer, ForeignKey("households.id"))
    name = Column(String(100))
    assigned_to = Column(BigInteger)
    due_date = Column(DateTime)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    telegram_id = Column(BigInteger, primary_key=True)
    language = Column(String(10), default="he")
    role = Column(String(20), default="user")
    points = Column(Float, default=0.0)
    wallet_address = Column(String(255), nullable=True)
    last_gift_date = Column(String)
    gift_shares_today = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())

class CommandLog(Base):
    __tablename__ = "command_logs"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    command = Column(String)
    params = Column(String)
    timestamp = Column(DateTime, server_default=func.now())

class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    referrer_id = Column(BigInteger)
    referred_id = Column(BigInteger)
    created_at = Column(DateTime, server_default=func.now())

class UserExpense(Base):
    __tablename__ = "user_expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    amount = Column(Float)
    category = Column(String(50))
    frequency = Column(String(20))
    potential_ton_savings = Column(Float, default=0.0)
    notes = Column(String(200))
    created_at = Column(DateTime, server_default=func.now())

class UserMemory(Base):
    __tablename__ = "user_memory"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    last_command = Column(String(50))
    last_params = Column(String(200))
    last_result = Column(String(500))
    updated_at = Column(DateTime, server_default=func.now())

class AdminRequest(Base):
    __tablename__ = "admin_requests"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, server_default=func.now())

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)

class PensionProfile(Base):
    __tablename__ = "pension_profiles"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    language = Column(String(5), default="he")
    country = Column(String(5), default="IL")
    result_capital = Column(Float)
    result_monthly = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

class BotGroup(Base):
    __tablename__ = "bot_groups"
    id = Column(Integer, primary_key=True)
    group_id = Column(BigInteger, unique=True)
    group_name = Column(String(200))
    welcome_message = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class UserRole(Base):
    __tablename__ = "user_roles"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    role = Column(String(50), default="citizen")

class Course(Base):
    __tablename__ = "courses"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    required_role = Column(String(50), default="citizen")
    order_num = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

class UserProgress(Base):
    __tablename__ = "user_progress"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger)
    course_id = Column(Integer, ForeignKey("courses.id"))
    completed_lessons = Column(Text, default="[]")
    score = Column(Integer, default=0)
    last_accessed = Column(DateTime, server_default=func.now())

class Event(Base):
    __tablename__ = "events"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, index=True)
    type = Column(String(50))
    payload = Column(Text)
    timestamp = Column(DateTime, server_default=func.now())

class KnowledgeNode(Base):
    __tablename__ = "knowledge_nodes"
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    description = Column(Text)
    difficulty = Column(Integer, default=1)
    estimated_minutes = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())

class KnowledgeEdge(Base):
    __tablename__ = "knowledge_edges"
    id = Column(Integer, primary_key=True)
    from_node_id = Column(Integer, ForeignKey("knowledge_nodes.id"))
    to_node_id = Column(Integer, ForeignKey("knowledge_nodes.id"))
    relation_type = Column(String(50), nullable=False)
    weight = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    __table_args__ = (UniqueConstraint('from_node_id', 'to_node_id', 'relation_type'),)

class UserKnowledgeProgress(Base):
    __tablename__ = "user_knowledge_progress"
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger)
    node_id = Column(Integer, ForeignKey("knowledge_nodes.id"))
    status = Column(String(20), default="not_started")
    score = Column(Integer, default=0)
    completed_at = Column(DateTime)
    last_accessed = Column(DateTime, server_default=func.now())
    __table_args__ = (UniqueConstraint('telegram_id', 'node_id'),)

class Donation(Base):
    __tablename__ = "donations"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, index=True)
    amount = Column(Float)
    created_at = Column(DateTime, server_default=func.now())

class GameStats(Base):
    __tablename__ = "game_stats"
    user_id = Column(Integer, primary_key=True)
    slots_points = Column(Integer, default=0)
    slots_spins_total = Column(Integer, default=0)
    slots_daily_spins = Column(Integer, default=0)
    slots_last_spin_at = Column(DateTime, nullable=True)

class Expense(Base):
    __tablename__ = "expenses"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    amount = Column(Float)
    category = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    receipt_url = Column(String(500), nullable=True)   # URL לתמונה שמורה (עתידי)

class Income(Base):
    __tablename__ = "incomes"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    amount = Column(Float)
    category = Column(String(50))
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now())

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, index=True)
    name = Column(String(50))
    type = Column(String(10))    # 'expense' or 'income'
    created_at = Column(DateTime, server_default=func.now())
