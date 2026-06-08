import openai
from bot.config import settings
import json, asyncio

class AITranslator:
    def __init__(self):
        if settings.AI_TRANSLATION_ENABLED and settings.OPENAI_API_KEY:
            openai.api_key = settings.OPENAI_API_KEY
            self.enabled = True
        else:
            self.enabled = False

    async def translate(self, text: str, target_lang: str, source_lang: str = "en") -> str:
        if not self.enabled:
            return None
        try:
            prompt = f"Translate the following text from {source_lang} to {target_lang}, keeping any HTML tags and placeholders like {{name}} exactly as they are:\n\n{text}"
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3,
            )
            translated = response.choices[0].message.content.strip()
            return translated
        except Exception as e:
            print(f"AI translation error: {e}")
            return None
