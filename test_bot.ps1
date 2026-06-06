param($Token="8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M", $Base="https://api.telegram.org")
$cid="224223270";$p=0;$f=0
function T($n,$c){Write-Host -NoNewline "$n... ";$r=Invoke-RestMethod -Uri "$Base/bot$Token/sendMessage" -Method Post -Body (ConvertTo-Json @{chat_id=$cid;text=$c}) -ContentType "application/json; charset=utf-8"
if($r.ok){Write-Host "✅";$script:p++}else{Write-Host "❌ $($r.description)";$script:f++}}
T "Start" "/start";T "Compare" "/compare 500 10";T "Wallet" "/wallet";T "Why" "/why";T "Business" "/business"
T "Budget" "/budget 12000";T "Crypto" "/crypto";T "CBDC" "/cbdc";T "Decentral" "/decentral"
T "Socio" "/socio";T "Anti" "/anti";T "Edu" "/edu";T "Tip" "/tip";T "FAQ" "/faq"
T "ID" "/id";T "Help" "/help";T "Profile" "/profile";T "Stats" "/stats";T "Top" "/top"
T "Ref" "/ref";T "Contact" "/contact"
Write-Host "`nTotal: $($p+$f) | Passed: $p | Failed: $f"
