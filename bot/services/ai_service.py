import os
import google.generativeai as genai
from groq import AsyncGroq

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
gemini_model = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    gemini_model = genai.GenerativeModel("gemini-1.5-flash")

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
groq_client = None
if GROQ_API_KEY:
    groq_client = AsyncGroq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = (
    "אתה עוזר חינוכי לבוט TON Israel, שמטרתו לעזור למשפחות בישראל לחסוך בעמלות, "
    "לעבור למערכת תשלומים מבוזרת (TON), וללמוד על כלכלה חכמה, ביזוריות, NFT, "
    "וסוציוקרטיה. ענה בעברית, בקצרה, ובצורה ידידותית. אם השאלה לא קשורה, הפנה את המשתמש לפקודות הרלוונטיות בבוט."
)

async def ask_ai(question: str) -> str:
    if groq_client:
        try:
            resp = await groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                max_tokens=400
            )
            return resp.choices[0].message.content
        except:
            pass
    if gemini_model:
        try:
            response = await gemini_model.generate_content_async(
                f"{SYSTEM_PROMPT}\n\nשאלה: {question}",
                generation_config={"max_output_tokens": 400}
            )
            return response.text
        except:
            return "שגיאה בפנייה ל-AI. נסה שוב מאוחר יותר."
    return "שירות ה-AI אינו זמין. הגדר GEMINI_API_KEY או GROQ_API_KEY."
