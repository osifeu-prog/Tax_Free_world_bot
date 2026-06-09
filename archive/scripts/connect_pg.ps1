param(
    [string]$PublicUrl = $env:DATABASE_PUBLIC_URL
)
if (-not $PublicUrl) {
    # נסה לקחת מ-Railway (אם הגדרת)
    $PublicUrl = "postgresql://postgres:kWTGhinhMbrlPjhiFLwWSIuSMZGgmxKV@taxfreeworldbot-postgres.railway.internal:5432/railway"
    Write-Host "Using default internal URL. Replace with Public URL if needed."
}
Write-Host "Connecting to PostgreSQL..."
psql $PublicUrl -c "SELECT COUNT(*) FROM users;"
psql $PublicUrl -c "SELECT COUNT(*) FROM user_profiles;"
psql $PublicUrl -c "SELECT COUNT(*) FROM user_expenses;"
psql $PublicUrl -c "SELECT COUNT(*) FROM command_logs;"
psql $PublicUrl -c "SELECT telegram_id, monthly_income FROM user_profiles LIMIT 5;"
psql $PublicUrl -c "SELECT * FROM user_expenses LIMIT 5;"
Write-Host "Done."
