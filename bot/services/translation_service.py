import json, os

TRANSLATIONS = {}
_locale_dir = os.path.join(os.path.dirname(__file__), '..', 'locales')
for lang_file in os.listdir(_locale_dir):
    if lang_file.endswith('.json'):
        lang_code = lang_file.replace('.json', '')
        with open(os.path.join(_locale_dir, lang_file), 'r', encoding='utf-8') as f:
            TRANSLATIONS[lang_code] = json.load(f)

class translator:
    @staticmethod
    def t(lang: str, key: str) -> str:
        if lang not in TRANSLATIONS:
            lang = 'en'
        return TRANSLATIONS.get(lang, {}).get(key, TRANSLATIONS['en'].get(key, key))
