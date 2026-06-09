import os
import json
from deep_translator import GoogleTranslator

LANGUAGES = ['en', 'ru', 'ar', 'es', 'fr', 'yi']

def translate_text(text: str, target: str) -> str:
    if not text or not text.strip():
        return text
    try:
        return GoogleTranslator(source='auto', target=target).translate(text)
    except Exception as e:
        print(f"⚠️ שגיאה בתרגום ל-{target}: {e}")
        return text

def auto_translate_free():
    base_path = 'bot/locales/he.json'
    if not os.path.exists(base_path):
        print("❌ חסר he.json")
        return

    with open(base_path, 'r', encoding='utf-8-sig') as f:
        base = json.load(f)

    for lang in LANGUAGES:
        path = f'bot/locales/{lang}.json'
        existing = {}
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8-sig') as f:
                existing = json.load(f)

        print(f"\n🔄 מתרגם → {lang} ...")
        updated = 0
        for key, value in base.items():
            if key not in existing or not existing.get(key):
                translated = translate_text(value, lang)
                existing[key] = translated
                updated += 1
                print(f"  ✅ {key}")

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)

        print(f"✅ {lang}  {updated} מחרוזות תורגמו")

if __name__ == "__main__":
    auto_translate_free()
