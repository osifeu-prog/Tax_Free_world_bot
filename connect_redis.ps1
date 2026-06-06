# connect_redis.ps1  התחברות ל-Redis של Railway
param([string]$RedisUrl = $env:REDIS_URL)
if (-not $RedisUrl) {
    Write-Host "Please set REDIS_URL or pass -RedisUrl"
    exit
}
# שימוש ב-redis-cli (אם מותקן)
redis-cli -u $RedisUrl
