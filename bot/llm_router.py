import os
from typing import Dict, Optional
from aiogram.types import Message
import google.generativeai as genai

class LLMRouter:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.5-flash')

        self.system_prompt = '''אתה יועץ כלכלי חכם, פרו-TON, פרו-ישראל, אנטי-שביר. 
        המטרה שלך היא לעזור למשתמשים להפוך את ישראל למעצמה כלכלית דרך חינוך, חיסכון, פנסיה וקריפטו.
        ענה תמיד בשפה של ההודעה של המשתמש, בצורה מעודדת, פשוטה ומעשית.'''

    async def get_response(self, message: Message, user_data: Optional[Dict] = None) -> str:
        text = message.text.strip()
        if not text:
            return "שאל אותי משהו!"

        try:
            prompt = f"{self.system_prompt}\n\n{text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return "מצטער, יש עומס זמני. נסה שוב בעוד כמה שניות."
