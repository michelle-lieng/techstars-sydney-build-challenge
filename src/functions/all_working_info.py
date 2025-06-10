from src.utilities.models import LinkedInJob
from typing import List, Optional

########## current working info ###############
def get_current_company(jobs: List[dict]) -> str:
    if not jobs:
        return "Unemployed"
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.company
    
    return "Unemployed"

def get_current_title(jobs: List[dict]) -> str: 
    if not jobs:
        return "Unemployed"
    
    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.title
    
    return "Unemployed"

def get_current_start_date(jobs: List[dict]) -> str:
    if not jobs:
        return None

    for job in jobs:
        # Ensure it's a Pydantic LinkedInJob instance
        if isinstance(job, LinkedInJob) and job.end_date.strip().lower() == "present":
            return job.start_date

    return None

############ all working info #############333

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