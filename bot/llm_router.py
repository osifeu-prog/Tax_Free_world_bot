import os
from typing import Dict, Optional
from aiogram.types import Message
import google.generativeai as genai

class LLMRouter:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        self.system_prompt = '''אתה **יועץ כלכלי אסטרטגי** של Tax Free World.
        תפקידך: לעזור למשתמשים להפוך את ישראל למעצמה כלכלית דרך TON, חיסכון, פנסיה, קריפטו וחינוך פיננסי.
        עקרונות:
        - תמיד פרו-ישראל, פרו-TON, אנטי-שביר
        - ענה בצורה מעשית, מעודדת וברורה
        - השתמש בשפה של המשתמש (עברית בעיקר)
        - קשר תשובות לחזון: חיסכון → פנסיה → חופש כלכלי → ישראל חזקה'''

    async def get_response(self, message: Message, user_data: Optional[Dict] = None) -> str:
        text = message.text.strip()
        if not text:
            return "שאל אותי משהו על חיסכון, פנסיה, TON או כלכלה!"

        try:
            prompt = f"{self.system_prompt}\n\nשאלת המשתמש: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception:
            return "מצטער, יש עומס זמני. נסה שוב בעוד כמה שניות."
