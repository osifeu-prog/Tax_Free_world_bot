def calc_accumulating(profile: dict) -> dict:
    """חישוב פנסיה צוברת"""
    years = profile["retirement_age"] - profile["age_now"]
    monthly_contrib = profile["salary_bruto"] * (
        profile["contribution_employee"] + profile["contribution_employer"]
    ) / 100
    net_return = (profile["expected_return"] - profile["management_fees"]) / 100
    capital = profile.get("current_capital", 0)
    for _ in range(int(years)):
        capital = (capital + monthly_contrib * 12) * (1 + net_return)
    annuity_factor = 210 if profile["retirement_age"] < 67 else 200
    monthly_pension = capital / annuity_factor
    return {"capital": round(capital, 2), "monthly_pension": round(monthly_pension, 2)}

def calc_budgetary(profile: dict) -> dict:
    """חישוב פנסיה תקציבית"""
    accrual = min(profile["seniority_years"] * (profile.get("accrual_rate", 2) / 100), 0.7)
    monthly_pension = profile["salary_bruto"] * accrual
    annuity_factor = 210 if profile["retirement_age"] < 67 else 200
    capital_est = monthly_pension * annuity_factor
    return {"capital": round(capital_est, 2), "monthly_pension": round(monthly_pension, 2)}

def estimate_tax(monthly_pension, threshold=5000, rate=0.1):
    """הערכת מס (פשטנית)"""
    if monthly_pension <= threshold:
        return 0
    return round((monthly_pension - threshold) * rate, 2)
