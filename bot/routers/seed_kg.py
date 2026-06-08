from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from bot.database.session import async_session
from bot.database.models import KnowledgeNode, KnowledgeEdge
from sqlalchemy import select

router = Router()

@router.message(Command("seed_kg"))
async def cmd_seed_kg(msg: Message):
    # בדיקת אדמין (פשוטה)
    if msg.from_user.id != 224223270:
        await msg.answer("⛔ אדמין בלבד.")
        return

    async with async_session() as session:
        existing = (await session.execute(select(KnowledgeNode))).scalars().all()
        if existing:
            await msg.answer(f"✅ Knowledge Graph already seeded ({len(existing)} nodes)")
            return

        nodes_data = [
            {"slug": "economics_basics", "title": "יסודות הכלכלה", "type": "module", "difficulty": 1, "estimated_minutes": 30},
            # ... (השלם את שאר ה‑nodes כפי שהיה ב‑seed_knowledge_graph_fixed.py)
        ]
        nodes = [KnowledgeNode(**data) for data in nodes_data]
        session.add_all(nodes)
        await session.commit()

        node_map = {node.slug: node.id for node in nodes}
        edges_data = [
            # ... (השלם edges)
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

