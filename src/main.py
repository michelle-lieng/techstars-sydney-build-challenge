import pandas as pd
import os
from dotenv import load_dotenv
from openai import OpenAI
from src.models import LinkedInJob, LinkedInEducation
from src.prompts import linkedin_job_json_prompt, linkedin_education_prompt, linkedin_scraper_sys_prompt, startup_summary_prompt, startup_industry_prompt
from src.utilities.bing_function import bing_search
from src.utilities.data_cleaning import clean_json_response, parse_linkedin_education, parse_linkedin_jobs
from src.utilities.gemini_function import gemini_call_with_pt
from datetime import datetime
import re
from typing import List, Union, Dict, Optional, Tuple
from src.classifiers import ACCELERATORS, SCALE_UPS, BIG_TECH

# Load environment variables
load_dotenv()

# Load data from Excel
df = pd.read_excel("data/input.xlsx")

# Check for existing outputs
if os.path.exists("data/linkedin_processed.xlsx"):
    df_processed = pd.read_excel("data/linkedin_processed.xlsx")
    df = df.merge(df_processed[["linkedin_job_dump", "linkedin_json_raw"]], on="linkedin_job_dump", how="left")
else:
    df["linkedin_json_raw"] = None

def run_or_skip_gemini(row):
    if pd.notna(row.get("linkedin_json_raw")):
        return row["linkedin_json_raw"]
    return gemini_call_with_pt(row["linkedin_job_dump"], linkedin_job_json_prompt,linkedin_scraper_sys_prompt)

df["linkedin_json_raw"] = df.apply(run_or_skip_gemini, axis=1)

# Apply Gemini and parse
df["linkedin_json_cleaned"] = df["linkedin_json_raw"].apply(clean_json_response)
df["linkedin_jobs"] = df["linkedin_json_cleaned"].apply(parse_linkedin_jobs)
# df["linkedin_jobs_json"] = df["linkedin_jobs"].apply(
#     lambda jobs: json.dumps([job.dict() for job in jobs]) if jobs else None
# )

# Check for existing education outputs
if os.path.exists("data/linkedin_processed.xlsx"):
    df_processed = pd.read_excel("data/linkedin_processed.xlsx")
    df = df.merge(df_processed[["linkedin_education_dump", "linkedin_education_raw"]], 
                 on="linkedin_education_dump", how="left")
else:
    df["linkedin_education_raw"] = None

def run_or_skip_gemini_education(row):
    if pd.notna(row.get("linkedin_education_raw")):
        return row["linkedin_education_raw"]
    return gemini_call_with_pt(row["linkedin_education_dump"], linkedin_education_prompt, linkedin_scraper_sys_prompt)

df["linkedin_education_raw"] = df.apply(run_or_skip_gemini_education, axis=1)

df["linkedin_education_cleaned"] = df["linkedin_education_raw"].apply(clean_json_response)
df["linkedin_education"] = df["linkedin_education_cleaned"].apply(parse_linkedin_education)

def get_current_company(jobs: List[dict]) -> str:
    if not jobs:
        return "Unemployed"
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.company
    
    return "Unemployed"

df["current_company"] = df["linkedin_jobs"].apply(get_current_company)

def get_current_title(jobs: List[dict]) -> str: 
    if not jobs:
        return "Unemployed"
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.title
    
    return "Unemployed"

df["current_title"] = df["linkedin_jobs"].apply(get_current_title)

def get_current_start_date(jobs: List[dict]) -> str:
    if not jobs:
        return None

    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.start_date

    return None

df["current_job_start_date"] = df["linkedin_jobs"].apply(get_current_start_date)

def is_founder_role(title: str) -> bool:
    if not isinstance(title, str):
        return False

    keywords = [
        "founder", "co-founder", "cofounder", "founding engineer",
        "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
        "Chief Executive Officer"
    ]

    title_lower = title.lower()
    return any(keyword in title_lower for keyword in keywords)

df["is_founder"] = df["current_title"].apply(is_founder_role)


def get_current_startup_info(jobs: List[dict]) -> str: 
    if not jobs:
        return None
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.additional_notes or None
    
    return None

df["current_startup_info"] = df["linkedin_jobs"].apply(get_current_startup_info)

def get_all_previous_titles(jobs: List[dict]) -> Optional[str]:
    if not jobs:
        return None

    previous_titles = []

    for job in jobs:
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() != "present":
            previous_titles.append(job.title)

    return ", ".join(previous_titles) if previous_titles else None
df["previous_titles"] = df["linkedin_jobs"].apply(get_all_previous_titles)


