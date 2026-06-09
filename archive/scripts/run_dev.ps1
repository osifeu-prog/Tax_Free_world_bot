param(
    [string]$Task = "run"
)
$venvPath = ".\venv\Scripts\Activate.ps1"
if (Test-Path $venvPath) {
    . $venvPath
}
if ($Task -eq "run") {
    python bot/main.py
} elseif ($Task -eq "migrate") {
    cd bot
    alembic upgrade head
    cd ..
} else {
    Write-Host "Usage: .\run_dev.ps1 [run|migrate]"
}
