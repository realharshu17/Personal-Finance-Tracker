from data_store import load_data
from transaction import filter_by_month

def monthly_summary(year, month):
    txns = filter_by_month(year, month)
    income  = round(sum(t["amount"] for t in txns if t["type"] == "income"), 2)
    expense = round(sum(t["amount"] for t in txns if t["type"] == "expense"), 2)
    savings = round(income - expense, 2)
    rate    = round((savings / income * 100) if income > 0 else 0.0, 2)
    return {
        "year": year, "month": month,
        "income": income, "expense": expense,
        "savings": savings, "savings_rate": rate}

def top_spending_categories(year=None, month=None, top_n=5):
    data = load_data()
    txns = data["transactions"]
    if year and month:
        prefix = f"{year:04d}-{month:02d}"
        txns = [t for t in txns if t["date"].startswith(prefix) and t["type"] == "expense"]
    else:
        txns = [t for t in txns if t["type"] == "expense"]
    totals = {}
    for t in txns:
        totals[t["category"]] = round(totals.get(t["category"], 0) + t["amount"], 2)
    ranked = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    grand_total = sum(v for _, v in ranked)
    result = []
    for cat, amt in ranked[:top_n]:
        pct = round((amt / grand_total * 100) if grand_total > 0 else 0, 1)
        result.append({"category": cat, "amount": amt, "percentage": pct})
    return result

def daily_average_spend(year, month):
    import calendar
    txns = filter_by_month(year, month)
    total_expense = sum(t["amount"] for t in txns if t["type"] == "expense")
    days_in_month = calendar.monthrange(year, month)[1]
    return round(total_expense / days_in_month, 2)

def savings_rate(year, month):
    summary = monthly_summary(year, month)
    return summary["savings_rate"]

def spending_trend(year, month):
    curr = monthly_summary(year, month)
    prev_month = month - 1 if month > 1 else 12
    prev_year  = year if month > 1 else year - 1
    prev = monthly_summary(prev_year, prev_month)
    diff = round(curr["expense"] - prev["expense"], 2)
    if diff > 0:
        trend = "increased"
    elif diff < 0:
        trend = "decreased"
    else:
        trend = "unchanged"
    return {"trend": trend, "difference": abs(diff),
            "current": curr["expense"], "previous": prev["expense"]}

def find_highest_expense():
    """Return the single largest expense transaction ever recorded."""
    data = load_data()
    expenses = [t for t in data["transactions"] if t["type"] == "expense"]
    if not expenses:
        return None
    return max(expenses, key=lambda t: t["amount"])

def income_vs_expense_ratio():
    """Return the ratio of total income to total expenses (all time)."""
    data = load_data()
    income  = sum(t["amount"] for t in data["transactions"] if t["type"] == "income")
    expense = sum(t["amount"] for t in data["transactions"] if t["type"] == "expense")
    ratio   = round(income / expense, 2) if expense > 0 else float("inf")
    return {"total_income": round(income, 2),
            "total_expense": round(expense, 2),
            "ratio": ratio}

def print_monthly_summary(year, month):
    MONTH_NAMES = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
    s = monthly_summary(year, month)
    print(f"\n  +----------------------------------------+")
    print(f"  |  {MONTH_NAMES[month]} {year} Summary")
    print(f"  +----------------------------------------+")
    print(f"  |  Total Income   : Rs. {s['income']:>10.2f}        |")
    print(f"  |  Total Expense  : Rs. {s['expense']:>10.2f}        |")
    print(f"  |  Net Savings    : Rs. {s['savings']:>10.2f}        |")
    print(f"  |  Savings Rate   : {s['savings_rate']:>9.1f}%        |")
    print(f"  +----------------------------------------+")
    tops = top_spending_categories(year, month)
    if tops:
        print(f"  |    Top Spending Categories:            |")
        for i, entry in enumerate(tops, 1):
            print(f"  |  {i}. {entry['category']:<12} Rs.{entry['amount']:>8.2f}  {entry['percentage']:>5.1f}%  |")
    print(f"  +----------------------------------------+\n")