def was_founder_before_from_titles(titles: str) -> bool:
    if not isinstance(titles, str):
        return False

    founder_keywords = [
        "founder", "co-founder", "cofounder", "founding engineer",
        "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
        "chief executive officer", "partner", "cfo", "chief financial officer"
    ]

    titles_lower = titles.lower()
    return any(keyword in titles_lower for keyword in founder_keywords)

df["was_founder_before"] = df["previous_titles"].apply(was_founder_before_from_titles)


def get_all_companies(jobs: List[dict]) -> Optional[str]:
    if not jobs:
        return None

    all_companies = []
    seen = set() #deals with duplicates

    for job in jobs:
        if isinstance(job, LinkedInJob):
            company = job.company
            if company not in seen:
                all_companies.append(job.company)
                seen.add(company)

    return ", ".join(all_companies) if all_companies else None

df["all_companies"] = df["linkedin_jobs"].apply(get_all_companies)





def extract_top_education_info(entries: List[dict]) -> Optional[dict]:
    if not entries:
        return None

    degree_rank = {
        # PhD level
        "phd": 3, "doctor of philosophy": 3, "dphil": 3, "ph.d.":3,

        # Master's level
        "master": 2, "msc": 2, "m.sc": 2, "meng": 2, "m.eng": 2, "mba": 2,
        "mtech": 2, "m.tech": 2, "mres": 2, "med": 2, "m.ed": 2, "graduate diploma": 2,

        # Bachelor's level
        "bachelor": 1, "b.sc": 1, "bsc": 1, "beng": 1, "b.eng": 1, "ba": 1,
        "b.a": 1, "undergraduate": 1,

        # Non-traditional / bootcamps
        "diploma": 0, "cert iv": 0, "certificate": 0, "certification": 0,
        "short course": 0, "bootcamp": 0, "nanodegree": 0, "microcredential": 0,
        "udemy": 0, "coursera": 0, "edx": 0, "general assembly": 0
    }

    degree_label = {
        3: "PhD",
        2: "Master’s",
        1: "Bachelor’s",
        0: "Non-traditional",
        -1: "Unknown"
    }

    def categorize(degree: Optional[str]) -> int:
        if not degree:
            return -1
        deg = degree.lower()
        for keyword, rank in degree_rank.items():
            if keyword in deg:
                return rank
        return -1

    top_score = -1
    top_entry = None
    for entry in entries:
        score = categorize(entry.degree)
        if score > top_score:
            top_score = score
            top_entry = entry

    if not top_entry:
        return None

    return {
        "top_degree": top_entry.degree or "",
        "top_degree_label": degree_label.get(top_score, "Unknown"),
        "top_institution": top_entry.institution,
        "top_degree_end_date": top_entry.end_date
    }

df["top_education_summary"] = df["linkedin_education"].apply(extract_top_education_info)

df["top_degree"] = df["top_education_summary"].apply(lambda x: x.get("top_degree") if x else None)
df["top_degree_label"] = df["top_education_summary"].apply(lambda x: x.get("top_degree_label") if x else None)
df["top_institution"] = df["top_education_summary"].apply(lambda x: x.get("top_institution") if x else None)
df["top_degree_end_date"] = df["top_education_summary"].apply(lambda x: x.get("top_degree_end_date") if x else None)


def is_before_startup_founded(result_date: str, startup_start_str: str) -> bool:
    try:
        # Parse startup founding date
        startup_start = datetime.strptime(startup_start_str, "%b %Y")  # e.g., Feb 2024

        # Parse result date
        result_dt = datetime.strptime(result_date, "%Y-%m-%d")  # e.g., 2023-11-28

        return result_dt < startup_start
    except:
        # If date is "Unknown" or malformed, don’t auto-discard
        return False

def contains_exact_startup_name(text: str, startup_name: str) -> bool:
    # Normalize both to lowercase
    text = text.lower()
    name = re.escape(startup_name.lower())

    # Match name surrounded by word boundaries
    return bool(re.search(rf"\b{name}\b", text))


def is_valid_crunchbase_org_url(url: str, startup_name: str) -> bool:
    """
    CHANGE IN MVP 2 TO ALLOW MORE LINKS NOT CRUNCHBASE THROUGH LIKE lorikeet is
    actually series A but on crunchbase it's seed!!!
    """


    # if not url.startswith("https://www.crunchbase.com/organization/"):
    #     return True  # Allow non-Crunchbase org URLs through


    pattern = r'/organization/([^/]+)'
    match = re.search(pattern, url)
    if not match:
        return False

    slug = match.group(1).lower()
    startup = startup_name.lower().strip().replace(" ", "-")

    # Exact match
    if slug == startup:
        return True

    # Allow suffixes like -f57f but reject -crunchy or -products
    if slug.startswith(startup + "-"):
        suffix = slug[len(startup) + 1:]
        return not suffix.isalpha()  # Reject if it's all letters (e.g. crunchy)

    return False

