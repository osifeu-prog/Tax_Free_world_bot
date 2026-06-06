FEES = {
    "ביט":     {"percent": 0.015, "fixed": 0.0},
    "פייבוקס": {"percent": 0.018, "fixed": 0.5},
    "TON":     {"percent": 0.001, "fixed": 0.0},
}

def calc_fee(service, amount):
    f = FEES[service]
    return round(amount * f["percent"] + f["fixed"], 2)

def build_comparison(amount, tx_per_month):
    bit_fee = calc_fee("ביט", amount)
    paybox_fee = calc_fee("פייבוקס", amount)
    ton_fee = calc_fee("TON", amount)
    save_bit = round((bit_fee - ton_fee) * tx_per_month * 12)
    save_paybox = round((paybox_fee - ton_fee) * tx_per_month * 12)
    return (
        f"💰 <b>השוואת עמלות להעברה של {amount:,.0f}</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🔴 <b>ביט:</b>      {bit_fee}  (1.5%)\n"
        f"🟠 <b>פייבוקס:</b>  {paybox_fee}  (1.8% + 0.5)\n"
        f"🟢 <b>TON:</b>      {ton_fee}  (0.1%) ✅\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📅 <b>אם אתה מבצע {tx_per_month} העברות בחודש:</b>\n"
        f"→ לעומת ביט:     <b>{save_bit:,} חיסכון שנתי</b>\n"
        f"→ לעומת פייבוקס: <b>{save_paybox:,} חיסכון שנתי</b>\n\n"
        f"💡 <b>למה זה קורה?</b>\n"
        f"• ביט ופייבוקס גובות עמלות גבוהות לכל העברה.\n"
        f"• TON מבוססת בלוקצ'יין  ללא מתווכים, לכן העמלה נמוכה במיוחד.\n"
        f"• החיסכון השנתי הוא <b>הכסף שנשאר בכיס שלך</b>.\n\n"
        f"📲 <i>כדי להתחיל לחסוך, פתח ארנק TON דרך /wallet</i>"
    )
