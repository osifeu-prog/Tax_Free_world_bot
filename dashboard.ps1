# 🏗️ TON Israel  SSOT Dashboard
## תאריך: $(Get-Date -Format "yyyy-MM-dd HH:mm")

## Railway
- Status: $(Invoke-RestMethod -Uri "https://taxfreeworldbot-production.up.railway.app/health" -ErrorAction SilentlyContinue)
- DB: $(python -c "import asyncio; from bot.database.session import engine; asyncio.run(engine.connect()); print('OK')" 2>$null)
- Redis: $(python -c "import os,redis.asyncio,asyncio; r=redis.from_url(os.getenv('REDIS_URL','redis://localhost:6379')); asyncio.run(r.ping()); print('OK')" 2>$null)

## GitHub
- Last commit: $(git log -1 --format=%ci)
- Branch: $(git branch --show-current)

## Tests
- test_bot.ps1: $(if ((.\test_bot.ps1 | Select-String "Failed: 0").Count -gt 0) { "OK" } else { "FAIL" })
