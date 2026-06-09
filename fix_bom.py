import os

def remove_bom(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
    
    # הסרת BOM אם קיים (EF BB BF)
    if content.startswith(b'\xef\xbb\xbf'):
        content = content[3:]
        with open(file_path, 'wb') as f:
            f.write(content)
        print(f"✅ BOM removed: {os.path.basename(file_path)}")
    else:
        print(f"ℹ️  No BOM: {os.path.basename(file_path)}")

# ====================== הרץ על כל הקבצים ======================
root_dir = "bot"

for dirpath, _, filenames in os.walk(root_dir):
    for filename in filenames:
        if filename.endswith('.py'):
            full_path = os.path.join(dirpath, filename)
            remove_bom(full_path)

print("\n🎉 סיום בדיקה ותיקון BOM!")
