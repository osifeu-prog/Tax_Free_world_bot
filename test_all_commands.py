import os, json, time, sys, asyncio
import aiohttp

BOT_TOKEN = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("BOT_TOKEN", "")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

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

async def test_command(session, command, chat_id):
    start = time.monotonic()
    try:
        async with session.post(
            f"{BASE_URL}/sendMessage",
            json={"chat_id": chat_id, "text": command},
            timeout=10
        ) as resp:
            data = await resp.json()
            elapsed = (time.monotonic() - start) * 1000
            ok = data.get("ok")
            return {
                "command": command,
                "status": "✅" if ok else "❌",
                "time_ms": round(elapsed),
                "error": data.get("description", "") if not ok else ""
            }
    except Exception as e:
        return {"command": command, "status": "❌", "time_ms": 0, "error": str(e)}

async def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not set. Usage: python test_all_commands.py <TOKEN> <CHAT_ID>")
        return
    if len(sys.argv) < 3:
        print("❌ CHAT_ID missing. Usage: python test_all_commands.py <TOKEN> <CHAT_ID>")
        return
    chat_id = int(sys.argv[2])

    results = []
    async with aiohttp.ClientSession() as session:
        for cmd in COMMANDS:
            r = await test_command(session, cmd, chat_id)
            results.append(r)
            print(f"  {r['status']} {cmd} ({r['time_ms']}ms)")
            await asyncio.sleep(0.3)

    passed = sum(1 for r in results if r['status'] == '✅')
    total = len(results)
    avg_time = sum(r['time_ms'] for r in results) / total if total else 0

    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": total, "passed": passed, "failed": total - passed,
        "success_rate": f"{(passed/total*100):.1f}%",
        "avg_response_ms": round(avg_time),
        "failures": [r for r in results if r['status'] == '❌']
    }

    with open("bot_health_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    summary = (
        f"📊 <b>דוח בדיקות אוטומטיות</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"✅ עברו: {passed}/{total} ({report['success_rate']})\n"
        f"⏱️ זמן תגובה ממוצע: {avg_time:.0f}ms\n"
        f"📄 דוח מלא: bot_health_report.json"
    )
    await session.post(
        f"{BASE_URL}/sendMessage",
        json={"chat_id": chat_id, "text": summary, "parse_mode": "HTML"}
    )
    print(f"\n✅ {passed}/{total} ({report['success_rate']}) | avg {avg_time:.0f}ms")

if __name__ == "__main__":
    asyncio.run(main())