class KeyboardFactory:
    @staticmethod
    def get_reply(keyboard_name: str, lang: str = "he"):
        from bot.factory.reply_keyboards import KEYBOARDS
        kb = KEYBOARDS.get(keyboard_name, {})
        return kb.get(lang, kb.get("he"))
