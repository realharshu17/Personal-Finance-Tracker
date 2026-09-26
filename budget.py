from data_store import load_data, save_data
from transaction import filter_by_month
from datetime import datetime

def set_budget(category, limit):
    try:
        limit = round(float(limit), 2)
        if limit <= 0:
            raise ValueError
    except ValueError:
        print("  ERROR! Budget limit must be a positive number.")
        return False
    data = load_data()
    data["budgets"][category] = limit
    save_data(data)
    print(f"  OK! Budget for '{category}' set to Rs.{limit:.2f}/month.")
    return True

def update_budget(category, new_limit):
    data = load_data()
    if category not in data["budgets"]:
        print(f"  WARNING! No existing budget for '{category}'. Creating new.")
    return set_budget(category, new_limit)

def delete_budget(category):
    data = load_data()
    if category not in data["budgets"]:
        print(f"  ERROR! No budget found for '{category}'.")
        return False
    del data["budgets"][category]
    save_data(data)
    print(f"  OK! Budget for '{category}' removed.")
    return True

def _get_spent(category, year, month):
    txns = filter_by_month(year, month)
    return round(sum(
        t["amount"] for t in txns
        if t["type"] == "expense" and t["category"] == category), 2)

def check_budget_status(year=None, month=None):
    now = datetime.now()
    year  = year  or now.year
    month = month or now.month
    data = load_data()
    budgets = data["budgets"]
    results = []
    for cat, limit in budgets.items():
        spent     = _get_spent(cat, year, month)
        remaining = round(limit - spent, 2)
        pct       = round((spent / limit * 100) if limit > 0 else 0, 1)
        if pct >= 100:
            status = "exceeded"
        elif pct >= 80:
            status = "warning"
        else:
            status = "ok"
        results.append({
            "category": cat, "limit": limit,
            "spent": spent, "remaining": remaining,
            "percent_used": pct, "status": status})
    return sorted(results, key=lambda x: x["percent_used"], reverse=True)

def remaining_budget(category, year=None, month=None):
    now   = datetime.now()
    year  = year  or now.year
    month = month or now.month
    data  = load_data()
    limit = data["budgets"].get(category)
    if limit is None:
        return None
    spent = _get_spent(category, year, month)
    return round(limit - spent, 2)

def print_budget_status(year=None, month=None):
    MONTH_NAMES = [
        "", "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"]
    now   = datetime.now()
    year  = year  or now.year
    month = month or now.month
    statuses = check_budget_status(year, month)
    if not statuses:
        print("  INFO! No budgets set. Use 'Set Budget' to add limits.")
        return
    print(f"\n    Budget Status - {MONTH_NAMES[month]} {year}")
    print(f"  {'Category':<16} {'Spent':>10} {'Limit':>10} {'Remaining':>10}  {'Used%':>6}  Status")
    print("  " + "-" * 72)
    for s in statuses:
        label = (
            "On Track"   if s["status"] == "ok"
            else "Near Limit" if s["status"] == "warning"
            else f"EXCEEDED Rs.{abs(s['remaining']):.2f}")
        print(
            f"  {s['category']:<16} Rs.{s['spent']:>8.2f} Rs.{s['limit']:>8.2f} "
            f"Rs.{s['remaining']:>8.2f}  {s['percent_used']:>5.1f}%  {label}")
    print("  " + "-" * 72 + "\n")