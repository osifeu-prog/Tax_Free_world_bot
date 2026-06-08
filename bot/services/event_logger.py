from bot.database.session import async_session
from sqlalchemy import text

async def log_event(user_id: int, event_type: str, payload: str = None):
    async with async_session() as session:
        await session.execute(
            text("INSERT INTO events_log (user_id, event_type, payload) VALUES (:uid, :type, :payload)"),
            {"uid": user_id, "type": event_type, "payload": payload or ""}
        )
        await session.commit()
