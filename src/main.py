import pandas as pd
import os
from dotenv import load_dotenv

from src.utilities.prompts import linkedin_job_json_prompt, linkedin_education_prompt, linkedin_scraper_sys_prompt, startup_summary_prompt, startup_industry_prompt
from src.functions.data_cleaning_edu_and_job import clean_json_response, parse_linkedin_education, parse_linkedin_jobs
from src.utilities.gemini_function import gemini_call_with_pt
from src.utilities.classifiers import ACCELERATORS, SCALE_UPS, BIG_TECH

from src.functions.founder_info import is_founder_role, get_current_startup_info, classify_founder_persona, count_founder_roles, was_founder_before_from_count, get_founder_companies, calculate_duration
from src.functions.all_working_info import get_current_company, get_current_title, get_current_start_date, get_all_companies, get_all_job_titles
from src.functions.startup_info import bing_funding_info, infer_startup_funding_stage, bing_find_linkedin_company_url, bing_general_startup_info, summarise_startup_info, find_startup_industry, uses_ai, check_is_stealth_mode, get_linkedin_company_followers_from_url
from src.functions.information_about_person import extract_top_education_info, classifier_matches, current_city, get_all_locations_worked

# Load environment variables
load_dotenv()

# Load data from Excel
df = pd.read_excel("data/input.xlsx")

# This is to help understand which func_arg is a Col and which is a constant
class Col:
    def __init__(self, name):
        self.name = name

# LET'S DO ALL THE CHANGES IN WHICH WE SKIP IF ALREADY DONE!
def merge_previous_results(df, columns_to_merge):
    """
    This checks if a previously processed file exists. 
    
    If it does then it loads it and merges the given columns from the 
    processed_df to your current df so you don't have to redo.

    If it doesn't exist it initialises the columns you want to merge 
    as empty (None).

    Returns the updated df loaded with previous values for those columns
    given.
    """
    if os.path.exists("data/linkedin_processed.xlsx"):
        df_processed = pd.read_excel("data/linkedin_processed.xlsx")
        # Only keep columns that exist in df_processed
        cols = ["name"] + [col for col in columns_to_merge if col in df_processed.columns]
        df = df.merge(df_processed[cols], on="name", how="left")
        # For any columns not present, initialize as None
        for col in columns_to_merge:
            if col not in df.columns:
                df[col] = None
    else:
        for col in columns_to_merge:
            df[col] = None
    return df

def run_or_skip(row, col_name, func, func_args=None, condition=None):
    """
    For given row only run the function if the target column is empty.

    If column already has value (not na) then return existing value.

    If it is then call the function with arguments pulled from the 
    necessary rows. 
    """
    if pd.notna(row.get(col_name)):
        return row[col_name], True  # Skipped
    if condition is not None and not condition(row):
        return None, False
    func_args = func_args or []
    resolved_args = [
        row[arg.name] if isinstance(arg, Col) 
        else arg for arg in func_args
    ]
    return func(*resolved_args), False  # Not skipped

def cols_to_skip_if_filled(df, cols_to_skip):
    skip_report = {item["col"]: [] for item in cols_to_skip}
    df = merge_previous_results(
        df,
        columns_to_merge=[item["col"] for item in cols_to_skip]
    )
    for item in cols_to_skip:
        def apply_and_track(row):
            value, skipped = run_or_skip(
                row,
                item["col"], 
                item["func"], 
                item.get("args", []),
                item.get("condition", None)
            )
            if skipped:
                skip_report[item["col"]].append(row.get("name", row.name))
            return value
        df[item["col"]] = df.apply(apply_and_track, axis=1)
    # Print or return skip_report as needed
    print("Skip report:")
    for col, skipped_names in skip_report.items():
        print(f"{col}: {skipped_names}")
    return df

