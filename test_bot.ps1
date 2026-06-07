param($Token="8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M", $Base="https://api.telegram.org")
$cid="224223270";$p=0;$f=0
function T($n,$c){Write-Host -NoNewline "$n... ";$r=Invoke-RestMethod -Uri "$Base/bot$Token/sendMessage" -Method Post -Body (ConvertTo-Json @{chat_id=$cid;text=$c}) -ContentType "application/json; charset=utf-8"
if($r.ok){Write-Host "✅";$script:p++}else{Write-Host "❌ $($r.description)";$script:f++}}
T "Start" "/start"; T "Compare" "/compare 500 10"; T "Budget" "/budget 12000"; T "Profile" "/profile"
T "Expenses" "/expenses"; T "AddExpense" "/addexpense"; T "SetIncome" "/setincome"; T "DeleteExpense" "/delexpense 1"
T "Wallet" "/wallet"; T "Why" "/why"; T "Business" "/business"; T "Crypto" "/crypto"; T "CBDC" "/cbdc"
T "Decentral" "/decentral"; T "Socio" "/socio"; T "Anti" "/anti"; T "Edu" "/edu"; T "FAQ" "/faq"
T "Tip" "/tip"; T "Stats" "/stats"; T "Top" "/top"; T "Ref" "/ref"; T "Contact" "/contact"; T "ID" "/id"
T "Daily" "/daily"; T "MyData" "/mydata"; T "Help" "/help"; T "Admin" "/admin"; T "Debug" "/debug"
T "Miniapp" "/miniapp"; T "Keyboard" "/keyboard"; T "Hide" "/hide"; T "Export" "/export"; T "Donate" "/donate"
T "AcademyExtended" "/academy_extended"; T "AcademyNFT" "/academy_nft"; T "AcademyDAO" "/academy_dao"
T "Feedback" "/feedback תיקון"; T "Ask" "/ask איך לחסוך"; T "Gift" "/gift"
T "Quiz" "/quiz"
T "AddAdmin" "/addadmin 224223270 admin 1234"
T "Login" "/login 1234"
T "SetPassword" "/setpassword 1234 5678"
T "RemoveAdmin" "/removeadmin 224223270"
Write-Host "`nTotal: $($p+$f) | Passed: $p | Failed: $f"
