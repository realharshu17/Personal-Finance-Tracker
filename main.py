from datetime import datetime
from data_store import initialize_store, backup_data, restore_backup
from transaction import (
    add_transaction, edit_transaction, delete_transaction, list_transactions, filter_by_date,
    filter_by_type, filter_by_month, search_by_keyword, get_transaction_by_id)

from category_manager import (
    list_categories, add_category, delete_category,
    rename_category, get_category_total)

from analytics import (
    print_monthly_summary, spending_trend, find_highest_expense,
    income_vs_expense_ratio, daily_average_spend)

from budget import set_budget, update_budget, delete_budget, print_budget_status
from report import (
    generate_monthly_report,
    export_to_txt, export_to_csv)

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]


def prompt_int(msg, min_val=None, max_val=None):
    while True:
        try:
            val = int(input(f"  {msg}: ").strip())
            if (min_val is not None and val < min_val) or \
               (max_val is not None and val > max_val):
                print(f"  ERROR! Enter a value between {min_val} and {max_val}.")
                continue
            return val
        except ValueError:
            print("  ERROR! Please enter a valid number.")

def prompt_float(msg):
    while True:
        try:
            val = float(input(f"  {msg}: ").strip())
            if val <= 0:
                raise ValueError
            return val
        except ValueError:
            print("  ERROR! Enter a positive number.")

def prompt_date(msg="Date (YYYY-MM-DD) [Enter for today]"):
    while True:
        raw = input(f"  {msg}: ").strip()
        if not raw:
            return datetime.now().strftime("%Y-%m-%d")
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  ERROR! Use format YYYY-MM-DD (e.g. 2026-09-15).")

def prompt_month_year():
    now = datetime.now()
    year  = prompt_int(f"Year  [Enter blank for {now.year}]" , min_val=2000, max_val=2100) \
            if input(f"  Year  [{now.year}] (press Enter to use current): ").strip() \
            else now.year
    month = prompt_int(f"Month (1-12) [Enter blank for {now.month}]", min_val=1, max_val=12) \
            if input(f"  Month [{now.month}] (press Enter to use current): ").strip() \
            else now.month
    return year, month

def clear():
    print("\n" + "-" * 55 + "\n")

def banner():
    print("  Personal Finance Tracker:  ")


def menu_transactions():
    while True:
        clear()
        print("TRANSACTIONS:")
        print("1. Add Transaction")
        print("2. View All Transactions")
        print("3. Edit Transaction")
        print("4. Delete Transaction")
        print("5. Filter by Date Range")
        print("6. Filter by Type (Income/Expense)")
        print("7. Filter by Month")
        print("8. Search by Keyword")
        print("0. Back to Main Menu")
        choice = input("  Choose: ").strip()
        if choice == "1":
            clear()
            print(" ADD TRANSACTION : ")
            txn_type = input("  Type (income/expense): ").strip().lower()
            amount   = prompt_float("Amount (Rs.)")
            list_categories()
            category = input("  Category: ").strip()
            date     = prompt_date()
            note     = input("  Note (optional): ").strip()
            add_transaction(txn_type, amount, category, date, note)
        elif choice == "2":
            clear()
            list_transactions()
        elif choice == "3":
            clear()
            txn_id = prompt_int("Transaction ID to edit", min_val=1)
            txn = get_transaction_by_id(txn_id)
            if not txn:
                print(f"  ERROR! Transaction #{txn_id} not found.")
            else:
                print(f"  Current: {txn}")
                print("  (Press Enter to keep existing value)")
                kwargs = {}
                amt  = input("  New Amount (Rs.): ").strip()
                if amt: kwargs["amount"] = amt
                cat  = input("  New Category: ").strip()
                if cat: kwargs["category"] = cat
                dt   = input("  New Date (YYYY-MM-DD): ").strip()
                if dt:  kwargs["date"] = dt
                note = input("  New Note: ").strip()
                if note: kwargs["note"] = note
                edit_transaction(txn_id, **kwargs)
        elif choice == "4":
            clear()
            txn_id = prompt_int("Transaction ID to delete", min_val=1)
            confirm = input(f"  Confirm delete #{txn_id}? (yes/no): ").strip().lower()
            if confirm == "yes":
                delete_transaction(txn_id)
            else:
                print("  Cancelled.")
        elif choice == "5":
            clear()
            start = prompt_date("Start date")
            end   = prompt_date("End date")
            results = filter_by_date(start, end)
            list_transactions(results)
        elif choice == "6":
            clear()
            txn_type = input("  Type (income/expense): ").strip().lower()
            results  = filter_by_type(txn_type)
            list_transactions(results)
        elif choice == "7":
            clear()
            now   = datetime.now()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            results = filter_by_month(year, month)
            list_transactions(results)
        elif choice == "8":
            clear()
            kw = input("  Keyword: ").strip()
            results = search_by_keyword(kw)
            list_transactions(results)
        elif choice == "0":
            break
        else:
            print("  ERROR! Invalid choice.")
        input("\n  Press Enter to continue...")

