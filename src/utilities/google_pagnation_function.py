import os
import requests
from dotenv import load_dotenv
from datetime import datetime
import re

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
GOOGLE_CX = os.getenv("GOOGLE_SEARCH_CX")

def google_search(query: str, total_count: int = 30):
    endpoint = "https://www.googleapis.com/customsearch/v1"
    results = []
    
    for start in range(1, total_count + 1, 10):
        params = {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_CX,
            "q": query,
            "num": min(10, total_count - len(results)),  # max 10 per request
            "start": start
        }
        response = requests.get(endpoint, params=params)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])
        if not items:
            break

        for item in items:
            results.append({
                "title": item.get("title"),
                "url": item.get("link"),
                "snippet": item.get("snippet")
            })

        if len(results) >= total_count:
            break

    return results

#results = google_search("site:linkedin.com/in/ 'Hobart, Tasmania, Australia' 'founder'", total_count=11)
#results = google_search("site:linkedin.com/in 'founder' 'Darwin, Northern Territory, Australia'", total_count=11)
# results = google_search("site:linkedin.com/in 'founder' 'Melbourne, Victoria, Australia'", total_count=20)
#results = google_search("site:linkedin.com/in 'founder' 'Perth, Western Australia, Australia'", total_count=20)
#results = google_search("site:linkedin.com/in 'founder' 'Brisbane, Queensland, Australia'", total_count=20)
results = google_search("site:linkedin.com/in 'founder' 'Adelaide, South Australia, Australia'", total_count=20)

founder_keywords = [
    "founder", "co-founder", "cofounder", "founding engineer",
    "founding member", "founding team", "cto", "ceo", "cpo", "cso", "chief",
    "chief executive officer", "owner"
]

for i, result in enumerate(results, 1):
    #print(f"Result {i}")
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
    
    # even remove if it says 2K etc.
    if "2K" in snippet:
        continue

    if any(keyword in snippet.lower() for keyword in founder_keywords):
        print(url)
        print(snippet)