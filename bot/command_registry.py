# bot/command_registry.py
# Registry of all bot commands, used for /help, /menu, i18n, logging.

COMMANDS = {
    # חיסכון אישי
    "start": {"category": "חיסכון", "i18n_key": "cmd_start", "log": "start"},
    "compare": {"category": "חיסכון", "i18n_key": "cmd_compare", "log": "compare_view"},
    "wallet": {"category": "חיסכון", "i18n_key": "cmd_wallet", "log": "wallet_view"},
    "why": {"category": "חיסכון", "i18n_key": "cmd_why", "log": "why_view"},
    "business": {"category": "חיסכון", "i18n_key": "cmd_business", "log": "business_view"},
    "budget": {"category": "חיסכון", "i18n_key": "cmd_budget", "log": "budget_view"},
    "profile": {"category": "חיסכון", "i18n_key": "cmd_profile", "log": "profile_view"},
    "expenses": {"category": "חיסכון", "i18n_key": "cmd_expenses", "log": "expenses_view"},
    "addexpense": {"category": "חיסכון", "i18n_key": "cmd_addexpense", "log": "expense_add"},
    "setincome": {"category": "חיסכון", "i18n_key": "cmd_setincome", "log": "income_set"},
    "delexpense": {"category": "חיסכון", "i18n_key": "cmd_delexpense", "log": "expense_delete"},
    "mysavings": {"category": "חיסכון", "i18n_key": "cmd_mysavings", "log": "savings_view"},
    "setwallet": {"category": "חיסכון", "i18n_key": "cmd_setwallet", "log": "wallet_set"},

    # פנסיה
    "pension": {"category": "פנסיה", "i18n_key": "cmd_pension", "log": "pension_start"},
    "report_pension": {"category": "פנסיה", "i18n_key": "cmd_report_pension", "log": "report_pension_view"},

    # משק בית
    "household": {"category": "משק בית", "i18n_key": "cmd_household", "log": "household_view"},
    "familygroup": {"category": "משק בית", "i18n_key": "cmd_familygroup", "log": "familygroup_create"},
    "shopping": {"category": "משק בית", "i18n_key": "cmd_shopping", "log": "shopping_add"},
    "chore": {"category": "משק בית", "i18n_key": "cmd_chore", "log": "chore_add"},

    # אקדמיה
    "academy": {"category": "אקדמיה", "i18n_key": "cmd_academy", "log": "academy_view"},
    "crypto": {"category": "אקדמיה", "i18n_key": "cmd_crypto", "log": "course_view"},
    "cbdc": {"category": "אקדמיה", "i18n_key": "cmd_cbdc", "log": "course_view"},
    "decentral": {"category": "אקדמיה", "i18n_key": "cmd_decentral", "log": "course_view"},
    "socio": {"category": "אקדמיה", "i18n_key": "cmd_socio", "log": "course_view"},
    "anti": {"category": "אקדמיה", "i18n_key": "cmd_anti", "log": "course_view"},
    "edu": {"category": "אקדמיה", "i18n_key": "cmd_edu", "log": "course_view"},
    "academy_extended": {"category": "אקדמיה", "i18n_key": "cmd_academy_ext", "log": "course_view"},
    "academy_nft": {"category": "אקדמיה", "i18n_key": "cmd_academy_nft", "log": "course_view"},
    "academy_dao": {"category": "אקדמיה", "i18n_key": "cmd_academy_dao", "log": "course_view"},
    "vision": {"category": "אקדמיה", "i18n_key": "cmd_vision", "log": "vision_view"},
    "spark": {"category": "אקדמיה", "i18n_key": "cmd_spark", "log": "spark_view"},
    "course_progress": {"category": "אקדמיה", "i18n_key": "cmd_course_progress", "log": "course_progress_view"},
    "seed_courses": {"category": "אקדמיה", "i18n_key": "cmd_seed_courses", "log": None},  # Admin only

    # קהילה
    "ref": {"category": "קהילה", "i18n_key": "cmd_ref", "log": "ref_link_generated"},
    "qr": {"category": "קהילה", "i18n_key": "cmd_qr", "log": "qr_view"},
    "stats": {"category": "קהילה", "i18n_key": "cmd_stats", "log": "stats_view"},
    "top": {"category": "קהילה", "i18n_key": "cmd_top", "log": "top_view"},
    "tip": {"category": "קהילה", "i18n_key": "cmd_tip", "log": "tip_send"},
    "contact": {"category": "קהילה", "i18n_key": "cmd_contact", "log": "contact_view"},
    "faq": {"category": "קהילה", "i18n_key": "cmd_faq", "log": "faq_view"},
    "daily": {"category": "קהילה", "i18n_key": "cmd_daily", "log": "daily_claim"},
    "mydata": {"category": "קהילה", "i18n_key": "cmd_mydata", "log": "mydata_view"},
    "gift": {"category": "קהילה", "i18n_key": "cmd_gift", "log": "gift_send"},

    # תרומות
    "donate": {"category": "תרומות", "i18n_key": "cmd_donate", "log": "donate_view"},

    # כלים
    "help": {"category": "כלים", "i18n_key": "cmd_help", "log": "help_view"},
    "menu": {"category": "כלים", "i18n_key": "cmd_menu", "log": "menu_view"},
    "language": {"category": "כלים", "i18n_key": "cmd_language", "log": "language_change"},
    "miniapp": {"category": "כלים", "i18n_key": "cmd_miniapp", "log": "miniapp_view"},
    "keyboard": {"category": "כלים", "i18n_key": "cmd_keyboard", "log": "keyboard_view"},
    "hide": {"category": "כלים", "i18n_key": "cmd_hide", "log": "hide_keyboard"},
    "ask": {"category": "כלים", "i18n_key": "cmd_ask", "log": "ask_ai"},
    "feedback": {"category": "כלים", "i18n_key": "cmd_feedback", "log": "feedback_send"},
    "quiz": {"category": "כלים", "i18n_key": "cmd_quiz", "log": "quiz_start"},
    "ai": {"category": "כלים", "i18n_key": "cmd_ai", "log": "ai_chat"},
    "architecture": {"category": "כלים", "i18n_key": "cmd_architecture", "log": "architecture_view"},

    # אודות
    "whyus": {"category": "אודות", "i18n_key": "cmd_whyus", "log": "whyus_view"},
    "familyguide": {"category": "אודות", "i18n_key": "cmd_familyguide", "log": "familyguide_view"},

    # ניהול (Admin)
    "admin": {"category": "ניהול", "i18n_key": "cmd_admin", "log": None},
    "export": {"category": "ניהול", "i18n_key": "cmd_export", "log": None},
    "debug": {"category": "ניהול", "i18n_key": "cmd_debug", "log": None},
    "addgroup": {"category": "ניהול", "i18n_key": "cmd_addgroup", "log": None},
    "groups": {"category": "ניהול", "i18n_key": "cmd_groups", "log": None},
    "report": {"category": "ניהול", "i18n_key": "cmd_report", "log": "report_view"},
    "setrole": {"category": "ניהול", "i18n_key": "cmd_setrole", "log": None},

    # TON City (חדש)
    "city": {"category": "TON City", "i18n_key": "cmd_city", "log": "city_view"},
    "market": {"category": "TON City", "i18n_key": "cmd_market", "log": "market_view"},
}

def get_commands_by_category():
    cats = {}
    for cmd, info in COMMANDS.items():
        cat = info["category"]
        cats.setdefault(cat, []).append(cmd)
    return cats
