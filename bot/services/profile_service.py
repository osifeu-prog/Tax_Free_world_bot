from sqlalchemy import select, delete
from bot.database.models import UserProfile, UserExpense
from bot.database.session import async_session

def calc_savings(amount: float, frequency: str) -> float:
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
    async with async_session() as session:
        result = await session.execute(
            select(UserProfile).where(UserProfile.telegram_id == telegram_id)
        )
        profile = result.scalar_one_or_none()
        if not profile:
            profile = UserProfile(telegram_id=telegram_id, monthly_income=income)
            session.add(profile)
        else:
            profile.monthly_income = income
        await session.commit()

async def add_expense(telegram_id: int, category: str, amount: float, frequency: str):
    saving = calc_savings(amount, frequency)
    async with async_session() as session:
        exp = UserExpense(
            telegram_id=telegram_id,
            category=category,
            amount=amount,
            frequency=frequency,
            potential_ton_savings=saving
        )
        session.add(exp)
        await session.commit()
        await session.refresh(exp)
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

async def delete_expense(telegram_id: int, expense_id: int) -> bool:
    async with async_session() as session:
        result = await session.execute(
            delete(UserExpense).where(
                UserExpense.id == expense_id,
                UserExpense.telegram_id == telegram_id
            )
        )
        await session.commit()
        return result.rowcount > 0

async def get_total_users_with_expenses() -> int:
    async with async_session() as session:
        result = await session.execute(
            select(func.count(func.distinct(UserExpense.telegram_id)))
        )
        return result.scalar() or 0

async def get_total_savings_sum() -> float:
    async with async_session() as session:
        result = await session.execute(
            select(func.sum(UserExpense.potential_ton_savings))
        )
        return result.scalar() or 0.0
