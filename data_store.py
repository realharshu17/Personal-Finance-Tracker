import json
import os
import shutil
from datetime import datetime
DATA_FILE = "finance_data.json"
BACKUP_DIR = "backups"
DEFAULT_DATA = {
    "transactions": [],
    "categories": {
        "income": ["Salary", "Allowance", "Freelance", "Gift", "Other"],
        "expense": ["Food", "Transport", "Education", "Healthcare",
                    "Entertainment", "Shopping", "Utilities", "Other"]
    },
    "budgets": {}}

def initialize_store():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump(DEFAULT_DATA, f, indent=4)
        print("  INFO! Data store initialized with default settings.")

    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)

def load_data():
    initialize_store()
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
        for key in DEFAULT_DATA:
            if key not in data:
                data[key] = DEFAULT_DATA[key]
        return data
    except (json.JSONDecodeError, IOError) as e:
        print(f"  ERROR! Could not load data: {e}. Restoring defaults.")
        return dict(DEFAULT_DATA)

def save_data(data):
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"  ERROR! Could not save data: {e}")

def backup_data():
    if not os.path.exists(DATA_FILE):
        print("  WARNING! No data file found to backup.")
        return
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = os.path.join(BACKUP_DIR, f"finance_data_backup_{timestamp}.json")
    shutil.copy2(DATA_FILE, backup_file)
    print(f"  INFO! Backup created: {backup_file}")

def restore_backup():
    if not os.path.exists(BACKUP_DIR):
        print("  INFO! No backups directory found.")
        return
    backups = sorted([
        f for f in os.listdir(BACKUP_DIR) if f.endswith(".json")
    ], reverse=True)
    if not backups:
        print("  INFO! No backup files found.")
        return
    print("\n  Available Backups:")
    for i, b in enumerate(backups, 1):
        print(f"    [{i}] {b}")
    choice = input("\n  Enter backup number to restore (0 to cancel): ").strip()
    if choice == "0":
        return
    try:
        idx = int(choice) - 1
        chosen = os.path.join(BACKUP_DIR, backups[idx])
        shutil.copy2(chosen, DATA_FILE)
        print(f"  INFO! Restored from: {backups[idx]}")
    except (ValueError, IndexError):
        print("  ERROR! Invalid selection.")

def validate_data(data):
    required_keys = ["transactions", "categories", "budgets"]
    for key in required_keys:
        if key not in data:
            return False
    if "income" not in data["categories"] or "expense" not in data["categories"]:
        return False
    return True