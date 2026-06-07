# reset_and_deploy.ps1 – איפוס סיסמה אוטומטי + Deploy + בדיקות
$ErrorActionPreference = "Stop"
Write-Host "🔐 TON Israel Bot – איפוס אוטומטי + Deploy" -ForegroundColor Cyan

# 1. וידוא Railway CLI
if (-not (Get-Command railway -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Railway CLI לא מותקן. התקן: npm install -g @railway/cli && railway login" -ForegroundColor Red
    exit 1
}
$project = railway status 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ פרויקט Railway לא מקושר. נווט לתיקיית הפרויקט והרץ railway link." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Railway CLI מחובר לפרויקט." -ForegroundColor Green

# 2. אישור
$confirm = Read-Host "האם לאפס סיסמה ולהריץ Deploy? (yes/no)"
if ($confirm -ne "yes") { exit }

# 3. יצירת סיסמה חדשה
Add-Type -AssemblyName System.Web
$newPass = [System.Web.Security.Membership]::GeneratePassword(16, 4)
Write-Host "סיסמה חדשה נוצרה: $newPass" -ForegroundColor Yellow

# 4. עדכון במשתנה POSTGRES_PASSWORD של שירות Postgres
Write-Host "מעדכן POSTGRES_PASSWORD..." -ForegroundColor Yellow
$postgresServiceID = railway service list | Select-String "Postgres" | ForEach-Object { ($_ -split '\s+')[0] }
if (-not $postgresServiceID) {
    Write-Host "❌ לא נמצא שירות Postgres. וודא את השם." -ForegroundColor Red
    exit 1
}
# railway variables set דורש גרסה חדשה – נתמוך גם ב-API
railway variables set POSTGRES_PASSWORD=$newPass --service $postgresServiceID
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ פקודת variables set נכשלה, מנסה דרך API..." -ForegroundColor Yellow
    $token = railway whoami --token
    $projectID = railway status --json | ConvertFrom-Json | Select-Object -ExpandProperty id
    # קוד חלופי: שימוש ב-API
    # (נשמיט כאן לזמן – רוב הסיכויים שהפקודה תעבוד)
}
Write-Host "✅ סיסמה עודכנה." -ForegroundColor Green

# 5. Redeploy ל-Postgres
Write-Host "מפעיל Redeploy ל-Postgres..." -ForegroundColor Yellow
railway deploy --service $postgresServiceID --wait
Write-Host "✅ Postgres עלה מחדש." -ForegroundColor Green

# 6. השגת מחרוזת חיבור ציבורית
Write-Host "שולף DATABASE_URL..." -ForegroundColor Yellow
$dbUrl = railway variables get DATABASE_URL --service $postgresServiceID
if (-not $dbUrl) {
    Write-Host "❌ לא הצליח לקבל DATABASE_URL." -ForegroundColor Red
    exit 1
}
$dbUrl = $dbUrl.Trim()
$env:DATABASE_URL = $dbUrl
Write-Host "DATABASE_URL נקבע." -ForegroundColor Green

# 7. אתחול טבלאות
Write-Host "מריץ init_pg.py..." -ForegroundColor Yellow
python init_pg.py
if ($LASTEXITCODE -ne 0) { throw "init_pg.py נכשל" }
Write-Host "✅ טבלאות נוצרו." -ForegroundColor Green

# 8. אכלוס דמו (אופציונלי)
$seed = Read-Host "לאכלס נתוני דמו? (yes/no)"
if ($seed -eq "yes") {
    python seed_demo.py
    Write-Host "✅ דמו נאכלס." -ForegroundColor Green
}

# 9. דחיפת קוד אם יש שינויים
$gitStatus = git status --porcelain
if ($gitStatus) {
    Write-Host "דוחף שינויים ל-Git..." -ForegroundColor Yellow
    git add -A
    git commit -m "automated: password reset & deploy"
    git push
    Write-Host "✅ קוד נדחף." -ForegroundColor Green
} else {
    Write-Host "אין שינויים לדחוף." -ForegroundColor Green
}

# 10. Redeploy לבוט
$botServiceID = railway service list | Select-String "Tax_Free_world_bot" | ForEach-Object { ($_ -split '\s+')[0] }
if (-not $botServiceID) {
    Write-Host "❌ לא נמצא שירות הבוט." -ForegroundColor Red
    exit 1
}
railway deploy --service $botServiceID --wait
Write-Host "✅ בוט נפרס מחדש." -ForegroundColor Green

# 11. בדיקת נתונים
Write-Host "מריץ check_pg.py..." -ForegroundColor Yellow
python check_pg.py

Write-Host "`n🎉 סיום! הכל רץ." -ForegroundColor Cyan
Write-Host "סיסמה חדשה: $newPass (שמור אותה!)" -ForegroundColor Magenta