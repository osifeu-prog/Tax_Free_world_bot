Write-Host "Checking PostgreSQL..."
python -c "import asyncio; from bot.database.session import engine; asyncio.run(engine.connect()); print('✅ DB connected')"
Write-Host "Checking Redis..."
python -c "import os,redis.asyncio,asyncio; r=redis.from_url(os.getenv('REDIS_URL','redis://localhost:6379')); asyncio.run(r.ping()); print('✅ Redis OK')"
