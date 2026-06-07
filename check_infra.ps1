Write-Host "Checking SQLite DB..."
if (Test-Path "data.db") {
    $dbSize = (Get-Item "data.db").Length
    Write-Host "✅ data.db exists ($dbSize bytes)"
} else {
    Write-Host "❌ data.db not found!"
}
Write-Host "Checking Redis..."
python -c "import os, asyncio, redis.asyncio; r = redis.from_url(os.environ.get('REDIS_URL','redis://localhost:6379')); asyncio.run(r.ping()); print('✅ Redis ping OK')"
