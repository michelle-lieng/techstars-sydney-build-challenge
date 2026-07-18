"""
Bulk-load founder profiles from a CSV into the database.

Usage (run from the `server/` directory):
    python insertCsv.py path/to/founders.csv           # append rows
    python insertCsv.py path/to/founders.csv --fresh    # drop table first, then load

CSV header names must match the field names below. Columns the loader doesn't
recognize are reported and skipped. Empty cells become NULL.
"""
import os
import sys
import csv
import json
import argparse
from flask import Flask
from dotenv import load_dotenv
from mysqlSchema import FounderProfileDB

load_dotenv()

# Columns that must be interpreted as true/false rather than plain strings.
BOOL_FIELDS = {
    "is_current_founder", "ai_in_curr_startup", "was_prev_founder",
    "was_in_accelerator", "was_in_scaleup", "was_in_bigtech",
    "migrant", "is_stealth",
}
# Columns stored as JSON arrays (insertFounder json.dumps them).
JSON_LIST_FIELDS = {
    "all_founded_companies", "accelerators_worked_in",
    "scaleups_worked_in", "bigtechs_worked_in",
}
INT_FIELDS = {"linkedin_follower_count"}

# Every keyword insertFounder accepts. Anything else in the CSV is ignored.
VALID_FIELDS = {
    "name", "linkedin_url", "city", "current_company", "current_title",
    "current_job_start", "time_in_current_role", "is_current_founder",
    "curr_startup_funding_stage", "curr_startup_url", "curr_startup_info",
    "curr_startup_industry", "ai_in_curr_startup", "was_prev_founder",
    "all_founded_companies", "top_degree", "top_degree_label",
    "top_degree_end_date", "top_institution", "was_in_accelerator",
    "accelerators_worked_in", "was_in_scaleup", "scaleups_worked_in",
    "was_in_bigtech", "bigtechs_worked_in", "gender", "migrant",
    "is_stealth", "linkedin_follower_count", "founder_persona",
}


def parse_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")


def coerce(field, raw):
    value = (raw or "").strip()
    if value == "":
        return None
    if field in BOOL_FIELDS:
        return parse_bool(value)
    if field in INT_FIELDS:
        try:
            return int(float(value))
        except ValueError:
            return 0
    if field in JSON_LIST_FIELDS:
        # Accept a JSON array string ("[...]") or a plain string; store as a list.
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else [parsed]
        except (json.JSONDecodeError, TypeError):
            return [value]
    return value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv_path", help="Path to the CSV file")
    ap.add_argument("--fresh", action="store_true",
                    help="Drop and recreate the table before loading (DESTRUCTIVE)")
    args = ap.parse_args()

    if not os.path.exists(args.csv_path):
        sys.exit(f"CSV not found: {args.csv_path}")

    app = Flask(__name__)
    db = FounderProfileDB(app=app, password=os.getenv("DB_PASSWORD"))

    if args.fresh:
        print("--fresh: dropping and recreating founder_profile table")
        db.dropFounderTable()
        db.createFounderProfileTable()

    inserted, failed = 0, 0
    # utf-8-sig strips the BOM Excel adds to CSV exports.
    with open(args.csv_path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        unknown = [c for c in (reader.fieldnames or []) if c not in VALID_FIELDS]
        if unknown:
            print(f"WARNING: ignoring unrecognized columns: {unknown}")
        if "name" not in (reader.fieldnames or []):
            sys.exit("CSV must have a 'name' column.")

        for i, row in enumerate(reader, start=2):  # row 1 is the header
            kwargs = {f: coerce(f, row.get(f)) for f in VALID_FIELDS if f in row}
            if not kwargs.get("name"):
                print(f"Row {i}: skipped (no name)")
                continue
            try:
                db.insertFounder(**kwargs)
                inserted += 1
            except Exception as e:
                failed += 1
                print(f"Row {i} ({kwargs.get('name')}): failed - {e}")

    print(f"\nDone. Inserted {inserted}, failed {failed}.")


if __name__ == "__main__":
    main()
