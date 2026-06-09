Write-Host "=== TON Israel Pre-Deploy Check ===" -ForegroundColor Cyan

# 1. וודא שאנחנו בתיקיית הפרויקט
if (-not (Test-Path "bot\main.py")) {
    Write-Host "❌ Not in project directory!" -ForegroundColor Red
    exit 1
}

# 2. בדיקת smoke_test.py
Write-Host "🔍 Running smoke_test..." -ForegroundColor Yellow
$env:BOT_TOKEN = "8782546867:AAFxsqjad8RHCLjRcLpJp8WJ_uQ_mQnHKJc"
$result = python smoke_test.py 2>&1
if ($LASTEXITCODE -ne 0 -or $result -match "❌") {
    Write-Host "❌ Smoke test failed!" -ForegroundColor Red
    Write-Host $result
    exit 1
}
Write-Host "✅ Smoke test passed" -ForegroundColor Green

# 3. בדיקת audit_locales.py
Write-Host "🔍 Checking locales..." -ForegroundColor Yellow
$locales = python audit_locales.py 2>&1
if ($locales -match "missing") {
    Write-Host "⚠️ Locale issues:" -ForegroundColor Yellow
    Write-Host $locales
} else {
    Write-Host "✅ All locales complete" -ForegroundColor Green
}

# 4. בדיקת DB local (אם bot.db קיים)
if (Test-Path "bot.db") {
    Write-Host "🔍 Local DB check..." -ForegroundColor Yellow
    python -c "import sqlite3; conn=sqlite3.connect('bot.db'); c=conn.cursor(); c.execute(\"SELECT name FROM sqlite_master WHERE type='table'\"); print('Tables:', [row[0] for row in c.fetchall()]); conn.close()"
}

# 5. בדיקת git status
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️ Uncommitted changes:" -ForegroundColor Yellow
    git status --short
}

# 6. גיבוי main.py
Copy-Item bot\main.py bot\main.py.stable -Force
Write-Host "✅ main.py.stable backup updated" -ForegroundColor Green

Write-Host "`n🎉 Pre-deploy check complete! Ready to push." -ForegroundColor Cyan
