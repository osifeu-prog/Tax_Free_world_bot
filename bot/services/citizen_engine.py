import json, datetime
from sqlalchemy import select, func
from bot.database.session import async_session
from bot.database.models import Event

class CitizenEngine:
    async def emit(self, telegram_id: int, event_type: str, payload: dict):
        async with async_session() as session:
            event = Event(
                telegram_id=telegram_id,
                type=event_type,
                payload=json.dumps(payload),
                timestamp=datetime.datetime.utcnow()
            )
            session.add(event)
            await session.commit()

    async def get_profile(self, telegram_id: int):
        async with async_session() as session:
            # XP total
            xp = (await session.execute(
                select(func.coalesce(func.sum(func.json_extract(Event.payload, '$.xp')), 0))
                .where(Event.telegram_id == telegram_id, Event.type == "xp_gained")
            )).scalar()
            # Level (100 XP = 1 level)
            level = max(1, xp // 100 + 1)
            # Reputation
            rep_knowledge = (await session.execute(
                select(func.count()).where(Event.telegram_id == telegram_id, Event.type == "knowledge_action")
            )).scalar() * 2
            rep_community = (await session.execute(
                select(func.count()).where(Event.telegram_id == telegram_id, Event.type == "referral_success")
            )).scalar() * 5
            rep_leadership = (await session.execute(
                select(func.count()).where(Event.telegram_id == telegram_id, Event.type == "budget_action")
            )).scalar() * 1

            return {
                "telegram_id": telegram_id,
                "level": level,
                "xp": xp,
                "reputation_knowledge": rep_knowledge,
                "reputation_community": rep_community,
                "reputation_leadership": rep_leadership,
                "profile_score": round(xp * 0.3 + rep_knowledge + rep_community + rep_leadership, 2)
            }

citizen = CitizenEngine()
