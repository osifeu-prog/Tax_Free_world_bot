Write-Host "Checking SQLite DB..."
if (Test-Path "data.db") { Write-Host "✅ data.db exists" } else { Write-Host "❌ data.db missing" }
Write-Host "Checking Redis..."
python -c "import os,redis.asyncio,asyncio; r=redis.from_url(os.getenv('REDIS_URL','redis://localhost:6379')); asyncio.run(r.ping()); print('✅ Redis OK')"
