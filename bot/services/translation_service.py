import json
from pathlib import Path
from typing import Dict

class TranslationService:
    def __init__(self):
        self.locales: Dict[str, Dict[str, str]] = {}
        self.load_locales()
    
    def load_locales(self):
        """טוען את כל קבצי התרגום"""
        locales_dir = Path("bot/locales")
        for file_path in locales_dir.glob("*.json"):
            lang_code = file_path.stem
            try:
                with open(file_path, encoding="utf-8") as f:
                    self.locales[lang_code] = json.load(f)
            except Exception as e:
                print(f"שגיאה בטעינת {lang_code}: {e}")
    
    def t(self, language: str, key: str, **kwargs) -> str:
        """תרגום ראשי עם fallback לעברית"""
        lang = (language or "he").lower()
        
        # ניסיון בשפה הנבחרת
        if lang in self.locales and key in self.locales[lang]:
            text = self.locales[lang][key]
        # fallback לעברית
        elif "he" in self.locales and key in self.locales["he"]:
            text = self.locales["he"][key]
        else:
            text = f"[{key}]"  # fallback debug
        
        # החלפת משתנים
        return text.format(**kwargs) if kwargs else text

# Singleton
translator = TranslationService()
