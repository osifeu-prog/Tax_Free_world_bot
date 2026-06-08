# family_calc.py  מנוע תקציב משפחתי

def add_income(profile: dict, amount: float):
    profile["monthly_income"] = amount
    return profile

def add_expense(expenses: list, category: str, amount: float, note: str = ""):
    expenses.append({
        "category": category,
        "amount": amount,
        "note": note,
        "id": len(expenses) + 1
    })
    return expenses

def calculate_savings(income: float, expenses: list):
    total_exp = sum(e["amount"] for e in expenses)
    return income - total_exp

def household_budget(members: list):
    total_income = sum(m.get("monthly_income", 0) for m in members)
    total_expenses = sum(sum(e["amount"] for e in m.get("expenses", [])) for m in members)
    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": total_income - total_expenses,
        "members_count": len(members)
    }
