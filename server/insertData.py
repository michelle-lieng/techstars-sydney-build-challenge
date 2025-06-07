import os
from dotenv import load_dotenv
from flask import Flask
from mysqlSchema import FounderProfileDB
import json
from datetime import datetime

load_dotenv()

mysqlPass = os.getenv('MYSQL_PASSWORD')

app = Flask(__name__)
stealthDb = FounderProfileDB(app=app, password=mysqlPass)
stealthDb.dropFounderTable()
stealthDb.createFounderProfileTable()

with open('../founders.json', 'r') as f:
    data = json.load(f)

founders = data.get("founders", [])

for founder in founders:
    try:
        # Parse booleans from strings
        for key in ['is_current_founder', 'was_prev_founder', 'was_in_accelerator', 
                    'was_in_scaleup', 'was_in_bigtech', 'migrant', 'ai_in_curr_startup', 'is_stealth']:
            if key in founder:
                founder[key] = founder[key] == "True"
        
        def parse_bool(value):
            return str(value).strip().lower() == "true"

        # Call insertFounder with keyword unpacking
        stealthDb.insertFounder(
            name=founder.get('name'),
            linkedin_url=founder.get('linkedin_url'),
            city=founder.get('city'),
            current_company=founder.get('current_company'),
            current_title=founder.get('current_title'),
            current_job_start=founder.get("current_job_start"),
            time_in_current_role=founder.get('time_in_current_role'),
            is_current_founder=parse_bool(founder.get('is_current_founder', False)),
            curr_startup_funding_stage=founder.get('curr_startup_funding_stage'),
            curr_startup_url=founder.get('curr_startup_url'),
            curr_startup_info=founder.get('curr_startup_info'),
            curr_startup_industry=founder.get('curr_startup_industry'),
            ai_in_curr_startup=parse_bool(founder.get('ai_in_curr_startup', False)),
            was_prev_founder=parse_bool(founder.get('was_prev_founder', False)),
            all_founded_companies=founder.get('all_founded_companies'),
            top_degree=founder.get('top_degree'),
            top_degree_label=founder.get('top_degree_label'),
            top_degree_end_date=founder.get("top_degree_end_date"),
            was_in_accelerator=parse_bool(founder.get('was_in_accelerator', False)),
            accelerators_worked_in=founder.get('accelerators_worked_in'),
            was_in_scaleup=parse_bool(founder.get('was_in_scaleup', False)),
            scaleups_worked_in=founder.get('scaleups_worked_in'),
            was_in_bigtech=parse_bool(founder.get('was_in_bigtech', False)),
            bigtechs_worked_in=founder.get('bigtechs_worked_in'),
            gender=founder.get('gender'),
            migrant=founder.get('migrant', False),
            is_stealth=parse_bool(founder.get('is_stealth', False)),
            linkedin_follower_count=founder.get('linkedin_follower_count')
        )
    except Exception as e:
        print(f"Failed to insert founder {founder.get('name')}: {e}")

founders = stealthDb.getAllFounders()

for founder in founders:
    print(founder)