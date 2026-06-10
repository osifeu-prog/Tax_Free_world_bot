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
            try:
                with open(file, encoding='utf-8-sig') as f:  # utf-8-sig removes BOM
                    self.translations[lang] = json.load(f)
            except Exception as e:
                print(f"Error loading {file}: {e}")
    
    def get(self, key: str, lang: str = "en", **kwargs) -> str:
        text = self.translations.get(lang, self.translations.get("en", {})).get(key, f"[{key}]")
        return text.format(**kwargs) if kwargs else text

i18n = I18n()
