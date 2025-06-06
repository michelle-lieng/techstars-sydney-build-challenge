from src.utilities.models import LinkedInJob
from typing import List
import re
from src.functions.startup_info import bing_find_linkedin_company_url, bing_funding_info, infer_startup_funding_stage, get_linkedin_company_followers_from_url
from datetime import datetime

def calculate_duration(start_date: str, end_date: str) -> str:
    """
    Calculate the duration between start_date and end_date in years and months.
    If end_date is 'present' or None, use today's date.
    Dates should be in the format 'Apr 2025'.
    """
    if not start_date:
        return "Unknown"

    # Parse start date
    try:
        start = datetime.strptime(start_date, "%b %Y")
    except ValueError:
        return "Invalid start date"

    # Handle end date
    if not end_date or end_date.strip().lower() == "present":
        end = datetime.today()
    else:
        try:
            end = datetime.strptime(end_date, "%b %Y")
        except ValueError:
            return "Invalid end date"

    # Calculate difference in months and years
    months = (end.year - start.year) * 12 + (end.month - start.month)
    years = months // 12
    rem_months = months % 12

    # Format result
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if rem_months > 0:
        parts.append(f"{rem_months} month{'s' if rem_months > 1 else ''}")
    if not parts:
        return "Less than a month"
    return " ".join(parts)

calculate_duration("Apr 2025", "Jan 2027")

founder_keywords = [
    "founder", "co-founder", "cofounder", "founding engineer",
    "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
    "chief executive officer"
]

def is_founder_role(title: str) -> bool:
    if not isinstance(title, str):
        return False

    title = title.lower()
    for keyword in founder_keywords:
        # \b means "word boundary" so 'cto' won't match 'director'
        if re.search(rf'\b{re.escape(keyword)}\b', title):
            return True
    return False

def get_current_startup_info(jobs: List[dict]) -> str: 
    if not jobs:
        return None
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.additional_notes or None
    
    return None

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

def count_founder_roles(all_job_titles: List) -> bool:
    founder_count = 0
    for title in all_job_titles:
        if is_founder_role(title):
            founder_count += 1
    return founder_count

def was_founder_before_from_count(is_founder: bool, founder_count: int) -> bool:
    if not is_founder:
        return founder_count > 0
    return founder_count > 1

def get_founder_companies(jobs: List[dict], founder_name: str, is_founder: bool, current_job_start_date) -> List[str]:
    """
    THESE ARE PREVIOUS COMPANIES!!!!!!!!

    Return a list of companies where the title indicates a founder or founding role.
    """
    if not jobs:
        return None
    
    # If the person is a current founder, skip the first job (assumed to be current)
    jobs_to_check = jobs[1:] if is_founder else jobs

    founder_companies = []

    for job in jobs_to_check:
        if is_founder_role(job.title):
            url = bing_find_linkedin_company_url(job.company.strip(), founder_name)
            bing_funding = bing_funding_info(job.company.strip(), founder_name, current_job_start_date)
            funding_info = "Bootstrapped" if bing_funding is None else infer_startup_funding_stage(bing_funding)
            if url != "Invalid":
                founder_companies.append({
                    "title": job.title,
                    "startup": job.company.strip(),
                    "startup_url": url,
                    "linkedin_follower_count": get_linkedin_company_followers_from_url(url),
                    #"bing_funding": bing_funding,
                    "funding_info": funding_info,
                    "startup_length": calculate_duration(job.start_date,job.end_date)
                })

    if founder_companies == []:
        return None

    return founder_companies