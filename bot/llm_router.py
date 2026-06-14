import os
from typing import Dict, Optional
from aiogram.types import Message

# Grok (xAI)
from xai_sdk import Client as GrokClient

# Gemini
import google.generativeai as genai

class LLMRouter:
    def __init__(self):
        self.grok_client = GrokClient(api_key=os.getenv("XAI_API_KEY"))
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')

        self.system_prompt = '''אתה יועץ כלכלי חכם, פרו-TON, פרו-ישראל, אנטי-שביר. 
        המטרה: לעזור למשתמשים להפוך את ישראל למעצמה כלכלית דרך חינוך, חיסכון ופנסיה.
        ענה תמיד בשפה של המשתמש, בצורה מעודדת, פשוטה ומעשית.'''

    async def get_response(self, message: Message, user_data: Optional[Dict] = None) -> str:
        text = message.text.strip()
        user_lang = user_data.get("user_language", "he") if user_data else "he"

        try:
            # Grok למורכבות גבוהה
            chat = self.grok_client.chat.create(model="grok-4")
            chat.append(system=self.system_prompt)
            if user_data:
                chat.append(user=f"נתוני משתמש: {user_data}")
            chat.append(user=text)
            response = chat.complete()
            return response.text
        except:
            # Fallback ל-Gemini
            try:
                prompt = f"{self.system_prompt}\nשפה: {user_lang}\n\n{text}"
                response = self.gemini_model.generate_content(prompt)
                return response.text
            except Exception as e:
                return "מצטער, יש עומס כרגע. נסה שוב בעוד כמה שניות."