url = "https://www.crunchbase.com/organization/bean-f57f"
url = "https//www.google.com"
#url = "https://www.crunchbase.com/organization/bean-crunchy/company_financials"
startup_name = "bean"
is_valid_crunchbase_org_url(url, startup_name)

def extract_mentioned_years(text: str) -> List[int]:
    matches = re.findall(r"\b(19[8-9]\d|20[0-3]\d)\b", text)  # Year between 1980–2039
    return [int(m) for m in matches]

text = 'Their latest funding was raised on Sep 11, 2013 from a Series C round. NextDocs is funded by 3 investors. OpenView and Bridgebank Capital are the most recent investors.'
extract_mentioned_years(text)
def mentions_outdated_funding(text: str, startup_start_str: str) -> bool:
    try:
        startup_start = datetime.strptime(startup_start_str, "%b %Y")  # e.g. Jun 2024
        mentioned_years = extract_mentioned_years(text)
        return any(year < startup_start.year for year in mentioned_years)
    except:
        return False
dat="Jun 2024"
mentions_outdated_funding(text, dat)

def bing_funding_info(startup_name: str, founder_name: str, current_job_start_date: str) -> str:
    results = bing_search(f"site: crunchbase.com {startup_name} {founder_name} funding round", count=3)
    # Filter for relevant results 
    # Problem: saw if there was no funding start returning articles on general how to fund in a startup etc
    # Filter for those with startup name in snippet or name
        # Filter for relevant results
    relevant_results = []
    for result in results:
        date = result.get("date", "")
        snippet = result.get("snippet", "").lower()
        title = result.get("name", "").lower()
        url = result.get("url", "").lower()

        full_text = f"{snippet} {title} {url}"

        # Check if both startup name is mentioned
        if contains_exact_startup_name(full_text, startup_name):
            if not is_before_startup_founded(date, current_job_start_date):
                if not mentions_outdated_funding(snippet, current_job_start_date):
                    if is_valid_crunchbase_org_url(url, startup_name):
                        relevant_results.append({
                            'url': result.get('url'),
                            'snippet': result.get('snippet'),
                            'date': result.get('date')
                        })
    
    return relevant_results if relevant_results else None

# Search for funding info only if person is a founder at their current company
df["bing_funding_info"] = df.apply(
    lambda row: bing_funding_info(
        startup_name=row["current_company"],
        founder_name=row["name"],
        current_job_start_date=row["current_job_start_date"]
    ) if row["is_founder"] is True else None,
    axis=1
)

# Rank mapping of funding stages
round_rank = {
    "idea": 0,
    "bootstrapped": 0,
    "pre seed": 1,
    "seed": 2,
    "series a": 3,
    "series b": 4,
    "growth": 5,
    "public": 6,
    "exited": 7
}

def normalize_round_label(text: str) -> Optional[str]:
    text = text.lower()
    clean_text = text.replace("-", " ")  # handle "series-a" and similar
    for label in round_rank:
        if label in clean_text:
            return label.title()
    return None

def infer_startup_funding_stage(bing_results: List[Dict]) -> str:
    if not bing_results:
        return "Unknown"

    valid_mentions = []

    for result in bing_results:
        snippet = result.get("snippet", "").lower()

        round_label = normalize_round_label(snippet)
        if round_label:
            valid_mentions.append(round_label)

    if not valid_mentions:
        return "Bootstrapped"  # If there are results but no rounds mentioned

    # Pick the highest-ranked round
    best_round = max(valid_mentions, key=lambda r: round_rank.get(r.lower(), -1))
    return best_round

#df["startup_funding_stage"] = df["bing_funding_info"].apply(infer_startup_funding_stage)
df["startup_funding_stage"] = df.apply(
    lambda row: (
        "Bootstrapped" if row.get("bing_funding_info") is None
        else infer_startup_funding_stage(row["bing_funding_info"])
    ) if row.get("is_founder") is True else None,
    axis=1
)

def bing_find_linkedin_company_url(startup_name: str, founder_name: str) -> str:
    results = bing_search(f"site:linkedin.com {startup_name} {founder_name}", count=1)
    for result in results:
        url = result.get("url", "").lower()
        if "linkedin.com/company" in url:
            return url  # <-- As soon as this runs, the function exits!
    return None

