import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_SEARCH_CX")

def google_search(query: str, count: int = 10):
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
#results = google_search("site:linkedin.com/company ToothFairyAI")
#results = google_search("dogs")
results = google_search("site:linkedin.com/in/ 'Hobart, Tasmania, Australia' 'founder'")
# print(results)
# for result in results:
#     #print(type(result))
#     print(result["url"])

for result in results:
    snippet = result["snippet"]
    url = result["url"]
    # Look for patterns like "4 years", "10 years", etc.
    match = re.search(r"(\d+)\s+years?", snippet)
    if match:
        years = int(match.group(1))
        if years > 3:
            continue
            #print("OLD")
            #print(snippet)  # Skip this result if years > 3

    # Skip if "followers" is above or equal to 2K
    match_followers = re.search(r"([\d,.]+)\s*K?\s*followers", snippet, re.IGNORECASE)
    if match_followers:
        followers_str = match_followers.group(1).replace(',', '')
        if 'K' in match_followers.group(0):
            followers = float(followers_str) * 1000
        else:
            followers = float(followers_str)
        if followers >= 2000:
            #print("TOO MANY FOLLOWERS")
            #print(snippet)
            continue  # Skip this result

    print(url)
    print(snippet)


# startup_name = "lorikeet"
# founder_name = "Jamie Hall"

# results = google_search(f"site: crunchbase.com/organization/ {startup_name} {founder_name} funding round", count=3)
# print(results)

# startup_name = "Bean"
# founder_name = "Pankrit Jindal"
# results = google_search(f"site:linkedin.com/company {startup_name} {founder_name}", count=1)
# company_url = results[0]["url"]
# results = google_search(f"{company_url} 'followers'", 1)


# DOES BADLY
#google_search("https://www.linkedin.com/company/beantheapp 'followers",1)