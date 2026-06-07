from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    bot_token: str
    database_url: str = "sqlite+aiosqlite:///./data.db"
    admin_ids: list[int] = []

    class Config:
        env_file = None
        env_file_encoding = "utf-8"

settings = Settings()

