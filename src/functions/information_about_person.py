from src.utilities.models import LinkedInJob
from typing import List, Optional, Tuple

################ INFORMATION ABOUT EDUCATION 

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
        2: "Masters",
        1: "Bachelors",
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
        print(entry)
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
##########

def classifier_matches(all_companies: str, classifier: set) -> Tuple[bool, Optional[str]]:
    companies = [c.strip() for c in all_companies.split(",")]
    matches = [company for company in companies if company in classifier]
    if matches:
        return (True, ",".join(matches))
    else: 
        return (False, None)
    

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
    #print(all_locations[-1])
    last_location = all_locations[-1].lower()
    is_migrant = not any(term in last_location for term in aus_terms)
    #print(is_migrant)
    #return ", ".join(all_locations), is_migrant
    return all_locations, is_migrant

def current_city(all_locations_worked):
    if not all_locations_worked or not isinstance(all_locations_worked, list) or not all_locations_worked[0]:
        return None
    return all_locations_worked[0].split(",")[0]