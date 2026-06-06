from sqlalchemy import select
from bot.database.models import UserProfile, UserExpense
from bot.database.session import async_session

# מחשב חיסכון פוטנציאלי בהעברת תשלום ל-TON
def calc_savings(amount: float, frequency: str) -> float:
    # הנחה: עמלת ביט 1.5%, עמלת TON 0.1%
    fee_bit = amount * 0.015
    fee_ton = amount * 0.001
    saving_per_tx = fee_bit - fee_ton
    months = {"חודשי": 12, "דו-חודשי": 6, "שנתי": 1}
    return round(saving_per_tx * months.get(frequency, 12))

async def get_or_create_profile(telegram_id: int) -> UserProfile:
    async with async_session() as session:
        result = await session.execute(
            select(UserProfile).where(UserProfile.telegram_id == telegram_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = UserProfile(telegram_id=telegram_id)
            session.add(profile)
            await session.commit()
            await session.refresh(profile)
        return profile

async def update_income(telegram_id: int, income: float):
    profile = await get_or_create_profile(telegram_id)
    async with async_session() as session:
        profile = await session.merge(profile)
        profile.monthly_income = income
        await session.commit()

async def add_expense(telegram_id: int, category: str, amount: float, frequency: str, notes: str = ""):
    saving = calc_savings(amount, frequency)
    async with async_session() as session:
        exp = UserExpense(
            telegram_id=telegram_id,
            category=category,
            amount=amount,
            frequency=frequency,
            potential_ton_savings=saving,
            notes=notes
        )
        session.add(exp)
        await session.commit()
        return exp

async def get_expenses(telegram_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(UserExpense).where(UserExpense.telegram_id == telegram_id).order_by(UserExpense.created_at.desc())
        )
        return result.scalars().all()

async def get_total_savings(telegram_id: int) -> float:
    async with async_session() as session:
        result = await session.execute(
            select(UserExpense).where(UserExpense.telegram_id == telegram_id)
        )
        exps = result.scalars().all()
        return round(sum(e.potential_ton_savings for e in exps), 2)
