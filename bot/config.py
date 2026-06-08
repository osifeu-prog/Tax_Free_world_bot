from dotenv import load_dotenv
load_dotenv()
# -*- coding: utf-8 -*-
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    bot_token: str
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    admin_ids: Optional[str] = None
    groq_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None

    model_config = {
        "case_sensitive": False,
        "env_file": None
    }

settings = Settings()

def get_admin_ids():
    raw = settings.admin_ids or ''
    return [int(x.strip()) for x in raw.split(',') if x.strip()]

    AI_TRANSLATION_ENABLED: bool = Field(default=False, env="AI_TRANSLATION_ENABLED")
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")

