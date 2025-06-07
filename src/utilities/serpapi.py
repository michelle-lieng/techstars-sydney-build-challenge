from serpapi import GoogleSearch
import os

# Set your SerpAPI key (store this securely)
SERPAPI_KEY = os.getenv("SERPAPI_KEY")  # or replace with your API key string directly

def get_google_results(query, location="Australia", num_results=10):
    params = {
        "engine": "google",                    # use real Google search engine
        "q": query,                            # your query string
        "api_key": SERPAPI_KEY,
        "num": num_results,                    # number of results to return (max 100)
        "hl": "en",                            # language
        "gl": "au",                            # geo location for country-specific results
        "location": location                   # optional: makes results more location-specific
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    # Return organic results only
    return results.get("organic_results", [])

#query = "site:linkedin.com/company/toothfairy-ai 'followers'"
query = "site:linkedin.com/company/bizflashai 'followers'"
search_results = get_google_results(query)
print(search_results)
print(search_results["title"])
print(search_results["displayed_link"])
print(search_results["snippet"])
print(search_results["url"])


    # for i, result in enumerate(search_results, 1):
    #     print(f"{i}. {result['title']}")
    #     print(result['link'])
    #     print(result.get("snippet", ""))
    #     print("-" * 80)
