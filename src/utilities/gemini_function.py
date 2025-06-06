import os
from dotenv import load_dotenv
from openai import OpenAI
import pandas as pd
from src.utilities.prompts import linkedin_job_json_prompt

# Load variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = "gemini-2.0-flash"

def gemini_with_query(query: str, system_prompt: str) -> str:
    messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": query},
                ]

    completion = client.chat.completions.create(
                    model="gemini-2.0-flash",
                    messages=messages,
                    response_format={"type": "text"},
                    temperature=0
                )

    return completion.choices[0].message.content.strip()

# Call Gemini API to extract job JSON
# not called extract_linkedin anymore
def gemini_call_with_pt(input_info: str, prompt_template: str, system_prompt: str) -> str:
    prompt = prompt_template.format(input=input_info)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=messages,
            response_format={"type": "text"},
            temperature=0
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"ERROR: {e}"
    
if __name__ == "__main__":
    #system_prompt="You are an expert about animals."
    #query="What is a dog?"
    #print(gemini_with_query(query, system_prompt))

    system_prompt= "You are a professional data extractor trained on LinkedIn."
    prompt_template=linkedin_job_json_prompt
    input= pd.read_excel("data/input.xlsx").loc[0,'linkedin_job_dump']
    print(gemini_call_with_pt(input, prompt_template, system_prompt))