df["startup_url"] = df.apply(
    lambda row: bing_find_linkedin_company_url(
        row["current_company"],
        row["name"]
    ) if row["is_founder"] is True else None,
    axis=1
)

def bing_general_startup_info(startup_name: str, founder_name: str, current_job_start_date: str) -> str:
    results = bing_search(f"What is the startup {startup_name} {founder_name} about", count=4)
    # Filter for relevant results 
    # Problem: saw if there was no funding start returning articles on general how to fund in a startup etc
    # Filter for those with startup name in snippet or name
        # Filter for relevant results
    relevant_results = []
    for result in results:
        date = result.get("date", "")
        snippet = result.get("snippet", "").lower()
        title = result.get("name", "").lower()
        url = result.get("url", "").lower()

        full_text = f"{snippet} {title} {url}"

        # Check if both startup name is mentioned
        if contains_exact_startup_name(full_text, startup_name):
            if not is_before_startup_founded(date, current_job_start_date):
                if not mentions_outdated_funding(snippet, current_job_start_date):
                    relevant_results.append({
                        'url': result.get('url'),
                        'snippet': result.get('snippet'),
                        'date': result.get('date')
                    })
    
    return relevant_results if relevant_results else None


# Search for funding info only if person is a founder at their current company
df["bing_general_startup_info"] = df.apply(
    lambda row: bing_general_startup_info(
        startup_name=row["current_company"],
        founder_name=row["name"],
        current_job_start_date=row["current_job_start_date"]
    ) if row["is_founder"] is True else None,
    axis=1
)


def summarise_startup_info(bing_general_startup_info: str, current_startup_info) -> str:
    # Flatten list of snippets
    snippets = "\n".join(item.get("snippet", "") for item in bing_general_startup_info or [])

    # Combine with current startup info (if any)
    combined_info = (current_startup_info or "") + "\n" + snippets 

    summary = gemini_call_with_pt(
        input_info=combined_info,
        prompt_template=startup_summary_prompt,
        system_prompt="You are a professional startup analyst."
    )
    return summary

# Apply to DataFrame
df["startup_info"] = df.apply(
    lambda row: summarise_startup_info(
        row.get("bing_general_startup_info"), 
        row.get("current_startup_info")
        )
    if row.get("is_founder") else None,
    axis=1
)

def find_startup_industry(startup_info: str) -> str:
    summary = gemini_call_with_pt(
        input_info=startup_info,
        prompt_template=startup_industry_prompt,
        system_prompt="You are a professional startup analyst."
    )
    return summary

# Apply to DataFrame
df["startup_industry"] = df.apply(
    lambda row: find_startup_industry(row.get("startup_info"))
    if row.get("is_founder") else None,
    axis=1
)

def uses_ai(bing_general_startup_info: str) -> bool:
    if not bing_general_startup_info:
        return None
    text = " ".join(item.get("snippet", "") for item in bing_general_startup_info if isinstance(item, dict))
    text = text.lower()
    return bool(re.search(r"\bai\b", text)) or "artificial intelligence" in text

df["ai_in_product_identity"] = df["bing_general_startup_info"].apply(uses_ai)

def classifier_matches(all_companies: str, classifier: set) -> Tuple[bool, Optional[str]]:
    companies = [c.strip() for c in all_companies.split(",")]
    matches = [company for company in companies if company in classifier]
    if matches:
        return (True, ",".join(matches))
    else: 
        return (False, None)

# # Example usage for a single row:
# x = df["all_companies"][2]
# was_in, which_accels = accelerator_matches(x)
# print(was_in)
# print(which_accels)

