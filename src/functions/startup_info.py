from src.utilities.prompts import startup_summary_prompt, startup_industry_prompt
from src.utilities.bing_function import bing_search
from src.utilities.gemini_function import gemini_call_with_pt
from datetime import datetime
import re
from typing import List, Dict, Optional
from difflib import SequenceMatcher
from src.utilities.classifiers import STEALTH_MODE

def check_is_stealth_mode(startup_name: str) -> bool:
    return startup_name.lower() in STEALTH_MODE


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

#url = "https://www.crunchbase.com/organization/bean-f57f"
#url = "https//www.google.com"
#url = "https://www.crunchbase.com/organization/bean-crunchy/company_financials"
#startup_name = "bean"
#is_valid_crunchbase_org_url(url, startup_name)

def extract_mentioned_years(text: str) -> List[int]:
    matches = re.findall(r"\b(19[8-9]\d|20[0-3]\d)\b", text)  # Year between 1980–2039
    return [int(m) for m in matches]

#text = 'Their latest funding was raised on Sep 11, 2013 from a Series C round. NextDocs is funded by 3 investors. OpenView and Bridgebank Capital are the most recent investors.'
#extract_mentioned_years(text)

def mentions_outdated_funding(text: str, startup_start_str: str) -> bool:
    try:
        startup_start = datetime.strptime(startup_start_str, "%b %Y")  # e.g. Jun 2024
        mentioned_years = extract_mentioned_years(text)
        return any(year < startup_start.year for year in mentioned_years)
    except:
        return False

#dat="Jun 2024"
#mentions_outdated_funding(text, dat)

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

############## NOW WE HAVE TO USE GEMINI TO GET ACTUAL INFO FROM FUNDING INFO!
# Rank mapping of funding stages
round_rank = {
    #"idea": 0,
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


###### GET STARTUP URL

# def bing_find_linkedin_company_url(startup_name: str, founder_name: str) -> str:
#     results = bing_search(f"site:linkedin.com/company {startup_name} {founder_name}", count=1)
#     for result in results:
#         url = result.get("url", "").lower()
#         print(url)
#         if "linkedin.com/company" in url:
#             return url  # <-- As soon as this runs, the function exits!
#     return None

def normalize(text):
    """Lowercase, remove non-alphanumerics for fuzzy matching."""
    return re.sub(r'[^a-z0-9]', '', text.lower())

def fuzzy_in(startup, url, threshold=0.85):
    norm_startup = normalize(startup)
    norm_url = normalize(url)
    # Try to find the best matching substring in the url for the startup name
    for i in range(len(norm_url) - len(norm_startup) + 1):
        window = norm_url[i:i+len(norm_startup)]
        ratio = SequenceMatcher(None, norm_startup, window).ratio()
        if ratio >= threshold:
            return True
    return False

def bing_find_linkedin_company_url(startup_name: str, founder_name: str) -> str:
    results = bing_search(f"site:linkedin.com/company {startup_name} {founder_name}", count=1)
    if not results:
        return "Invalid"
    url = results[0].get("url", "").lower()
    if "linkedin.com/company" not in url:
        return "Invalid"
    if fuzzy_in(startup_name, url):
        return url
    return "Invalid"

def get_linkedin_company_followers_from_url(company_url: str) -> int | None:
    """
    Given a LinkedIn company URL, search Bing for the number of followers and extract it from the snippet.
    Returns the number of followers as an int, or None if not found.
    """
    if company_url is None:
        return None
    
    if not company_url or company_url == "Invalid" or "linkedin.com/company" not in company_url:
        return "Unknown"

    # Search for the company URL with 'followers' in the query
    results = bing_search(f"{company_url} 'followers'", 1)
    if not results:
        return None

    snippet = results[0].get("snippet", "")
    # Extract the number of followers using regex
    match = re.search(r"([\d,\.]+)\s+followers", snippet)
    if match:
        return int(match.group(1).replace(",", ""))
    return None

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

def find_startup_industry(startup_info: str) -> str:
    summary = gemini_call_with_pt(
        input_info=startup_info,
        prompt_template=startup_industry_prompt,
        system_prompt="You are a professional startup analyst."
    )
    return summary

def uses_ai(bing_general_startup_info: str) -> bool:
    if not bing_general_startup_info:
        return None
    text = " ".join(item.get("snippet", "") for item in bing_general_startup_info if isinstance(item, dict))
    text = text.lower()
    return bool(re.search(r"\bai\b", text)) or "artificial intelligence" in text
