import json, os

class TranslationService:
    def __init__(self):
        self.data = {}
        self.load_locales()

    def load_locales(self):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        locales_dir = os.path.join(base_dir, "..", "locales")
        self.langs = ["he", "en", "ar", "ru", "es", "fr"]
        for lang in self.langs:
            path = os.path.join(locales_dir, f"{lang}.json")
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8-sig") as f:
                        self.data[lang] = json.load(f)
                except Exception as e:
                    print(f"שגיאה בטעינת {lang}: {e}")
            else:
                print(f"⚠️ Missing locale: {lang}.json")

    def t(self, lang: str, key: str, **kwargs):
        if lang in self.data and key in self.data[lang]:
            return self.data[lang][key]
        if "he" in self.data and key in self.data["he"]:
            return self.data["he"][key]
        if "en" in self.data and key in self.data["en"]:
            return self.data["en"][key]
        return f"[{key}]"

translator = TranslationService()
