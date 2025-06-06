import re
from typing import List, Union
from src.utilities.models import LinkedInJob, LinkedInEducation
import json
from pydantic import ValidationError

# Clean raw JSON text
def clean_json_response(raw_text: str) -> str:
    cleaned = re.sub(r"```json|```", "", raw_text.strip())  # remove code fences
    cleaned = cleaned.replace('\xa0', ' ').replace('Â·', '·')  # fix bad characters
    return cleaned

# Parse and validate structured JSON using Pydantic
def parse_linkedin_jobs(raw_text: str) -> Union[List[LinkedInJob], None]:
    try:
        cleaned = clean_json_response(raw_text)
        data = json.loads(cleaned)
        return [LinkedInJob(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[Job Parse Error] {e}")
        return None

def parse_linkedin_education(raw_text: str) -> Union[List[LinkedInEducation], None]:
    try:
        cleaned = clean_json_response(raw_text)
        data = json.loads(cleaned)
        return [LinkedInEducation(**item) for item in data]
    except (json.JSONDecodeError, ValidationError) as e:
        print(f"[Education Parse Error] {e}")
        return None
    

