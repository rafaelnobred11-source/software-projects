"""Compare payroll exports using SQLite and exact integer cents."""

import argparse
import csv
import sqlite3
from contextlib import closing
from decimal import Decimal, InvalidOperation
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KEY = ("company", "period", "employee_id", "pay_code")
HEADERS = (*KEY, "amount")


def read_export(path):
    """Read one record per company, period, employee, and pay code."""
    records = {}
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != list(HEADERS):
            raise ValueError(f"{path}: expected columns {', '.join(HEADERS)}")
        for row in reader:
            location = f"{path}:{reader.line_num}"
            if None in row or any(row[field] is None for field in HEADERS):
                raise ValueError(f"{location}: wrong number of columns")
            key = tuple(row[field].strip() for field in KEY)
            if not all(key):
                raise ValueError(f"{location}: key fields must be populated")
            if key in records:
                raise ValueError(f"{location}: duplicate key {key}")
            try:
                amount = Decimal(row["amount"].strip())
                if not amount.is_finite() or abs(amount) > Decimal("999999999999.99"):
                    raise ValueError
                cents = amount * 100
                if cents != cents.to_integral_value():
                    raise ValueError
            except (InvalidOperation, ValueError):
                raise ValueError(f"{location}: use a decimal amount with at most two places") from None
            records[key] = int(cents)
    return [(*key, cents) for key, cents in records.items()]


def reconcile(expected, actual):
    query = (ROOT / "payroll_reconciliation.sql").read_text(encoding="utf-8-sig")
    with closing(sqlite3.connect(":memory:")) as db:
        schema = """
            (company TEXT, period TEXT, employee_id TEXT, pay_code TEXT, cents INTEGER,
             PRIMARY KEY (company, period, employee_id, pay_code))
        """
        db.execute("CREATE TABLE expected " + schema)
        db.execute("CREATE TABLE actual " + schema)
        db.executemany("INSERT INTO expected VALUES (?, ?, ?, ?, ?)", expected)
        db.executemany("INSERT INTO actual VALUES (?, ?, ?, ?, ?)", actual)
        cursor = db.execute(query)
        return [column[0] for column in cursor.description], cursor.fetchall()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("expected", nargs="?", type=Path, default=ROOT / "sample_expected.csv")
    parser.add_argument("actual", nargs="?", type=Path, default=ROOT / "sample_actual.csv")
    parser.add_argument("-o", "--output", type=Path, default=Path("reconciliation.csv"))
    args = parser.parse_args()
    try:
        if args.output.resolve() in {args.expected.resolve(), args.actual.resolve()}:
            raise ValueError("output must be different from both input files")
        headers, rows = reconcile(read_export(args.expected), read_export(args.actual))
        with args.output.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(headers)
            writer.writerows(rows)
    except (OSError, ValueError, csv.Error, sqlite3.Error) as error:
        parser.exit(1, f"Error: {error}\n")
    print(f"Wrote {len(rows)} exceptions to {args.output}")


if __name__ == "__main__":
    main()
