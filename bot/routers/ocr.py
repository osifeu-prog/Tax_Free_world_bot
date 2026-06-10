import os
import io
import asyncio
import logging
from aiogram import Router, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import Command
from PIL import Image
import google.generativeai as genai
from bot.database.session import engine
from sqlalchemy import text

router = Router()
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    vision_model = genai.GenerativeModel('gemini-1.5-flash')
else:
    vision_model = None
    logger.warning("GEMINI_API_KEY not set, OCR disabled")

async def extract_text_from_image(image_bytes: bytes) -> str:
    """שלח תמונה ל-Gemini ובקש לחלץ סכום, תיאור, תאריך"""
    if not vision_model:
        return None
    img = Image.open(io.BytesIO(image_bytes))
    prompt = """
    אתה בוט כלכלי. נתון צילום קבלה.
    חלץ בבקשה:
    1. סכום כולל (במספרים, ללא סימני מטבע)
    2. תיאור קצר (מה קנו)
    3. תאריך (אם קיים)
    תשובה בפורמט JSON:
    {"amount": 123.45, "description": "קניות בסופר", "date": "2025-01-01"}
    אם לא מזהה סכום, החזר {"amount": null}
    """
    try:
        response = vision_model.generate_content([prompt, img])
        text = response.text.strip()
        # ניסיון לפרש JSON
        if text.startswith("```json"):
            text = text.split("```json")[1].split("```")[0]
        elif text.startswith("```"):
            text = text.split("```")[1].split("```")[0]
        import json
        data = json.loads(text)
        return data
    except Exception as e:
        logger.error(f"OCR error: {e}")
        return None

@router.message(Command("receipt"))
async def cmd_receipt(msg: Message):
    await msg.answer("📸 שלח תמונה של הקבלה (JPG/PNG)")

@router.message(F.photo)
async def handle_photo(msg: Message):
    # בדיקה שהמשתמש ביקש OCR לאחרונה - נשתמש ב-FSM פשוט או נניח שהפקודה /receipt הוזנה
    # נבדוק את ההיסטוריה  פשוט: נענה רק אם ההודעה הקודמת הייתה /receipt?
    # כאן נבצע זיהוי ישיר ללא שמירת מצב (לשם פשטות)
    photo = msg.photo[-1]
    file = await msg.bot.get_file(photo.file_id)
    file_bytes = await msg.bot.download_file(file.file_path)
    data = await extract_text_from_image(file_bytes.read())
    if data and data.get("amount"):
        amount = data["amount"]
        desc = data.get("description", "הוצאה מזוהה")
        # הוסף הוצאה לטבלה (user_expenses)
        uid = msg.from_user.id
        async with engine.begin() as conn:
            await conn.execute(
                text("INSERT INTO user_expenses (user_id, amount, description, created_at) VALUES (:uid, :amt, :desc, datetime('now'))"),
                {"uid": uid, "amt": amount, "desc": desc}
            )
        await msg.answer(f"✅ הוספת הוצאה: {amount}  - {desc}")
    else:
        await msg.answer("❌ לא זיהיתי סכום. נסה לצלם קבלה ברורה יותר.")
