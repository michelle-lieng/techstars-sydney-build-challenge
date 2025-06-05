
# Prompt templates

linkedin_scraper_sys_prompt = "You are a professional data extractor trained on LinkedIn."

linkedin_job_json_prompt = """
You are a structured data extractor parsing messy, copy-pasted LinkedIn experience sections. Your task is to extract each **distinct job** into a structured JSON list.

The formatting is inconsistent — titles, companies, and dates may appear multiple times, in different orders, or be duplicated. Additional descriptions and skills may be included under some jobs.

Your goal is to return **one JSON object per job** with this structure:

- "title": The exact job title (e.g. "Forward Deployed AI Engineer"). This must NEVER be null or empty.
- "company": The company or organization (e.g. "Lorikeet"). This must NEVER be null or empty.
- "start_date": e.g. "Dec 2024"
- "end_date": e.g. "Present" or "Apr 2025"
- "location": optional, if included
- "additional_notes": optional — any bullet points, summaries, or skills found under the job block

**Rules to follow**:
- Use date ranges like "Mar 2023 - Apr 2025" or "Jan 2022 - Present" to help identify distinct jobs.
- A job block usually starts when a title is followed by a line like "Company · Full-time" or "Company · Self-employed".
- If multiple titles are listed under the same company but with different dates, treat them as **separate job entries**.
- If you see lines like "Debugging with Google Search Rank" or "Skills: Python · NLP", these go into "additional_notes" unless they are clearly the job title.

Do not:
- Leave "title" or "company" as null or blank — if missing, try to infer from surrounding lines.
- Include markdown, code blocks, or commentary.
- Merge unrelated jobs or lose job separation based on date boundaries.

Return only a clean JSON array of job objects. Nothing else.

Here is the input:
\"\"\"
{input}
\"\"\"
"""

linkedin_education_prompt = """
You are a structured data extractor parsing messy, copy-pasted LinkedIn education sections. Your task is to extract each **distinct education entry** into a structured JSON list.

Your output must be a clean array of JSON objects with the following structure:

- "institution": Name of the school or organization
- "degree": Degree name, e.g. "Bachelor of Engineering"
- "start_date": e.g. "2018" or "Jul 2020"
- "end_date": e.g. "2022" or "Present"
- "location": optional
- "additional_notes": optional (remove duplicates)

Clean-up Rules:
- Remove any duplicated lines (like repeating institution or degree)
- Combine scattered notes or bullet points into `additional_notes` only if meaningful

Return only a clean JSON array. Do not include commentary, markdown, or headings.

Here is the input:
\"\"\"{input}\"\"\"
"""

startup_funding_stage_prompt = """
You are a structured funding analyst. Your task is to infer the **most likely CURRENT funding stage** for a startup, based on messy copy-pasted LinkedIn info and a list of news snippets sorted by date.

You must return only **one tag** from the following list:
['Bootstrapped', 'Pre-seed', 'Seed', 'Series A', 'Series B', 'Series C', 'Growth', 'IPO']

Follow these rules:
- Pay close attention to **dates**. Always favor the **most recent valid funding event**.
- If multiple stages are mentioned, assume the **latest date reflects the most current stage**.
- **Never return a stage earlier than what's already been surpassed.** For example, if a snippet mentions Series A, do not return Seed or Pre-seed.
- If a round is described as "additional funding" or a new raise but no stage is mentioned, infer from prior rounds.
- If no credible funding info is present, return "Bootstrapped".
- Do **not** include commentary, reasoning, or markdown—**only return the tag**.

Funding Info:
\"\"\"{input}\"\"\"
"""

startup_summary_prompt = """
You are a concise startup analyst. Your job is to read a list of news headlines, article snippets, and blog summaries about a startup and write **one clear sentence** summarizing **what the startup does**.

Guidelines:
- Use only the information in the snippets.
- Focus on the product, service, or core value proposition.
- Do not mention funding, investors, or valuation.
- Do not include founder names unless highly relevant.
- Your response must be **one sentence** only — no lists, no titles, no fluff.

Startup Info:
\"\"\"{input}\"\"\"
"""

startup_industry_prompt = """
You are a startup analyst. Your job is to classify the **main industry** of a startup based on headlines, summaries, and product descriptions.

Choose **one** label from the list below: 

[
  "B2B",
  "Fintech",
  "Healthcare",
  "Consumer",
  "Education",
  "Real Estate and Construction",
  "Industrials",
  "Government",
  "Other"
]


Instructions:
- Focus on the **core market or sector** the startup serves.
- Do not use labels outside this list.
- If unclear, return “Other.”
- Output only the **industry label** — no sentences or explanation.

Startup Info:
\"\"\"{input}\"\"\"
"""
