from sqlalchemy import text
from bot.database.session import engine
import datetime

async def log_useless_action(user_id: int, action: str):
    try:
        async with engine.begin() as conn:
            await conn.run_sync(
                lambda c: c.execute(
                    text("INSERT INTO useless_log (user_id, action) VALUES (:uid, :action)"),
                    {"uid": user_id, "action": action}
                )
            )
    except Exception:
        pass