def menu_categories():
    while True:
        clear()
        print("CATEGORIES:")
        print("1. View All Categories")
        print("2. Add Category")
        print("3. Delete Category")
        print("4. Rename Category")
        print("5. Total Spent in Category")
        print("0. Back to Main Menu")
        choice = input("  Choose: ").strip()
        if choice == "1":
            clear()
            list_categories()
        elif choice == "2":
            clear()
            cat_type = input("  Type (income/expense): ").strip().lower()
            name     = input("  Category name: ").strip()
            add_category(cat_type, name)
        elif choice == "3":
            clear()
            list_categories()
            cat_type = input("  Type (income/expense): ").strip().lower()
            name     = input("  Category name to delete: ").strip()
            delete_category(cat_type, name)
        elif choice == "4":
            clear()
            list_categories()
            cat_type = input("  Type (income/expense): ").strip().lower()
            old_name = input("  Current name: ").strip()
            new_name = input("  New name: ").strip()
            rename_category(cat_type, old_name, new_name)
        elif choice == "5":
            clear()
            name  = input("  Category name: ").strip()
            total = get_category_total(name)
            print(f"\n  Total transactions in '{name}': Rs.{total:.2f}")
        elif choice == "0":
            break
        else:
            print("  ERROR! Invalid choice.")
        input("\n  Press Enter to continue...")

def menu_analytics():
    while True:
        clear()
        print("ANALYTICS & INSIGHTS:")
        print("1. Monthly Summary")
        print("2. Spending Trend (vs Previous Month)")
        print("3. Highest Single Expense")
        print("4. Income vs Expense Ratio (All Time)")
        print("5. Daily Average Spend")
        print("0. Back to Main Menu")
        choice = input("  Choose: ").strip()
        if choice == "1":
            clear()
            now   = datetime.now()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            print_monthly_summary(year, month)
        elif choice == "2":
            clear()
            now   = datetime.now()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            t = spending_trend(year, month)
            print(f"\n  Spending {MONTH_NAMES[month]} vs previous month:")
            print(f"  Current : Rs.{t['current']:.2f}")
            print(f"  Previous: Rs.{t['previous']:.2f}")
            print(f"  Trend   : {t['trend'].upper()} by Rs.{t['difference']:.2f}")
        elif choice == "3":
            clear()
            h = find_highest_expense()
            if h:
                print(f"\n   Highest Single Expense:")
                print(f"     Amount  : Rs.{h['amount']:.2f}")
                print(f"     Category: {h['category']}")
                print(f"     Date    : {h['date']}")
                print(f"     Note    : {h['note']}")
            else:
                print("  INFO! No expenses recorded yet.")
        elif choice == "4":
            clear()
            r = income_vs_expense_ratio()
            print(f"\n  All-Time Summary:")
            print(f"  Total Income : Rs.{r['total_income']:.2f}")
            print(f"  Total Expense: Rs.{r['total_expense']:.2f}")
            ratio_str = f"{r['ratio']:.2f}" if r['ratio'] != float('inf') else "inf (No expenses)"
            print(f"  I/E Ratio    : {ratio_str}")
        elif choice == "5":
            clear()
            now   = datetime.now()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            avg   = daily_average_spend(year, month)
            print(f"\n  Avg Daily Spend ({MONTH_NAMES[month]} {year}): Rs.{avg:.2f}")
        elif choice == "0":
            break
        else:
            print("  ERROR! Invalid choice.")
        input("\n  Press Enter to continue...")

def menu_budget():
    while True:
        clear()
        print("BUDGET MANAGER:")
        print("1. View Budget Status")
        print("2. Set / Update Budget")
        print("3. Delete Budget")
        print("0. Back to Main Menu")
        choice = input("  Choose: ").strip()
        if choice == "1":
            clear()
            now   = datetime.now()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            print_budget_status(year, month)
        elif choice == "2":
            clear()
            list_categories()
            cat   = input("  Category name: ").strip()
            limit = prompt_float("Monthly limit (Rs.)")
            set_budget(cat, limit)
        elif choice == "3":
            clear()
            cat = input("  Category name to remove budget: ").strip()
            delete_budget(cat)
        elif choice == "0":
            break
        else:
            print("  ERROR! Invalid choice.")
        input("\n  Press Enter to continue...")

def menu_reports():
    while True:
        clear()
        print("REPORTS:")
        print("1. View Monthly Report (Terminal)")
        print("2. Export Monthly Report (.txt)")
        print("3. Export All Transactions (.csv)")
        print("4. Export Monthly Transactions (.csv)")
        print("0. Back to Main Menu")
        choice = input("  Choose: ").strip()
        now = datetime.now()
        if choice == "1":
            clear()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            print(generate_monthly_report(year, month))
        elif choice == "2":
            clear()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            content = generate_monthly_report(year, month)
            fname   = f"report_{year}_{month:02d}.txt"
            export_to_txt(content, fname)
        elif choice == "3":
            clear()
            export_to_csv()
        elif choice == "4":
            clear()
            year  = prompt_int(f"Year  [{now.year}]", min_val=2000, max_val=2100)
            month = prompt_int(f"Month [{now.month}] (1-12)", min_val=1, max_val=12)
            export_to_csv(year, month)
        elif choice == "0":
            break
        else:
            print("  ERROR! Invalid choice.")
        input("\n  Press Enter to continue...")


def main():
    initialize_store()
    banner()
    while True:
        print("MAIN MENU:")
        print("1. Transactions")
        print("2. Categories")
        print("3. Analytics & Insights")
        print("4. Budget Manager")
        print("5. Reports & Export")
        print("6. Backup Data")
        print("7. Restore Backup")
        print("0. Exit")
        choice = input("  Choose: ").strip()
        if   choice == "1": menu_transactions()
        elif choice == "2": menu_categories()
        elif choice == "3": menu_analytics()
        elif choice == "4": menu_budget()
        elif choice == "5": menu_reports()
        elif choice == "6":
            backup_data()
            input("\n  Press Enter to continue...")
        elif choice == "7":
            restore_backup()
            input("\n  Press Enter to continue...")
        elif choice == "0":
            print("\n  Goodbye! Stay financially fit.\n")
            break
        else:
            print("  ERROR! Invalid choice. Try again.")

        banner()

if __name__ == "__main__":
    main()