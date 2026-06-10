from bot.services.translation_service import translator

class MessageFactory:
    @staticmethod
    async def get_message(lang: str, key: str, **kwargs):
        try:
            return translator.t(lang, key, **kwargs)
        except:
            return f"⚠️ {key} not found"
