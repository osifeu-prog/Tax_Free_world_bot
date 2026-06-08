import json, os

REQUIRED_KEYS = [line.strip() for line in open("bot/locales/keys_required.txt", encoding="utf-8") if line.strip() and not line.startswith("#")]
LANGUAGES = ["he", "en", "ar", "ru"]

for lang in LANGUAGES:
    path = f"bot/locales/{lang}.json"
    if not os.path.exists(path):
        print(f"❌ Missing file: {lang}.json")
        continue
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    missing = [k for k in REQUIRED_KEYS if k not in data]
    if missing:
        print(f"⚠️ {lang}: missing keys: {missing}")
    else:
        print(f"✅ {lang}: all required keys present")
