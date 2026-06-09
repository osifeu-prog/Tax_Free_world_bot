from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import KnowledgeNode, KnowledgeEdge
from sqlalchemy import select

router = Router()

@router.message(Command("seed_kg"))
async def cmd_seed_kg(msg: Message):
    # רק אדמין (תחליף במזהה שלך)
    if msg.from_user.id != 224223270:
        await msg.answer("⛔ אדמין בלבד.")
        return

    async with async_session() as session:
        # בדוק אם כבר זרוע
        existing = (await session.execute(select(KnowledgeNode))).scalars().all()
        if existing:
            await msg.answer(f"✅ Knowledge Graph already seeded ({len(existing)} nodes).")
            return

        # Nodes
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

        await msg.answer(f"✅ Knowledge Graph seeded: {len(nodes)} nodes, {len(edges)} edges.")
