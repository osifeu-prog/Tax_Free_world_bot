# -*- coding: utf-8 -*-
import csv, io
from sqlalchemy import select
from bot.database.session import async_session
from bot.database.models import CommandLog

async def export_logs_csv():
    async with async_session() as session:
        result = await session.execute(select(CommandLog).order_by(CommandLog.timestamp.desc()).limit(1000))
        logs = result.scalars().all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "user_id", "command", "params", "timestamp"])
    for log in logs:
        writer.writerow([log.id, log.user_id, log.command, log.params, log.timestamp.isoformat()])
    return output.getvalue()

