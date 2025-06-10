import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("BING_API_KEY")
ENDPOINT = "https://api.bing.microsoft.com/v7.0/search"

def bing_search(query: str, count: int = 10):
    headers = {"Ocp-Apim-Subscription-Key": API_KEY}
    params = {"q": query, "count": count}
    response = requests.get(ENDPOINT, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    results = []
    for item in data.get("webPages", {}).get("value", []):
        raw_date = item.get("datePublished", "Unknown")
        clean_date = "Unknown"
        if raw_date != "Unknown":
            try:
                clean_date = datetime.fromisoformat(raw_date).date().isoformat()
            except Exception:
                pass  # in case the format is wrong
        results.append({
            "name": item["name"],
            "url": item["url"],
            "snippet": item["snippet"],
            "date": clean_date
        })
    return results

# Example usage
if __name__ == "__main__":
    #results = bing_search("Information startup Lorikeet Jamie Hall about")
    #results = bing_search("site:linkedin.com BizFlash Bennett Carroll")
    #results = bing_search("site:crunchbase.com earlywork Dan Brockwell funding round")
    #results = bing_search("site:crunchbase.com Lorikeet Jamie Hall funding round")
    #results = bing_search("site:techcrunch.com OR site:businessinsider.com OR site:startupdaily.net 'Lorikeet' 'Series A' OR 'Seed' OR 'raises' OR 'funding'")
    #results = bing_search("site:linkedin.com Sydney startup founder")
    #for r in results:
    #    print(f"{r['date']} | {r['name']}\n{r['url']}\n")
    #results = bing_search("https://www.linkedin.com/company/beantheapp/about")
    #results = bing_search("https://www.linkedin.com/company/nextdocs-io",1)
    #results = bing_search("site:linkedin.com Ud.me/pathol.org Emmanuel (Mannie) Nsanga")
    #results = bing_search("site:linkedin.com/company deepmental-ai Emmanuel (Mannie) Nsanga")
    #results = bing_search("site:linkedin.com/company Propagate.Ink Nathan Hu", 1)
    results = bing_search("https://www.linkedin.com/company/toothfairy-ai 'followers'", 1)
    print(results)
