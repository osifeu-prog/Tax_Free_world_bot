import asyncio, os, random, string
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ DATABASE_URL not set.")
    exit(1)

if DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://", 1)
elif DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSession = async_sessionmaker(engine, expire_on_commit=False)

async def main():
    async with AsyncSession() as session:
        await session.execute(text("INSERT INTO users (telegram_id, language, is_business, points, last_gift_date, gift_shares_today, created_at) VALUES (111111, 'he', false, 100, '2026-06-07', 0, '2026-06-07 12:00:00') ON CONFLICT (telegram_id) DO NOTHING"))
        await session.execute(text("INSERT INTO users (telegram_id, language, is_business, points, last_gift_date, gift_shares_today, created_at) VALUES (222222, 'he', true, 250, '2026-06-07', 2, '2026-06-07 12:00:00') ON CONFLICT (telegram_id) DO NOTHING"))
        await session.execute(text("INSERT INTO users (telegram_id, language, is_business, points, last_gift_date, gift_shares_today, created_at) VALUES (224223270, 'he', false, 500, '2026-06-07', 5, '2026-06-07 12:00:00') ON CONFLICT (telegram_id) DO NOTHING"))

        await session.execute(text("INSERT INTO user_profiles (telegram_id, monthly_income, family_size, city, opt_in_data) VALUES (111111, 12000, 3, 'תל אביב', true) ON CONFLICT (telegram_id) DO NOTHING"))
        await session.execute(text("INSERT INTO user_profiles (telegram_id, monthly_income, family_size, city, opt_in_data) VALUES (222222, 8000, 1, 'חיפה', false) ON CONFLICT (telegram_id) DO NOTHING"))
        await session.execute(text("INSERT INTO user_profiles (telegram_id, monthly_income, family_size, city, opt_in_data) VALUES (224223270, 15000, 4, 'ירושלים', true) ON CONFLICT (telegram_id) DO NOTHING"))

        await session.execute(text("INSERT INTO user_expenses (telegram_id, category, amount, frequency, potential_ton_savings, notes, created_at) VALUES (111111, 'שכירות', 3500, 'חודשי', 504, 'דירת 3 חדרים', '2026-06-07 12:00:00')"))
        await session.execute(text("INSERT INTO user_expenses (telegram_id, category, amount, frequency, potential_ton_savings, notes, created_at) VALUES (111111, 'חשמל', 500, 'חודשי', 72, '', '2026-06-07 12:00:00')"))
        await session.execute(text("INSERT INTO user_expenses (telegram_id, category, amount, frequency, potential_ton_savings, notes, created_at) VALUES (222222, 'ארנונה', 200, 'חודשי', 28, '', '2026-06-07 12:00:00')"))
        await session.execute(text("INSERT INTO user_expenses (telegram_id, category, amount, frequency, potential_ton_savings, notes, created_at) VALUES (224223270, 'ביטוח', 300, 'חודשי', 43, 'ביטוח דירה', '2026-06-07 12:00:00')"))

        await session.execute(text("INSERT INTO command_logs (user_id, command, params, timestamp) VALUES (224223270, 'start', '', '2026-06-07 12:00:00')"))
        await session.execute(text("INSERT INTO command_logs (user_id, command, params, timestamp) VALUES (224223270, 'compare', '500 10', '2026-06-07 12:01:00')"))

        await session.execute(text("INSERT INTO referrals (code, inviter_id, clicks) VALUES ('DEMOCODE1', 111111, 3) ON CONFLICT (code) DO NOTHING"))
        await session.execute(text("INSERT INTO referrals (code, inviter_id, clicks) VALUES ('DEMOCODE2', 222222, 7) ON CONFLICT (code) DO NOTHING"))

        await session.commit()
        print("✅ Demo data seeded successfully")

asyncio.run(main())
