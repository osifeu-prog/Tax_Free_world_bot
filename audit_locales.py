import json, os, sys

LOCALES_DIR = "bot/locales"
KEYS_FILE = os.path.join(LOCALES_DIR, "keys_required.txt")
LANGS = ["he", "en", "ar", "ru"]

# 1. טען את המפתחות הנדרשים
required = set()
with open(KEYS_FILE, "r", encoding="utf-8-sig") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#"):
            required.add(line)

all_ok = True
for lang in LANGS:
    path = os.path.join(LOCALES_DIR, f"{lang}.json")
    with open(path, "r", encoding="utf-8-sig") as f:
        data = json.load(f)
    existing = set(data.keys())
    missing = required - existing
    if missing:
        print(f"⚠️ {lang}: missing keys: {sorted(missing)}")
        all_ok = False
    else:
        print(f"✅ {lang}: all keys present")

if all_ok:
    print("\n🎉 All locales complete.")
else:
    sys.exit(1)

