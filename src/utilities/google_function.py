import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_SEARCH_CX")

def google_search(query: str, count: int = 1):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": GOOGLE_CX,
        "q": query,
        "num": count,
    }
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "title": item.get("title"),
            "url": item.get("link"),
            "snippet": item.get("snippet")
        })
    return results

# Example usage
results = google_search("site:linkedin.com/company ToothFairyAI")
results = google_search("dogs")

startup_name = "Bean"
founder_name = "Pankrit Jindal"

results = google_search(f"site: crunchbase.com {startup_name} {founder_name} funding round", count=3)
print(results)
results = google_search(f"site:linkedin.com/company {startup_name} {founder_name}", count=1)
company_url = results[0]["url"]
results = google_search(f"{company_url} 'followers'", 1)


# DOES BADLY
#google_search("https://www.linkedin.com/company/beantheapp 'followers",1)