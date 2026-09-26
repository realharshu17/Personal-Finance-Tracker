import os
import csv
from datetime import datetime
from analytics import monthly_summary, top_spending_categories, income_vs_expense_ratio
from transaction import filter_by_month
from data_store import load_data
REPORTS_DIR = "reports"
MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"]

def _ensure_reports_dir():
    """Make sure the reports directory exists."""
    if not os.path.exists(REPORTS_DIR):
        os.makedirs(REPORTS_DIR)

def generate_monthly_report(year, month):
    """Build and return a full monthly report as a string."""
    s    = monthly_summary(year, month)
    txns = filter_by_month(year, month)
    tops = top_spending_categories(year, month)
    trend_line = income_vs_expense_ratio()
    lines = []
    lines.append("=" * 52)
    lines.append(f"  PERSONAL FINANCE REPORT")
    lines.append(f"  Period : {MONTH_NAMES[month]} {year}")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 52)
    lines.append(f"  Income      : Rs. {s['income']:>10.2f}")
    lines.append(f"  Expenses    : Rs. {s['expense']:>10.2f}")
    lines.append(f"  Net Savings : Rs. {s['savings']:>10.2f}")
    lines.append(f"  Savings Rate:  {s['savings_rate']:>9.1f}%")
    lines.append("-" * 52)
    if tops:
        lines.append("  Category Breakdown (Top Expenses):")
        for entry in tops:
            lines.append(
                f"    {entry['category']:<18} Rs.{entry['amount']:>8.2f}  "
                f"({entry['percentage']}%)")
        lines.append("-" * 52)
    lines.append(f"  Transactions ({len(txns)} entries):")
    lines.append(f"  {'ID':<5} {'Date':<12} {'Type':<9} {'Cat':<14} {'Amount':>10}  Note")
    lines.append("  " + "-" * 60)
    for t in sorted(txns, key=lambda x: x["date"]):
        sym = "+" if t["type"] == "income" else "-"
        lines.append(
            f"  [{t['id']:<4}] {t['date']:<12} {t['type'].capitalize():<9} "
            f"{t['category']:<14} {sym}Rs.{t['amount']:>8.2f}  {t['note']}")
    lines.append("=" * 52)
    return "\n".join(lines)

def export_to_txt(content, filename):
    """Save report content as a .txt file in the reports directory."""
    _ensure_reports_dir()
    filepath = os.path.join(REPORTS_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  OK! Report saved to: {filepath}")
    return filepath

def export_to_csv(year=None, month=None):
    _ensure_reports_dir()
    data = load_data()
    txns = data["transactions"]
    if year and month:
        prefix = f"{year:04d}-{month:02d}"
        txns = [t for t in txns if t["date"].startswith(prefix)]
        fname = f"transactions_{year}_{month:02d}.csv"
    else:
        fname = f"transactions_all_{datetime.now().strftime('%Y%m%d')}.csv"
    filepath = os.path.join(REPORTS_DIR, fname)
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "type", "amount", "category", "date", "note"])
        writer.writeheader()
        for t in sorted(txns, key=lambda x: x["date"]):
            writer.writerow(t)
    print(f"  OK! CSV exported to: {filepath}  ({len(txns)} records)")
    return filepath

def print_formatted_table(data_list, headers, keys):
    col_widths = [max(len(str(h)), max((len(str(row.get(k, ""))) for row in data_list), default=0))
                  for h, k in zip(headers, keys)]
    row_fmt = "  " + "  ".join(f"{{:<{w}}}" for w in col_widths)
    print("\n" + row_fmt.format(*headers))
    print("  " + "-" * (sum(col_widths) + 2 * len(col_widths)))
    for row in data_list:
        print(row_fmt.format(*[str(row.get(k, "")) for k in keys]))
    print()