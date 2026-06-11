import os
import asyncio
from typing import Dict, Optional
from aiogram.types import Message

from xai_sdk import Client as GrokClient
from xai_sdk.chat import system, user

import google.generativeai as genai

from bot.services.language_detector import get_user_language

class LLMRouter:
    def __init__(self):
        # Grok
        self.grok_client = GrokClient(api_key=os.getenv("XAI_API_KEY"))
        
        # Gemini
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.gemini_model = genai.GenerativeModel('gemini-2.5-flash')
        
        self.system_prompt = (
            "You are a financial advisor for Tax Free World, a community-driven bot that helps "
            "Israelis save, invest, learn, and build wealth with TON. "
            "You speak fluent Hebrew, English, Russian, and Arabic. "
            "Always respond in the language of the user's last message. "
            "Be practical, honest, encouraging, and direct. "
            "Use the user's data (role, savings, XP, wallet) when provided. "
            "Never fabricate numbers; refer to bot commands like /profile, /adde, /pension, /academy."
        )

    async def get_response(self, message: Message, user_context: Optional[Dict] = None) -> str:
        text = message.text.strip()
        if not text:
            return "אנא כתוב שאלה."
        
        user_lang = get_user_language(text, user_context.get("language") if user_context else None)
        
        if self.should_use_grok(text):
            return await self._call_grok(text, user_context, user_lang)
        else:
            return await self._call_gemini(text, user_context, user_lang)

    def should_use_grok(self, text: str) -> bool:
        """נתב ל-Grok עבור שאלות מורכבות"""
        if len(text) > 70:
            return True
        complex_keywords = ["למה", "איך", "חזון", "פנסיה", "השקעה", "לנתח", "דעה", "למה כדאי", "מה דעתך", "חישוב",
                            "why", "how", "vision", "invest", "pension", "analyze"]
        return any(k in text.lower() for k in complex_keywords)

    async def _call_grok(self, text: str, context: Optional[Dict], lang: str) -> str:
        try:
            chat = self.grok_client.chat.create(model="grok-4")
            chat.append(system(self.system_prompt))
            if context:
                chat.append(user(f"User data: {context}"))
            chat.append(user(text))
            response = chat.sample()
            return response.text
        except Exception as e:
            print(f"Grok failed: {e}")
            return await self._call_gemini(text, context, lang)

    async def _call_gemini(self, text: str, context: Optional[Dict], lang: str) -> str:
        try:
            full_prompt = f"{self.system_prompt}\n\nLanguage: {lang}\n\n{text}"
            if context:
                full_prompt = f"User data: {context}\n\n{full_prompt}"
            response = self.gemini_model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return "מצטער, יש עומס כרגע. נסה שוב בעוד כמה שניות."
