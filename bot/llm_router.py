import os
from typing import Dict, Optional
from aiogram.types import Message

import google.generativeai as genai

class LLMRouter:
    def __init__(self):
        # Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')

        self.system_prompt = '''אתה יועץ כלכלי חכם, פרו-TON, פרו-ישראל, אנטי-שביר. 
        המטרה: לעזור למשתמשים להפוך את ישראל למעצמה כלכלית דרך חינוך, חיסכון ופנסיה.
        ענה תמיד בשפה של המשתמש, בצורה מעודדת, פשוטה ומעשית.'''

    async def get_response(self, message: Message, user_data: Optional[Dict] = None) -> str:
        text = message.text.strip()
        user_lang = user_data.get("user_language", "he") if user_data else "he"

        try:
            prompt = f"{self.system_prompt}\nשפה: {user_lang}\n\n{text}"
            response = self.gemini_model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "מצטער, יש עומס כרגע. נסה שוב בעוד כמה שניות."
