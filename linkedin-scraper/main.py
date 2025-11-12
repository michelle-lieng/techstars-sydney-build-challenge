"""
Followed: https://github.com/joeyism/linkedin_scraper
"""

from selenium import webdriver
from linkedin_scraper import Person, actions
import time, random, re, os, json
from datetime import datetime
from dotenv import load_dotenv
from profile_urls import profile_urls # profile_urls = a list of linkedin urls

load_dotenv()

# Login credentials
email = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

def safe_serialize(obj, seen=None):
    if seen is None:
        seen = set()
    if id(obj) in seen:
        return None
    seen.add(id(obj))

    if isinstance(obj, list):
        return [safe_serialize(i, seen) for i in obj]
    elif isinstance(obj, dict):
        return {k: safe_serialize(v, seen) for k, v in obj.items()}
    elif hasattr(obj, "__dict__"):
        data = {}
        for key, value in obj.__dict__.items():
            if key == "driver":
                continue
            try:
                data[key] = safe_serialize(value, seen)
            except Exception:
                data[key] = str(value)
        return data
    elif isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    else:
        return str(obj)

# Step 1: Start browser + login
driver = webdriver.Chrome()
actions.login(driver, email=email, password=password)

# Step 2: Loop through profiles
for profile_url in profile_urls:
    try:
        username = re.search(r"/in/([^/]+)/?", profile_url).group(1)

        # Prevent auto scraping
        person = Person(profile_url, driver=driver, scrape=False)

        # Manually trigger scraping but keep the session alive
        person.scrape(close_on_complete=False)

        # Serialize data
        person_data = safe_serialize(person)

        # Save JSON
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"profile_{username}_{timestamp}.json"
        os.makedirs("output", exist_ok=True)
        with open(f"output/{filename}", "w", encoding="utf-8") as f:
            json.dump(person_data, f, ensure_ascii=False, indent=4)

        print(f"✅ Scraped and saved: {username}")
        time.sleep(random.uniform(10, 20))

    except Exception as e:
        print(f"⚠️ Error scraping {profile_url}: {e}")

driver.quit()
