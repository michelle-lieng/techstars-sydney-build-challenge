import csv
import json
import ast

def str_to_bool(s):
    return str(s).strip().lower() in ['true', '1', 'yes']

def parse_list(s):
    if not s or s.strip() == "":
        return []
    return [item.strip() for item in s.split(",")]

def parse_json(s):
    if not s or s.strip() == "":
        return []
    try:
        return json.loads(s)  # parse JSON string into Python list/dict
    except json.JSONDecodeError:
        # Fallback or raise error
        return []
    
def single_to_double_quotes(obj):
    return json.dumps(obj)

def convert_csv_to_json(csv_path, json_path):
    founders = []
    def safe_int(value, default=0):
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    def parse_list_of_dicts(s):
        if not s or s.strip() == "":
            return []
        try:
            return ast.literal_eval(s)  # safely parse a Python-style string representation of a list/dict
        except Exception:
            return []


    def fix_bool_string(s):
        s = str(s).strip().upper()
        if s == "TRUE":
            return "True"
        elif s == "FALSE":
            return "False"
        else:
            return "False"
    with open(csv_path, newline='', encoding='latin1') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            founder = {}

            def add_if_value(key, value):
                if isinstance(value, list) and value:
                    founder[key] = value
                elif isinstance(value, int) and value != 0:
                    founder[key] = value
                elif isinstance(value, str) and value.strip() != "":
                    founder[key] = value.strip()
                elif isinstance(value, bool):
                    founder[key] = value
                elif value not in [None, "", [], {}]:
                    founder[key] = value

            add_if_value("name", row.get("name"))
            add_if_value("linkedin_url", row.get("linkedin_url"))
            add_if_value("city", row.get("current_city"))
            add_if_value("current_company", row.get("current_company"))
            add_if_value("current_title", row.get("current_title"))
            add_if_value("current_job_start", row.get("current_job_start"))
            add_if_value("time_in_current_role", row.get("time_in_current_role"))
            add_if_value("is_current_founder", fix_bool_string(row.get("is_current_founder", "False")))
            add_if_value("curr_startup_funding_stage", row.get("curr_startup_funding_stage"))
            add_if_value("curr_startup_url", row.get("curr_startup_url"))

            startup_info = row.get("curr_startup_info", "").strip() or row.get("bing_general_startup_info", "").strip()
            add_if_value("curr_startup_info", startup_info)

            add_if_value("curr_startup_industry", row.get("curr_startup_industry"))
            add_if_value("ai_in_curr_startup", fix_bool_string(row.get("ai_in_curr_startup", "False")))
            add_if_value("was_prev_founder", fix_bool_string(row.get("was_prev_founder", "False")))
            add_if_value("all_founded_companies", parse_list_of_dicts(row.get("all_founded_companies", "")))
            add_if_value("top_degree", row.get("top_degree"))
            add_if_value("top_degree_label", row.get("top_degree_label"))
            add_if_value("top_degree_end_date", row.get("top_degree_end_date"))
            add_if_value("was_in_accelerator", fix_bool_string(row.get("was_in_accelerator", "False")))
            add_if_value("accelerators_worked_in", parse_list(row.get("accelerators_worked_in", "")))
            add_if_value("was_in_scaleup", fix_bool_string(row.get("was_in_scaleup", "False")))
            add_if_value("scaleups_worked_in", parse_list(row.get("scaleups_worked_in", "")))
            add_if_value("was_in_bigtech", fix_bool_string(row.get("was_in_big_tech", "False")))
            add_if_value("bigtechs_worked_in", parse_list(row.get("bigtechs_worked_in", "")))
            add_if_value("gender", row.get("gender"))
            add_if_value("migrant", row.get("migrant"))
            add_if_value("is_stealth", fix_bool_string(row.get("is_stealth", "False")))
            add_if_value("linkedin_follower_count", safe_int(row.get("linkedin_follower_count", 0)))

            founders.append(founder)

    with open(json_path, 'w', encoding='utf-8') as jsonfile:
        json.dump({"founders": founders}, jsonfile, indent=4)

# Example usage
convert_csv_to_json("linkedin_processed_send_b.csv", "founders.json")