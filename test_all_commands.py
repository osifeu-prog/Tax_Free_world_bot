import asyncio, json, os, sys, time, tracemalloc
from collections import defaultdict
from bot.config import settings

# ======================== הגדרות ========================
BOT_TOKEN = settings.bot_token
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
ADMIN_ID = 224223270  # ה-TG ID שלך

COMMANDS = [
    "/start", "/menu", "/pension", "/city", "/market", "/compare",
    "/donate", "/ref", "/daily", "/report", "/help", "/academy",
    "/budget", "/profile", "/wallet", "/stats", "/top", "/tip",
    "/contact", "/faq", "/gift", "/miniapp", "/keyboard", "/hide",
    "/ask", "/feedback", "/quiz", "/ai", "/architecture", "/vision",
    "/crypto", "/cbdc", "/decentral", "/socio", "/anti", "/edu",
    "/academy_nft", "/academy_dao", "/academy_extended", "/spark",
    "/course_progress", "/seed_courses", "/household", "/familygroup",
    "/shopping", "/chore", "/expenses", "/addexpense", "/delexpense",
    "/setincome", "/mysavings", "/setwallet", "/business", "/why",
    "/whyus", "/familyguide", "/language", "/id", "/mydata",
    "/export", "/debug", "/admin", "/addgroup", "/groups",
    "/setrole", "/report_pension", "/requestadmin", "/addadmin",
    "/login", "/setpassword", "/removeadmin", "/qr"
]

# ======================== פונקציית בדיקה ========================
async def test_command(session, command):
    """שולח פקודה ומודד זמן תגובה"""
    start = time.monotonic()
    try:
        async with session.post(
            f"{BASE_URL}/sendMessage",
            json={
                "chat_id": ADMIN_ID,
                "text": command,
                "parse_mode": "HTML"
            },
            timeout=10
        ) as resp:
            data = await resp.json()
            elapsed = (time.monotonic() - start) * 1000  # ms
            if data.get("ok"):
                return {"command": command, "status": "✅", "time_ms": round(elapsed)}
            else:
                return {"command": command, "status": "❌", "error": data.get("description", "Unknown"), "time_ms": round(elapsed)}
    except Exception as e:
        elapsed = (time.monotonic() - start) * 1000
        return {"command": command, "status": "❌", "error": str(e), "time_ms": round(elapsed)}

# ======================== בדיקת Redis ========================
async def test_redis():
    try:
        from bot.services.redis_service import redis_client
        await redis_client.ping()
        return "🟢 מחובר"
    except:
        return "🔴 מנותק"

# ======================== בדיקת DB ========================
async def test_db():
    try:
        from sqlalchemy import text
        from bot.database.session import engine
        async with engine.begin() as conn:
            tables = await conn.run_sync(lambda c: [row[0] for row in c.execute(text("SELECT name FROM sqlite_master WHERE type='table'")).fetchall()])
            count = await conn.run_sync(lambda c: c.execute(text("SELECT COUNT(*) FROM users")).fetchone()[0])
            return f"🟢 {len(tables)} טבלאות, {count} משתמשים"
    except Exception as e:
        return f"🔴 {e}"

# ======================== גודל מערכת ========================
def get_system_size():
    total_lines = 0
    total_files = 0
    for root, dirs, files in os.walk("bot"):
        for f in files:
            if f.endswith(".py"):
                total_files += 1
                with open(os.path.join(root, f), "r", encoding="utf-8") as fp:
                    total_lines += len(fp.readlines())
    return {"python_files": total_files, "python_lines": total_lines}

# ======================== Main ========================
async def main():
    import aiohttp
    
    print("=" * 60)
    print("🧪 TON Israel Bot  בדיקת מערכת מלאה")
    print("=" * 60)
    
    # 1. מדידת ביצועים
    tracemalloc.start()
    start_total = time.monotonic()
    
    # 2. בדיקת 60+ פקודות
    results = []
    async with aiohttp.ClientSession() as session:
        for i, cmd in enumerate(COMMANDS, 1):
            result = await test_command(session, cmd)
            results.append(result)
            print(f"  {result['status']} {cmd} ({result['time_ms']}ms)")
    
    total_time = time.monotonic() - start_total
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    # 3. סיכום
    passed = sum(1 for r in results if r["status"] == "✅")
    failed = sum(1 for r in results if r["status"] == "❌")
    avg_time = sum(r["time_ms"] for r in results) / len(results) if results else 0
    
    # 4. בדיקות נוספות
    redis_status = await test_redis()
    db_status = await test_db()
    system_size = get_system_size()
    
    # 5. דוח
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_commands": len(COMMANDS),
        "passed": passed,
        "failed": failed,
        "success_rate": f"{(passed/len(COMMANDS)*100):.1f}%",
        "total_time_seconds": round(total_time, 2),
        "avg_response_ms": round(avg_time),
        "memory_current_mb": round(current / 1024 / 1024, 2),
        "memory_peak_mb": round(peak / 1024 / 1024, 2),
        "system": system_size,
        "redis": redis_status,
        "database": db_status,
        "failures": [r for r in results if r["status"] == "❌"]
    }
    
    # 6. שמירה לקובץ
    with open("bot_health_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    
    # 7. שליחת סיכום לטלגרם
    async with aiohttp.ClientSession() as session:
        summary = (
            f"📊 <b>דוח בריאות מערכת</b>\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"📋 פקודות: {passed}/{len(COMMANDS)} עברו ({report['success_rate']})\n"
            f"⏱️ זמן תגובה ממוצע: {avg_time:.0f}ms\n"
            f"⏱️ זמן כולל: {total_time:.1f}s\n"
            f"💾 זיכרון: {report['memory_current_mb']}MB (שיא: {report['memory_peak_mb']}MB)\n"
            f"📦 Redis: {redis_status}\n"
            f"🗄️ DB: {db_status}\n"
            f"📂 קבצים: {system_size['python_files']} קבצי Python, {system_size['python_lines']} שורות\n\n"
            f"📄 דוח מלא: bot_health_report.json"
        )
        await session.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": ADMIN_ID, "text": summary, "parse_mode": "HTML"}
        )
    
    print("\n" + "=" * 60)
    print(f"✅ {passed}/{len(COMMANDS)} עברו ({report['success_rate']})")
    print(f"⏱️ זמן ממוצע: {avg_time:.0f}ms | סה\"כ: {total_time:.1f}s")
    print(f"💾 זיכרון: {report['memory_current_mb']}MB")
    print(f"📄 דוח מלא: bot_health_report.json")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)

if __name__ == "__main__":
    asyncio.run(main())
