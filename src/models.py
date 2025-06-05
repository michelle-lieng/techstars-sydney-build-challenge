from pydantic import BaseModel
from typing import Optional

# Define the Pydantic model
class LinkedInJob(BaseModel):
    company: str
    title: str
    start_date: str
    end_date: str
    location: Optional[str] = None
    additional_notes: Optional[str] = None

class LinkedInEducation(BaseModel):
    institution: str
    degree: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    location: Optional[str] = None
    additional_notes: Optional[str] = None