# -*- coding: utf-8 -*-
BUDGET_CATEGORIES = {
    "שכירות/משכנתא": 0.30,
    "חשבונות": 0.10,
    "מזון": 0.20,
    "תחבורה": 0.10,
    "חינוך": 0.10,
    "בריאות": 0.05,
    "בילויים": 0.05,
    "חיסכון": 0.10
}

def calculate_budget(income: float):
    result = {}
    for cat, pct in BUDGET_CATEGORIES.items():
        result[cat] = round(income * pct)
    return result

def budget_message(income: float):
    b = calculate_budget(income)
    msg = f"💰 <b>תקציב מומלץ להכנסה חודשית של {income:,.0f}</b>\n"
    msg += "━━━━━━━━━━━━━━━━━━\n"
    for cat, amount in b.items():
        msg += f"📌 {cat}: {amount:,}\n"
    msg += "\n💡 <i>העבר את התשלומים שלך ל-TON וחסוך בעמלות!</i>"
    return msg

