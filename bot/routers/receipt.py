from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import google.generativeai as genai
import os

router = Router()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@router.message(F.photo)
async def handle_photo(msg: Message):
    await msg.answer("📸 מעבד תמונה...")

    # שמירת התמונה
    photo = msg.photo[-1]
    file = await msg.bot.get_file(photo.file_id)
    file_path = f"temp_{file.file_id}.jpg"
    await msg.bot.download_file(file.file_path, file_path)

    # שליחה ל-Gemini
    model = genai.GenerativeModel('gemini-1.5-flash')
    img = genai.upload_file(path=file_path)
    response = model.generate_content(["תאר לי מה כתוב על הקבלה: סכום, תאריך, עסק. תן לי JSON עם amount, date, merchant", img])

    await msg.answer(f"✅ זוהה:\n{response.text}")

    # ניקוי
    if os.path.exists(file_path):
        os.remove(file_path)

@router.message(Command("receipt"))
async def receipt_help(msg: Message):
    await msg.answer("📸 שלח לי תמונה של קבלה ואני אנסה לזהות את ההוצאה.")