cols_to_skip_all = [
    # LinkedIn JSON columns
    {
        "col": "linkedin_json_raw",
        "func": gemini_call_with_pt,
        "args": [Col("linkedin_job_dump"), linkedin_job_json_prompt, linkedin_scraper_sys_prompt],
    },
    {
        "col": "linkedin_education_raw",
        "func": gemini_call_with_pt,
        "args": [Col("linkedin_education_dump"), linkedin_education_prompt, linkedin_scraper_sys_prompt],
    },
    # Cleaned and parsed columns
    {
        "col": "linkedin_json_cleaned",
        "func": clean_json_response,
        "args": [Col("linkedin_json_raw")],
    },
    {
        "col": "linkedin_jobs",
        "func": parse_linkedin_jobs,
        "args": [Col("linkedin_json_cleaned")],
    },
    {
        "col": "linkedin_education_cleaned",
        "func": clean_json_response,
        "args": [Col("linkedin_education_raw")],
    },
    {
        "col": "linkedin_education",
        "func": parse_linkedin_education,
        "args": [Col("linkedin_education_cleaned")],
    },
    # All companies and job titles
    {
        "col": "all_companies",
        "func": get_all_companies,
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "all_job_titles",
        "func": get_all_job_titles,
        "args": [Col("linkedin_jobs")],
    },
    # Current working info
    {
        "col": "current_company",
        "func": get_current_company,
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "current_title",
        "func": get_current_title,
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "current_job_start_date",
        "func": get_current_start_date,
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "time_in_current_role",
        "func": calculate_duration,
        "args": [Col("current_job_start_date"), "Present"],
        "condition": lambda row: row.get("current_job_start_date") is not None,
    },
    # Founder info
    {
        "col": "is_founder",
        "func": is_founder_role,
        "args": [Col("current_title")],
    },
    {
        "col": "founder_persona",
        "func": classify_founder_persona,
        "args": [Col("all_job_titles")],
    },
    # Education info
    {
        "col": "top_education_summary",
        "func": extract_top_education_info,
        "args": [Col("linkedin_education")],
    },
    {
        "col": "top_degree",
        "func": lambda summary: summary.get("top_degree") if summary else None,
        "args": [Col("top_education_summary")],
    },
    {
        "col": "top_degree_label",
        "func": lambda summary: summary.get("top_degree_label") if summary else None,
        "args": [Col("top_education_summary")],
    },
    {
        "col": "top_institution",
        "func": lambda summary: summary.get("top_institution") if summary else None,
        "args": [Col("top_education_summary")],
    },
    {
        "col": "top_degree_end_date",
        "func": lambda summary: summary.get("top_degree_end_date") if summary else None,
        "args": [Col("top_education_summary")],
    },
    #Classifier matches
    {
        "col": "was_in_accelerator",
        "func": lambda all_companies: classifier_matches(all_companies, ACCELERATORS)[0],
        "args": [Col("all_companies")],
    },
    {
        "col": "accelerator_companies_in",
        "func": lambda all_companies: classifier_matches(all_companies, ACCELERATORS)[1],
        "args": [Col("all_companies")],
    },
    {
        "col": "was_in_scaleup",
        "func": lambda all_companies: classifier_matches(all_companies, SCALE_UPS)[0],
        "args": [Col("all_companies")],
    },
    {
        "col": "scaleup_companies_in",
        "func": lambda all_companies: classifier_matches(all_companies, SCALE_UPS)[1],
        "args": [Col("all_companies")],
    },
    {
        "col": "was_in_big_tech",
        "func": lambda all_companies: classifier_matches(all_companies, BIG_TECH)[0],
        "args": [Col("all_companies")],
    },
    {
        "col": "big_tech_companies_in",
        "func": lambda all_companies: classifier_matches(all_companies, BIG_TECH)[1],
        "args": [Col("all_companies")],
    },
    # Locations worked and migration
    {
        "col": "all_locations_worked",
        "func": lambda jobs: get_all_locations_worked(jobs)[0],
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "is_migrant",
        "func": lambda jobs: get_all_locations_worked(jobs)[1],
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "current_city",
        "func": current_city,
        "args": [Col("all_locations_worked")],
    },
    # Startup info (conditional on founder and not stealth)
    {
        "col": "is_stealth_mode",
        "func": check_is_stealth_mode,
        "args": [Col("current_company")],
    },
    {
        "col": "startup_url",
        "func": bing_find_linkedin_company_url,
        "args": [Col("current_company"), Col("name")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    {
        "col": "linkedin_follower_count",
        "func": get_linkedin_company_followers_from_url,
        "args": [Col("startup_url")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    {
        "col": "bing_general_startup_info",
        "func": bing_general_startup_info,
        "args": [Col("current_company"), Col("name"), Col("current_job_start_date")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    {
        "col": "current_startup_info",
        "func": get_current_startup_info,
        "args": [Col("linkedin_jobs")],
    },
    {
        "col": "startup_info",
        "func": summarise_startup_info,
        "args": [Col("bing_general_startup_info"), Col("current_startup_info")],
        "condition": lambda row: row.get("is_founder") and row.get("is_stealth_mode") is False,
    },
    {
        "col": "startup_industry",
        "func": find_startup_industry,
        "args": [Col("startup_info")],
        "condition": lambda row: row.get("is_founder") and row.get("is_stealth_mode") is False,
    },
    {
        "col": "ai_in_product_identity",
        "func": uses_ai,
        "args": [Col("bing_general_startup_info")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    {
        "col": "bing_funding_info",
        "func": bing_funding_info,
        "args": [Col("current_company"), Col("name"), Col("current_job_start_date")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    {
        "col": "startup_funding_stage",
        "func": lambda funding: "Bootstrapped" if funding is None else infer_startup_funding_stage(funding),
        "args": [Col("bing_funding_info")],
        "condition": lambda row: row.get("is_founder") is True and row.get("is_stealth_mode") is False,
    },
    # Previous founder journey
    {
        "col": "founder_companies",
        "func": get_founder_companies,
        "args": [Col("linkedin_jobs"), Col("name"), Col("is_founder"), Col("current_job_start_date")],
    },
    {
        "col": "was_founder_before",
        "func": lambda founder_companies: founder_companies is not None,
        "args": [Col("founder_companies")],
    },
]

# Usage in your pipeline:
# Load processed names if file exists
if os.path.exists("data/linkedin_processed.xlsx"):
    df_processed = pd.read_excel("data/linkedin_processed.xlsx")
    processed_names = set(df_processed["name"].astype(str))
    # Only keep rows in df that are not already processed
    df_new = df[~df["name"].astype(str).isin(processed_names)].copy()
else:
    df_processed = None
    df_new = df.copy()

# Only process new names
if not df_new.empty:
    df_new = cols_to_skip_if_filled(df_new, cols_to_skip_all)
    # Append new results to the old processed file (if exists)
    if df_processed is not None:
        df_final = pd.concat([df_processed, df_new], ignore_index=True)
    else:
        df_final = df_new
else:
    # No new names to process
    if df_processed is not None:
        df_final = df_processed
    else:
        df_final = df

# Save and export as before
df_final.to_excel("data/linkedin_processed.xlsx", index=False)
with open("table_view.html", "w", encoding="utf-8") as f:
    f.write(df_final.to_html())

    ### ADD TAG "SERIAL FOUNDER"

    # build space (in education)

    
# EXTRA TAGS:
# - founder_signal_strength 