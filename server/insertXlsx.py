"""
Load founder profiles from linkedin_processed.xlsx into the database.

This maps the spreadsheet's column names onto the DB fields insertFounder
expects, coerces booleans / ints / JSON-list columns, and treats blank/"nan"
cells as NULL. Appends by default.

Usage (run from the `server/` directory):
    python insertXlsx.py ../linkedin_processed.xlsx           # append
    python insertXlsx.py ../linkedin_processed.xlsx --fresh   # drop table first

Needs pandas + openpyxl (present in the repo-root .venv, NOT in the slim
server/requirements.txt — this is a one-off local loader, not part of the API).
"""
import os
import sys
import ast
import argparse
import pandas as pd
from flask import Flask
from dotenv import load_dotenv
from mysqlSchema import FounderProfileDB

load_dotenv()

# Spreadsheet column -> insertFounder keyword. Columns not listed here and not
# already named like a DB field (e.g. the raw linkedin_* dumps) are ignored.
COLUMN_MAP = {
    "current_city": "city",
    "current_job_start_date": "current_job_start",
    "is_founder": "is_current_founder",
    "was_founder_before": "was_prev_founder",
    "founder_companies": "all_founded_companies",
    "startup_url": "curr_startup_url",
    "startup_info": "curr_startup_info",
    "startup_industry": "curr_startup_industry",
    "startup_funding_stage": "curr_startup_funding_stage",
    "ai_in_product_identity": "ai_in_curr_startup",
    "accelerator_companies_in": "accelerators_worked_in",
    "was_in_big_tech": "was_in_bigtech",
    "big_tech_companies_in": "bigtechs_worked_in",
    "scaleup_companies_in": "scaleups_worked_in",
    "is_migrant": "migrant",
    "is_stealth_mode": "is_stealth",
}

BOOL_FIELDS = {
    "is_current_founder", "ai_in_curr_startup", "was_prev_founder",
    "was_in_accelerator", "was_in_scaleup", "was_in_bigtech",
    "migrant", "is_stealth",
}
JSON_LIST_FIELDS = {
    "all_founded_companies", "accelerators_worked_in",
    "scaleups_worked_in", "bigtechs_worked_in",
}
INT_FIELDS = {"linkedin_follower_count"}

# Every keyword insertFounder accepts.
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

_EMPTY = {"", "nan", "none", "null", "n/a"}


def is_blank(value):
    return value is None or (isinstance(value, str) and value.strip().lower() in _EMPTY)


def parse_bool(value):
    return str(value).strip().lower() in ("true", "1", "yes", "y")


def coerce(field, value):
    if is_blank(value):
        return None
    if field in BOOL_FIELDS:
        return parse_bool(value)
    if field in INT_FIELDS:
        try:
            return int(float(value))
        except (ValueError, TypeError):
            return 0
    if field in JSON_LIST_FIELDS:
        # These cells hold Python-repr lists/dicts (single quotes) or plain text.
        # ast.literal_eval handles the repr; anything else becomes a 1-item list.
        # insertFounder json.dumps() the result before storing.
        if isinstance(value, str):
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return [value.strip()]
        return value
    return str(value).strip() if isinstance(value, str) else value


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("xlsx_path", help="Path to the .xlsx file")
    ap.add_argument("--fresh", action="store_true",
                    help="Drop and recreate the table before loading (DESTRUCTIVE)")
    args = ap.parse_args()

    if not os.path.exists(args.xlsx_path):
        sys.exit(f"File not found: {args.xlsx_path}")

    df = pd.read_excel(args.xlsx_path)
    df = df.rename(columns=COLUMN_MAP)
    # Convert pandas NaN -> None so is_blank/coerce see real nulls.
    df = df.astype(object).where(pd.notna(df), None)

    ignored = sorted(c for c in df.columns if c not in VALID_FIELDS)
    if ignored:
        print(f"Ignoring {len(ignored)} unmapped columns: {ignored}\n")
    if "name" not in df.columns:
        sys.exit("Spreadsheet has no 'name' column after mapping.")

    app = Flask(__name__)
    db = FounderProfileDB(app=app, password=os.getenv("DB_PASSWORD"))

    if args.fresh:
        print("--fresh: dropping and recreating founder_profile table\n")
        db.dropFounderTable()
        db.createFounderProfileTable()

    inserted, failed = 0, 0
    for idx, row in df.iterrows():
        kwargs = {f: coerce(f, row[f]) for f in VALID_FIELDS if f in df.columns}
        if is_blank(kwargs.get("name")):
            print(f"Row {idx + 2}: skipped (no name)")
            continue
        try:
            db.insertFounder(**kwargs)
            inserted += 1
        except Exception as e:
            failed += 1
            print(f"Row {idx + 2} ({kwargs.get('name')}): failed - {e}")

    print(f"\nDone. Inserted {inserted}, failed {failed}, out of {len(df)} rows.")


if __name__ == "__main__":
    main()
