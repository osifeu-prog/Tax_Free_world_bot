param(
    $Token = "8782546867:AAFkv4mYtkDXvwf9RJpCVU2Tv7oT4lVGq5M",
    $Base = "https://api.telegram.org",
    $ChatId = "224223270"
)
$ErrorActionPreference = "Continue"
$pass = 0; $fail = 0

function Test-Reply {
    param($Name, $Command, $ExpectedContains)
    Write-Host -NoNewline "$Name... "
    try {
        $body = @{chat_id=$ChatId; text=$Command} | ConvertTo-Json
        $resp = Invoke-RestMethod -Uri "$Base/bot$Token/sendMessage" -Method Post -Body $body -ContentType "application/json"
        if (-not $resp.ok) {
            Write-Host "❌ API error: $($resp.description)"
            $script:fail++
            return
        }
        $msgId = $resp.result.message_id
        # קריאת ההודעה בחזרה
        Start-Sleep -Seconds 2
        $resp2 = Invoke-RestMethod -Uri "$Base/bot$Token/getMessages?chat_id=$ChatId&message_ids=$msgId"
        $text = $resp2.result.messages[0].text
        if ($text -match $ExpectedContains) {
            Write-Host "✅"
            $script:pass++
        } else {
            Write-Host "❌ expected '$ExpectedContains' not in response"
            $script:fail++
        }
    } catch {
        Write-Host "❌ Exception: $_"
        $script:fail++
    }
}

Test-Reply "Start" "/start" "שלום"
Test-Reply "Compare" "/compare 500 10" "חיסכון שנתי"
Test-Reply "Budget" "/budget 12000" "תקציב"
Test-Reply "Wallet" "/wallet" "ארנק"
Test-Reply "Why" "/why" "עמלות"
Test-Reply "Business" "/business" "לעסקים"
Test-Reply "Crypto" "/crypto" "קריפטו"
Test-Reply "CBDC" "/cbdc" "CBDC"
Test-Reply "Decentral" "/decentral" "ביזור"
Test-Reply "Socio" "/socio" "סוציוקרטיה"
Test-Reply "Anti" "/anti" "שחיתות"
Test-Reply "Edu" "/edu" "חינוך"
Test-Reply "FAQ" "/faq" "שאלות"
Test-Reply "Tip" "/tip" "טיפ"
Test-Reply "Stats" "/stats" "סטטיסטיקות"
Test-Reply "Top" "/top" "לוח"
Test-Reply "Ref" "/ref" "הקוד"
Test-Reply "Contact" "/contact" "צור קשר"
Test-Reply "ID" "/id" "המשתמש"
Test-Reply "Daily" "/daily" "סיכום"
Test-Reply "MyData" "/mydata" "הנתונים"
Test-Reply "Help" "/help" "פקודות"
Test-Reply "Admin" "/admin" "אדמין"
Test-Reply "Debug" "/debug" "סטטוס"
Test-Reply "Miniapp" "/miniapp" "לחץ"
Test-Reply "Keyboard" "/keyboard" "בחר"
Test-Reply "Hide" "/hide" "הוסתרה"
Test-Reply "Export" "/export" "מנהלים"
Test-Reply "Donate" "/donate" "תרומה"
Test-Reply "AcademyExtended" "/academy_extended" "ביזוריות"
Test-Reply "AcademyNFT" "/academy_nft" "NFT"
Test-Reply "AcademyDAO" "/academy_dao" "DAO"
Test-Reply "Feedback" "/feedback בדיקה" "שלח"
Test-Reply "Ask" "/ask איך לחסוך" "תשובה"
Test-Reply "Gift" "/gift" "נקודות"

Write-Host "`n========================="
Write-Host "✅ Passed: $pass"
Write-Host "❌ Failed: $fail"
Write-Host "========================="
