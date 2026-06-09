import os
import json
from google.cloud import translate_v2 as translate

# הגדרות
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bot/google-credentials.json'

translate_client = translate.Client()

LANGUAGES = {
    'he': 'Hebrew',
    'en': 'English',
    'ru': 'Russian',
    'ar': 'Arabic',
    'es': 'Spanish',
    'fr': 'French',
    'yi': 'Yiddish'
}

def translate_text(text, target_lang):
    if not text or text.strip() == "":
        return text
    result = translate_client.translate(text, target_language=target_lang)
    return result['translatedText']

def auto_translate_all():
    base_file = 'bot/locales/he.json'
    
    with open(base_file, 'r', encoding='utf-8') as f:
        base_data = json.load(f)
    
    for lang_code in LANGUAGES:
        if lang_code == 'he':
            continue
            
        target_file = f'bot/locales/{lang_code}.json'
        
        if os.path.exists(target_file):
            with open(target_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)
        else:
            existing = {}
        
        print(f"\n🔄 מתרגם ל-{LANGUAGES[lang_code]} ({lang_code})...")
        
        for key, value in base_data.items():
            if key not in existing or not existing[key] or existing[key] == value:
                try:
                    translated = translate_text(value, lang_code)
                    existing[key] = translated
                    print(f"  ✅ {key}: {translated[:60]}...")
                except Exception as e:
                    print(f"  ❌ שגיאה בתרגום {key}: {e}")
                    existing[key] = value  # fallback
        
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(existing, f, ensure_ascii=False, indent=2)
        
        print(f"✅ סיום תרגום ל-{lang_code}")

if __name__ == "__main__":
    auto_translate_all()
