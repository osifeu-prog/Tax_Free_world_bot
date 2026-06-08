import os
os.environ.setdefault("BOT_TOKEN", "dummy_for_seed")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///bot.db")

import asyncio
from sqlalchemy import select
from bot.database.session import async_session, engine
from bot.database.models import Base, KnowledgeNode, KnowledgeEdge

async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables ensured")

    async with async_session() as session:
        existing = (await session.execute(select(KnowledgeNode))).scalars().all()
        if existing:
            print(f"Already seeded ({len(existing)} nodes)")
            return

        nodes_data = [
            {"slug": "economics_basics", "title": "יסודות הכלכלה", "type": "module", "difficulty": 1, "estimated_minutes": 30},
            {"slug": "inflation", "title": "אינפלציה", "type": "concept", "difficulty": 2, "estimated_minutes": 45},
            {"slug": "cbdc", "title": "CBDC - מטבעות בנק מרכזי", "type": "concept", "difficulty": 3, "estimated_minutes": 60},
            {"slug": "taxation", "title": "מיסוי ומדיניות פיסקלית", "type": "concept", "difficulty": 3, "estimated_minutes": 50},
            {"slug": "bitcoin", "title": "ביטקוין", "type": "concept", "difficulty": 2, "estimated_minutes": 40},
            {"slug": "ton", "title": "TON Blockchain", "type": "concept", "difficulty": 2, "estimated_minutes": 35},
            {"slug": "wallets", "title": "ארנקים דיגיטליים", "type": "lesson", "difficulty": 1, "estimated_minutes": 25},
            {"slug": "defi", "title": "DeFi - פיננסים מבוזרים", "type": "module", "difficulty": 4, "estimated_minutes": 90},
            {"slug": "decentralization", "title": "ביזור מול ריכוז", "type": "concept", "difficulty": 2, "estimated_minutes": 40},
            {"slug": "dao", "title": "DAO - ארגונים אוטונומיים", "type": "module", "difficulty": 3, "estimated_minutes": 70},
            {"slug": "voting", "title": "הצבעה מבוזרת", "type": "lesson", "difficulty": 2, "estimated_minutes": 30},
            {"slug": "transparency", "title": "שקיפות ומלחמה בשחיתות", "type": "concept", "difficulty": 2, "estimated_minutes": 35},
            {"slug": "financial_literacy", "title": "אוריינות פיננסית", "type": "skill", "difficulty": 1, "estimated_minutes": 20},
            {"slug": "critical_thinking", "title": "חשיבה ביקורתית", "type": "skill", "difficulty": 2, "estimated_minutes": 40},
        ]

        nodes = [KnowledgeNode(**data) for data in nodes_data]
        session.add_all(nodes)
        await session.commit()

        node_map = {node.slug: node.id for node in nodes}

        edges_data = [
            {"from": "economics_basics", "to": "inflation", "relation": "prerequisite"},
            {"from": "inflation", "to": "cbdc", "relation": "builds_upon"},
            {"from": "economics_basics", "to": "taxation", "relation": "related_to"},
            {"from": "economics_basics", "to": "bitcoin", "relation": "related_to"},
            {"from": "bitcoin", "to": "ton", "relation": "builds_upon"},
            {"from": "ton", "to": "wallets", "relation": "prerequisite"},
            {"from": "wallets", "to": "defi", "relation": "unlocks"},
            {"from": "decentralization", "to": "dao", "relation": "prerequisite"},
            {"from": "dao", "to": "voting", "relation": "builds_upon"},
            {"from": "decentralization", "to": "transparency", "relation": "related_to"},
            {"from": "cbdc", "to": "decentralization", "relation": "related_to"},
            {"from": "bitcoin", "to": "dao", "relation": "related_to"},
        ]

        edges = []
        for e in edges_data:
            fid = node_map.get(e["from"])
            tid = node_map.get(e["to"])
            if fid and tid:
                edges.append(KnowledgeEdge(from_node_id=fid, to_node_id=tid, relation_type=e["relation"]))

        session.add_all(edges)
        await session.commit()
        print(f"Seeded {len(nodes)} nodes and {len(edges)} edges")

asyncio.run(seed())
