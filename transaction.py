from datetime import datetime
from data_store import load_data, save_data
from category_manager import validate_category

def _next_id(transactions):
    if not transactions:
        return 1
    return max(t["id"] for t in transactions) + 1

def _format_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return date_str
    except ValueError:
        return None

def add_transaction(txn_type, amount, category, date_str, note=""):
    if txn_type not in ("income", "expense"):
        print("  ERROR! Type must be 'income' or 'expense'.")
        return None
    try:
        amount = round(float(amount), 2)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print("  ERROR! Amount must be a positive number.")
        return None
    date = _format_date(date_str)
    if not date:
        print("  ERROR! Date must be in YYYY-MM-DD format.")
        return None
    if not validate_category(txn_type, category):
        print(f"  ERROR! Category '{category}' not found under {txn_type}.")
        return None
    data = load_data()
    txn = {
        "id": _next_id(data["transactions"]),
        "type": txn_type,
        "amount": amount,
        "category": category,
        "date": date,
        "note": note.strip()}
    data["transactions"].append(txn)
    save_data(data)
    print(f"  OK! Transaction #{txn['id']} added successfully.")
    return txn

def edit_transaction(txn_id, **kwargs):
    data = load_data()
    txn = next((t for t in data["transactions"] if t["id"] == txn_id), None)
    if not txn:
        print(f"  ERROR! Transaction #{txn_id} not found.")
        return False
    if "amount" in kwargs:
        try:
            amt = round(float(kwargs["amount"]), 2)
            if amt <= 0:
                raise ValueError
            txn["amount"] = amt
        except ValueError:
            print("  ERROR! Invalid amount.")
            return False
    if "date" in kwargs:
        date = _format_date(kwargs["date"])
        if not date:
            print("  ERROR! Invalid date format.")
            return False
        txn["date"] = date
    if "note" in kwargs:
        txn["note"] = kwargs["note"].strip()
    if "category" in kwargs:
        if not validate_category(txn["type"], kwargs["category"]):
            print(f"  ERROR! Category '{kwargs['category']}' not valid.")
            return False
        txn["category"] = kwargs["category"]
    save_data(data)
    print(f"  OK! Transaction #{txn_id} updated.")
    return True

def delete_transaction(txn_id):
    data = load_data()
    original_count = len(data["transactions"])
    data["transactions"] = [t for t in data["transactions"] if t["id"] != txn_id]
    if len(data["transactions"]) == original_count:
        print(f"  ERROR! Transaction #{txn_id} not found.")
        return False
    save_data(data)
    print(f"  OK! Transaction #{txn_id} deleted.")
    return True

def list_transactions(transactions=None):
    if transactions is None:
        data = load_data()
        transactions = data["transactions"]
    if not transactions:
        print("  INFO! No transactions found.")
        return
    print(f"\n  {'ID':<5} {'Date':<12} {'Type':<9} {'Category':<16} {'Amount':>10}  Note")
    print("  " + "-" * 65)
    for t in sorted(transactions, key=lambda x: x["date"], reverse=True):
        symbol = "+" if t["type"] == "income" else "-"
        print(
            f"  {t['id']:<5} {t['date']:<12} {t['type'].capitalize():<9} "
            f"{t['category']:<16} {symbol}Rs.{t['amount']:>8.2f}  {t['note']}"
        )
    print("  " + "-" * 65)
    print(f"  Total entries: {len(transactions)}\n")

def filter_by_date(start_date, end_date):
    data = load_data()
    result = [
        t for t in data["transactions"]
        if start_date <= t["date"] <= end_date]
    return result

def filter_by_type(txn_type):
    data = load_data()
    return [t for t in data["transactions"] if t["type"] == txn_type]

def filter_by_month(year, month):
    prefix = f"{year:04d}-{month:02d}"
    data = load_data()
    return [t for t in data["transactions"] if t["date"].startswith(prefix)]

def search_by_keyword(keyword):
    data = load_data()
    kw = keyword.lower()
    return [t for t in data["transactions"] if kw in t["note"].lower()]

def get_transaction_by_id(txn_id):
    data = load_data()
    return next((t for t in data["transactions"] if t["id"] == txn_id), None)