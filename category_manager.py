from data_store import load_data, save_data

def list_categories():
    data = load_data()
    cats = data["categories"]
    print("   CATEGORIES   ")
    print(" INCOME: ")
    for i, c in enumerate(cats["income"], 1):
        print(f"      {i}. {c}")
    print(" EXPENSE: ")
    for i, c in enumerate(cats["expense"], 1):
        print(f"      {i}. {c}")

def add_category(cat_type, name):
    if cat_type not in ("income", "expense"):
        print("  ERROR! Type must be 'income' or 'expense'.")
        return False
    data = load_data()
    cats = data["categories"][cat_type]
    if name in cats:
        print(f"  WARNING! Category '{name}' already exists.")
        return False
    cats.append(name)
    save_data(data)
    print(f"  OK! Category '{name}' added to {cat_type}.")
    return True

def delete_category(cat_type, name):
    if name == "Other":
        print("  ERROR! Cannot delete the 'Other' category.")
        return False
    data = load_data()
    cats = data["categories"].get(cat_type, [])
    if name not in cats:
        print(f"  ERROR! Category '{name}' not found.")
        return False
    cats.remove(name)
    save_data(data)
    print(f"  OK! Category '{name}' removed.")
    return True

def rename_category(cat_type, old_name, new_name):
    data = load_data()
    cats = data["categories"].get(cat_type, [])
    if old_name not in cats:
        print(f"  ERROR! Category '{old_name}' not found.")
        return False
    if new_name in cats:
        print(f"  ERROR! Category '{new_name}' already exists.")
        return False
    idx = cats.index(old_name)
    cats[idx] = new_name
    for txn in data["transactions"]:
        if txn["category"] == old_name:
            txn["category"] = new_name
    if old_name in data["budgets"]:
        data["budgets"][new_name] = data["budgets"].pop(old_name)
    save_data(data)
    print(f"  OK! Renamed '{old_name}' to '{new_name}'.")
    return True

def get_category_total(cat_name):
    data = load_data()
    total = sum(t["amount"] for t in data["transactions"] if t["category"] == cat_name)
    return round(total, 2)

def validate_category(cat_type, name):
    data = load_data()
    return name in data["categories"].get(cat_type, [])

def get_all_categories():
    data = load_data()
    return data["categories"]["income"] + data["categories"]["expense"]