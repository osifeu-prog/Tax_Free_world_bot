# ====================== TON-ISRAEL COMMAND CENTER v2.1 ======================

function Show-Status {
    Write-Host "
=== TAX FREE WORLD BOT - STATUS ===" -ForegroundColor Cyan
    Get-Content STATUS.md -Raw
}

function Show-Tasks {
    Write-Host "
=== OPEN TASKS ===" -ForegroundColor Yellow
    Get-Content tasks/TASKS.md -Raw
}

function Backup-Project {
    $date = Get-Date -Format "yyyyMMdd_HHmm"
    $backupName = "backups/backup_$date.zip"
    Compress-Archive -Path "bot","requirements.txt","README.md","STATUS.md","tasks","project.ps1" -DestinationPath $backupName -Force
    Write-Host "✅ Backup created: $backupName" -ForegroundColor Green
}

function Deploy {
    param([string]$message = "update")
    git add .
    git commit -m "update: 13:22 - $message" --allow-empty
    git push
    railway up --service Tax_Free_world_bot --detach
    Write-Host "🚀 Deployed successfully!" -ForegroundColor Green
}

# DIR משופר - Source of Truth בכל פעם
function dir {
    Get-ChildItem
    Write-Host "
=== PROJECT STATUS ===" -ForegroundColor Cyan
    Get-Content STATUS.md -TotalCount 15 | Select-Object -Last 12
    Write-Host "
Next Priority:" -ForegroundColor Yellow
    Get-Content tasks/TASKS.md | Select-String -Pattern "\- \[ \]" -Context 0,3
}

Write-Host "✅ TON-ISRAEL Command Center v2.1 Loaded" -ForegroundColor Green
Write-Host "פקודות: Show-Status, Show-Tasks, Backup-Project, Deploy 'message', dir" -ForegroundColor White
