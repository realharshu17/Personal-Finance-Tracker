# Personal Finance Tracker

A terminal-based personal finance management application written in Python.
Track your income and expenses, manage budgets, analyse spending patterns,
and export financial reports — all from the command line.
No third-party libraries required.

---

## Features

| Module | Capabilities |
|---|---|
| **Transactions** | Add, edit, delete, view, filter by date / type / month, keyword search |
| **Categories** | Create and manage custom income and expense categories; rename with automatic transaction migration |
| **Analytics** | Monthly summaries, top spending categories, spending trends, income/expense ratio, daily averages |
| **Budget Manager** | Set per-category monthly budgets, track usage %, On Track / Near Limit / Exceeded status |
| **Reports & Export** | View formatted reports in terminal; export `.txt` reports and `.csv` transaction dumps |
| **Backup & Restore** | Timestamped JSON backups with an interactive restore menu |

---

## Project Structure

```
Personal Finance Tracker/
|
|-- main.py               # Entry point - CLI menus and user interaction
|-- data_store.py         # JSON persistence, backup and restore
|-- transaction.py        # CRUD operations and filters for transactions
|-- category_manager.py   # Category management (add, delete, rename, validate)
|-- analytics.py          # Summaries, trends, ratios, and spending analytics
|-- budget.py             # Budget setting, status checks, remaining calculation
|-- report.py             # Report generation, .txt and .csv export
|
|-- finance_data.json     # Auto-generated data store (do not edit manually)
|-- backups/              # Auto-created - timestamped backup files
`-- reports/              # Auto-created - exported .txt and .csv files
```

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- No `pip install` required — standard library only

### Running the App

Always run from **inside** the project folder so data files are created in the right place:

```bash
cd "Personal Finance Tracker"
python main.py
```

---

## Usage Guide

### Main Menu

```
MAIN MENU:
1. Transactions
2. Categories
3. Analytics & Insights
4. Budget Manager
5. Reports & Export
6. Backup Data
7. Restore Backup
0. Exit
```

### Adding a Transaction

1. Select `1. Transactions` then `1. Add Transaction`
2. Enter type: `income` or `expense`
3. Enter a positive amount
4. Select a category from the displayed list
5. Enter date in `YYYY-MM-DD` format (press Enter for today)
6. Optionally add a short note

### Default Categories

| Income | Expense |
|---|---|
| Salary | Food |
| Allowance | Transport |
| Freelance | Education |
| Gift | Healthcare |
| Other | Entertainment |
| | Shopping |
| | Utilities |
| | Other |

You can add, rename, or delete categories from the **Categories** menu.

### Setting a Budget

1. Select `4. Budget Manager` then `2. Set / Update Budget`
2. Enter a category name
3. Enter a monthly limit amount

Budget statuses:

| Status | Meaning |
|---|---|
| On Track | Less than 80% of budget used |
| Near Limit | 80–99% of budget used |
| EXCEEDED | Over 100% of budget used |

### Exporting Data

| Menu Option | Output File |
|---|---|
| Export Monthly Report `.txt` | `reports/report_YYYY_MM.txt` |
| Export All Transactions `.csv` | `reports/transactions_all_YYYYMMDD.csv` |
| Export Monthly Transactions `.csv` | `reports/transactions_YYYY_MM.csv` |

---

## Data Storage

All data is stored locally in `finance_data.json`:

```json
{
    "transactions": [
        {
            "id": 1,
            "type": "income",
            "amount": 3000.00,
            "category": "Salary",
            "date": "2026-09-26",
            "note": "September salary"
        }
    ],
    "categories": {
        "income": ["Salary", "Allowance", "Freelance", "Gift", "Other"],
        "expense": ["Food", "Transport", "Education", "Healthcare",
                    "Entertainment", "Shopping", "Utilities", "Other"]
    },
    "budgets": {
        "Food": 5000.00
    }
}
```

> Do not edit `finance_data.json` manually. Use the Backup option before making any significant changes.

---

## Backup & Restore

**Backup:** Select `6. Backup Data` from the main menu. A timestamped copy is saved to:
```
backups/finance_data_backup_YYYYMMDD_HHMMSS.json
```

**Restore:** Select `7. Restore Backup` to view all backups sorted by most recent first. Enter a number to restore.

---

## Module Reference

### `data_store.py`

| Function | Description |
|---|---|
| `initialize_store()` | Creates the data file and backup directory if they do not exist |
| `load_data()` | Reads the data store and merges any missing default keys |
| `save_data(data)` | Writes updated data back to the JSON file |
| `backup_data()` | Creates a timestamped backup copy of the data file |
| `restore_backup()` | Interactive restore menu from available backup files |
| `validate_data(data)` | Checks required top-level keys and category sub-keys exist |

### `transaction.py`

| Function | Description |
|---|---|
| `add_transaction(type, amount, category, date, note)` | Creates and saves a new transaction |
| `edit_transaction(txn_id, **kwargs)` | Updates one or more fields of an existing transaction |
| `delete_transaction(txn_id)` | Removes a transaction by ID |
| `list_transactions(transactions)` | Prints a formatted table of transactions |
| `filter_by_date(start, end)` | Returns transactions within a date range |
| `filter_by_type(type)` | Returns only income or expense transactions |
| `filter_by_month(year, month)` | Returns transactions for a specific month |
| `search_by_keyword(keyword)` | Searches transaction notes for a keyword |
| `get_transaction_by_id(txn_id)` | Returns a single transaction dict by ID |

### `analytics.py`

| Function | Description |
|---|---|
| `monthly_summary(year, month)` | Returns income, expense, savings, and savings rate |
| `top_spending_categories(year, month, top_n)` | Ranked list of highest expense categories |
| `spending_trend(year, month)` | Compares current month spending to the previous month |
| `find_highest_expense()` | Returns the single largest expense transaction ever |
| `income_vs_expense_ratio()` | All-time income vs expense ratio |
| `daily_average_spend(year, month)` | Average daily expense for a given month |
| `savings_rate(year, month)` | Returns the savings rate percentage for a given month |
| `print_monthly_summary(year, month)` | Prints a formatted summary table to the terminal |

### `budget.py`

| Function | Description |
|---|---|
| `set_budget(category, limit)` | Sets or updates a monthly budget limit for a category |
| `update_budget(category, new_limit)` | Updates an existing budget; creates one if it doesn't exist |
| `delete_budget(category)` | Removes a budget entry |
| `check_budget_status(year, month)` | Returns status objects for all budgets |
| `remaining_budget(category, year, month)` | Returns remaining budget for a specific category |
| `print_budget_status(year, month)` | Prints a formatted budget status table |

### `category_manager.py`

| Function | Description |
|---|---|
| `list_categories()` | Prints all income and expense categories |
| `add_category(type, name)` | Adds a new category to income or expense |
| `delete_category(type, name)` | Removes a category (the "Other" category is protected) |
| `rename_category(type, old, new)` | Renames a category; migrates all transactions and budgets |
| `validate_category(type, name)` | Returns `True` if a category name is valid |
| `get_category_total(name)` | Total transaction amount across all time for a category |
| `get_all_categories()` | Returns a flat list of all income and expense categories |

### `report.py`

| Function | Description |
|---|---|
| `generate_monthly_report(year, month)` | Builds and returns a full monthly report as a string |
| `export_to_txt(content, filename)` | Saves a report string to a `.txt` file in the `reports/` directory |
| `export_to_csv(year, month)` | Exports transactions to a `.csv` file in the `reports/` directory |
| `print_formatted_table(data_list, headers, keys)` | Utility to print any list of dicts as a formatted table |

---

## Requirements

```
Python >= 3.8

Standard library modules used:
  json, os, csv, shutil, datetime, calendar
```

No `pip install` required. Works out of the box on any platform.

---

*Personal Finance Tracker — README updated 2026-09-26*
