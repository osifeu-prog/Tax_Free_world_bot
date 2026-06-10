import json
from pathlib import Path
from typing import Dict

class I18n:
    def __init__(self):
        self.translations: Dict[str, Dict] = {}
        self.load_translations()
    
    def load_translations(self):
        locales_dir = Path("bot/locales")
        for file in locales_dir.glob("*.json"):
            lang = file.stem
            with open(file, encoding='utf-8') as f:
                self.translations[lang] = json.load(f)
    
    def get(self, key: str, lang: str = "en", **kwargs) -> str:
        text = self.translations.get(lang, self.translations.get("en", {})).get(key, f"[{key}]")
        return text.format(**kwargs) if kwargs else text

i18n = I18n()
