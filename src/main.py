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
        cols = list(set(["name"] + columns_to_merge))
        df = df.merge(df_processed[cols], on="name", how="left")
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
        return row[col_name]
    if condition is not None and not condition(row):
        return None
    func_args = func_args or []
    # this line lets use mix row values as constants as arguments 
    resolved_args = [
        row[arg.name] if isinstance(arg, Col) 
        else arg for arg in func_args
    ]
    return func(*resolved_args)

def cols_to_skip_if_filled(df, cols_to_skip):
    # Merge all previous results at once
    df = merge_previous_results(
        df,
        columns_to_merge=[item["col"] for item in cols_to_skip]
    )
    # Apply updates only if needed
    for item in cols_to_skip:
        df[item["col"]] = df.apply(
            lambda row: run_or_skip(
                row,
                item["col"], 
                item["func"], 
                item.get("args", []),
                item.get("condition", None)
            ),
            axis=1
        )
    return df

cols_to_skip_1 = [
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
]
# Usage in your pipeline:
df = cols_to_skip_if_filled(df, cols_to_skip_1)

# Now do everything else for getting linkedin_edu and linked_job cleaned:
df["linkedin_json_cleaned"] = df["linkedin_json_raw"].apply(clean_json_response)
df["linkedin_jobs"] = df["linkedin_json_cleaned"].apply(parse_linkedin_jobs)

df["linkedin_education_cleaned"] = df["linkedin_education_raw"].apply(clean_json_response)
df["linkedin_education"] = df["linkedin_education_cleaned"].apply(parse_linkedin_education)

# Summarise all companies and titles they've had (not in final df)
df["all_companies"] = df["linkedin_jobs"].apply(get_all_companies)
df["all_job_titles"] = df["linkedin_jobs"].apply(get_all_job_titles)

# Now functions to explore their current working situation!!!
df["current_company"] = df["linkedin_jobs"].apply(get_current_company)
df["current_title"] = df["linkedin_jobs"].apply(get_current_title)
df["current_job_start_date"] = df["linkedin_jobs"].apply(get_current_start_date)
df["time_in_current_role"] = df.apply(
    lambda row: calculate_duration(row["current_job_start_date"], "Present")
    if row["current_job_start_date"] != None else None,
    axis = 1
)

# Get all founder information for current startup!!!
df["is_founder"] = df["current_title"].apply(is_founder_role)
df["founder_persona"] = df["all_job_titles"].apply(classify_founder_persona)

# get information about education 
df["top_education_summary"] = df["linkedin_education"].apply(extract_top_education_info) # will remove later
df["top_degree"] = df["top_education_summary"].apply(lambda x: x.get("top_degree") if x else None)
df["top_degree_label"] = df["top_education_summary"].apply(lambda x: x.get("top_degree_label") if x else None)
df["top_institution"] = df["top_education_summary"].apply(lambda x: x.get("top_institution") if x else None)
df["top_degree_end_date"] = df["top_education_summary"].apply(lambda x: x.get("top_degree_end_date") if x else None)

# more info about the individual
df[["was_in_accelerator", "accelerator_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, ACCELERATORS))
)
df[["was_in_scaleup", "scaleup_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, SCALE_UPS))
)
df[["was_in_big_tech", "big_tech_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, BIG_TECH))
)
df[["all_locations_worked", "is_migrant"]] = df["linkedin_jobs"].apply(
    lambda jobs: pd.Series(get_all_locations_worked(jobs))
)
df["current_city"] = df["all_locations_worked"].apply(current_city)

# get startup info!!!!!!:
df["is_stealth_mode"]=df["current_company"].apply(check_is_stealth_mode)
# df["startup_url"] = df.apply(
#     lambda row: bing_find_linkedin_company_url(
#         row["current_company"],
#         row["name"]
#     ) if row["is_founder"] is True 
#     and row["is_stealth_mode"] is False else None,
#     axis=1
# )
df["startup_url"] = df.apply(
    lambda row: bing_find_linkedin_company_url(
            row["current_company"],
            row["name"]
        ) 
    if row["is_founder"] is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
)

df["linkedin_follower_count"] = df.apply(
    lambda row: get_linkedin_company_followers_from_url(
        row["startup_url"]
    ) 
    if row["is_founder"] is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
)
df["current_startup_info"] = df["linkedin_jobs"].apply(get_current_startup_info) # will remove later
# Search for funding info only if person is a founder at their current company
df["bing_general_startup_info"] = df.apply(
    lambda row: bing_general_startup_info(
        startup_name=row["current_company"],
        founder_name=row["name"],
        current_job_start_date=row["current_job_start_date"]
    ) if row["is_founder"] is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
) # WILL REMOVE LATER THIS IS JUST BING!!!
df["startup_info"] = df.apply(
    lambda row: summarise_startup_info(
        row.get("bing_general_startup_info"), 
        row.get("current_startup_info")
        )
    if row.get("is_founder") 
    and row["is_stealth_mode"] is False else None,
    axis=1
)
# Apply to DataFrame
df["startup_industry"] = df.apply(
    lambda row: find_startup_industry(row.get("startup_info"))
    if row.get("is_founder") 
    and row["is_stealth_mode"] is False else None,
    axis=1
)
df["ai_in_product_identity"] = df.apply(
    lambda row: uses_ai(
        row["bing_general_startup_info"]
    ) if row["is_founder"] is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
)
# get funding info: search for funding info only if person is a founder at their current company
df["bing_funding_info"] = df.apply(
    lambda row: bing_funding_info(
        startup_name=row["current_company"],
        founder_name=row["name"],
        current_job_start_date=row["current_job_start_date"]
    ) if row["is_founder"] is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
)
df["startup_funding_stage"] = df.apply(
    lambda row: (
        "Bootstrapped" if row.get("bing_funding_info") is None
        else infer_startup_funding_stage(row["bing_funding_info"])
    ) if row.get("is_founder") is True 
    and row["is_stealth_mode"] is False else None,
    axis=1
)

############## ABOUT PREVIOUS STARTUP JOURNEY - # will remove later
# df["founder_count"] = df["all_job_titles"].apply(count_founder_roles)
# df["was_founder_before"] = df.apply(
#     lambda row: was_founder_before_from_count(
#         row["is_founder"],
#         row["founder_count"]),
#     axis=1)

# get info for all previous startups too!!!
df["founder_companies"] = df.apply(
    lambda x: get_founder_companies(
        x["linkedin_jobs"],
        x["name"],
        x["is_founder"],
        x["current_job_start_date"]),
    axis =1)
#df["founder_companies"][2]

df["was_founder_before"] = df.apply(
    lambda row: row["founder_companies"] is not None,
    axis=1)

df.to_excel("data/linkedin_processed.xlsx", index=False)
cols_to_drop = ["linkedin_job_dump",
                "linkedin_education_dump",
                "linkedin_json_raw",
                "linkedin_json_cleaned",
                "linkedin_education_raw",
                "linkedin_education_cleaned",
                "current_startup_info",
                "all_locations_worked",
                "top_education_summary",
                "bing_funding_info",
                "bing_general_startup_info"
                ]
html = df.drop(cols_to_drop, axis=1).to_html()
with open("table_view.html", "w", encoding="utf-8") as f:
    f.write(df.to_html())


    ### ADD TAG "SERIAL FOUNDER"

    # build space (in education)

    
# EXTRA TAGS:
# - founder_signal_strength 