# To add to your DataFrame:
df[["was_in_accelerator", "accelerator_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, ACCELERATORS))
)

df[["was_in_scaleup", "scaleup_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, SCALE_UPS))
)

df[["was_in_big_tech", "big_tech_companies_in"]] = df["all_companies"].apply(
    lambda all_companies: pd.Series(classifier_matches(all_companies, BIG_TECH))
)

def get_all_locations_worked(jobs: List[dict]) -> Tuple[Optional[str], bool]:
    if not jobs:
        return None, False

    all_locations = []
    seen = set()
    for job in jobs:
        if isinstance(job, LinkedInJob):
            location = job.location
            if location and location not in seen:
                all_locations.append(location)
                seen.add(location)
    if not all_locations:
        return None, False
    
    # List of substrings to check for
    aus_terms = [
    # Country
    "australia", "australian",

    # States
    "new south wales",
    "victoria",
    "queensland",
    "western australia",
    "south australia",
    "tasmania",
    "australian capital territory",
    "northern territory",

    # Major cities and metro areas
    "sydney", "greater sydney area",
    "melbourne", "greater melbourne area",
    "brisbane", "greater brisbane area",
    "perth", "greater perth area",
    "adelaide", "greater adelaide area",
    "hobart", "greater hobart area",
    "canberra", "greater canberra area",
    "darwin", "greater darwin area",
    "gold coast", "sunshine coast", "newcastle", "wollongong", "geelong",

    # Regions
    "regional nsw", "regional victoria", "regional queensland", "regional wa",
    "regional sa", "regional tasmania", "regional act", "regional nt"
    ]
    print(all_locations[-1])
    last_location = all_locations[-1].lower()
    is_migrant = not any(term in last_location for term in aus_terms)
    print(is_migrant)
    return ", ".join(all_locations), is_migrant

df[["all_locations_worked", "is_migrant"]] = df["linkedin_jobs"].apply(
    lambda jobs: pd.Series(get_all_locations_worked(jobs))
)




# def get_all_locations_studied(degrees: List[dict]) -> Optional[str]:
#     if not degrees:
#         return None

#     all_locations = []

#     for degree in degrees:
#         if isinstance(degree, LinkedInEducation):
#             location = degree.location
#             if location:
#                 all_locations.append(degree.location)

#     return ", ".join(all_locations) if all_locations else None

# df["all_locations_studied"] = df["linkedin_education"].apply(get_all_locations_studied)


def get_all_job_titles(jobs: List[dict]) -> List:
    if not jobs:
        return None

    all_jobs = []

    for job in jobs:
        if isinstance(job, LinkedInJob):
            work = job.title
            if work:
                all_jobs.append(work)

    return all_jobs if all_jobs else None

df["all_job_titles"] = df["linkedin_jobs"].apply(get_all_job_titles)

def count_founder_roles(all_job_titles: List) -> bool:
    keywords = [
        "founder", "co-founder", "cofounder", "founding engineer",
        "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
        "Chief Executive Officer"
    ]
    founder_count = 0
    for title in all_job_titles:
        if any(keyword in title.lower() for keyword in keywords):
            founder_count += 1
    return founder_count

df["founder_count"] = df["all_job_titles"].apply(count_founder_roles)

def classify_founder_persona(job_titles: list[str]) -> str:
    """
    Classify founder persona based on job titles from most recent to oldest.
    Returns one of:
    ["Technical", "Product", "Design", "Growth / Marketing", "Business / Operations", "Other"]
    """
    for title in job_titles:
        title_lower = title.lower().strip()

        if any(kw in title_lower for kw in [
            "engineer", "developer", "machine learning", "data scientist", "cto", "software", "ai", "data"
        ]):
            return "Technical"

        if any(kw in title_lower for kw in [
            "product manager", "product owner", "head of product", "product lead", "product"
        ]):
            return "Product"

        if any(kw in title_lower for kw in [
            "designer", "ux", "ui", "design lead", "visual design"
        ]):
            return "Design"

        if any(kw in title_lower for kw in [
            "marketing", "growth", "performance", "brand", "campaign", "content",
            "sales", "account manager", "business development", "partnerships", "commercial"
        ]):
            return "Growth / Marketing"

        if any(kw in title_lower for kw in [
            "strategy", "operations", "ops", "consultant", "director",
            "business analyst", "mba", "finance"
        ]):
            return "Business / Operations"

    return "Other"

df["founder_persona"] = df["all_job_titles"].apply(classify_founder_persona)


def get_founder_companies(jobs: List[dict]) -> List[str]:
    """
    Return a list of companies where the title indicates a founder or founding role.
    """
    if not jobs:
        return []

    keywords = [
        "founder", "co-founder", "cofounder", "founding engineer",
        "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
        "chief executive officer"
    ]

    founder_companies = []

    for job in jobs:
        if job.title and any(keyword in job.title.lower() for keyword in keywords):
            if job.company:
                founder_companies.append(job.company.strip())

    return founder_companies

df["founder_companies"] = df.apply(
    lambda x: get_founder_companies(x["linkedin_jobs"])
    if x["is_founder"] == True
    else None,
    axis =1)

df.to_excel("data/linkedin_processed.xlsx", index=False)

html = df.to_html()
with open("table_view.html", "w", encoding="utf-8") as f:
    f.write(html)


    ### ADD TAG "SERIAL FOUNDER"

    # build space (in education)

    
# EXTRA TAGS:
# - founder_signal_strength 