import os
import asyncio
import logging
from aiogram import Bot

BOT_TOKEN = os.getenv("BOT_TOKEN")

print("=== DEBUG TOKEN ===")
print("BOT_TOKEN exists:", bool(BOT_TOKEN))
print("BOT_TOKEN length:", len(BOT_TOKEN) if BOT_TOKEN else 0)
print("First 20 chars:", BOT_TOKEN[:20] if BOT_TOKEN else "None")

async def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN is missing!")
        return
    
    bot = Bot(token=BOT_TOKEN)
    me = await bot.get_me()
    print("✅ Bot is working!")
    print(f"Bot username: @{me.username}")
    print(f"Bot ID: {me.id}")

if __name__ == "__main__":
    asyncio.run(main())
