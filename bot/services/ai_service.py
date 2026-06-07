import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None

async def ask_gemini(question: str) -> str:
    if not model:
        return "שירות ה‑AI אינו זמין כרגע. נסה שוב מאוחר יותר."
    try:
        response = await model.generate_content_async(
            f"אתה עוזר חינוכי לבוט TON Israel. ענה בקצרה ובעברית: {question}",
            generation_config={"max_output_tokens": 300}
        )
        return response.text
    except Exception as e:
        return f"שגיאה בפנייה ל‑AI: {str(e)}"
