# connect_pg.ps1  התחברות ל-PostgreSQL של Railway
param([string]$DatabaseUrl = $env:DATABASE_URL)
if (-not $DatabaseUrl) {
    Write-Host "Please set DATABASE_URL environment variable or pass -DatabaseUrl"
    exit
}
# חילוץ פרמטרים
$url = [uri]$DatabaseUrl
$user = $url.UserInfo.Split(":")[0]
$pass = $url.UserInfo.Split(":")[1]
$host = $url.Host
$port = $url.Port
$db = $url.AbsolutePath.TrimStart('/')
Write-Host "Connecting to PostgreSQL at $host`:$port/$db as $user"
# שימוש ב-psql (אם מותקן)
psql -h $host -p $port -U $user -d $db
