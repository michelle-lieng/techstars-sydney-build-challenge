import os
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from mysqlSchema import FounderProfileDB

load_dotenv()

mysqlPass = os.getenv('MYSQL_PASSWORD')

app = Flask(__name__)
CORS(app)
stealthDb = FounderProfileDB(app=app, password=mysqlPass)

print(stealthDb)

@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500

@app.route('/api/search', methods=['GET'])
def getData():
    try:
        filters = {
            'name': request.args.get('name'),
            'city': request.args.get('city'),
            'startup_name': request.args.get('startup'),
            'gender': request.args.get('gender'),
            'ethnicity': request.args.get('ethnicity'),
            'migrant': request.args.get('migrant')
        }

        tags = request.args.getlist('tags')
        if tags:
            filters['tags'] = tags
            
        # Remove keys with None or empty string values
        filters = {k: v for k, v in filters.items() if v}

        if filters:
            founders = stealthDb.searchFounders(filters)
        else:
            founders = stealthDb.getAllFounders()

        return jsonify(founders)
    except Exception as e:
        print(f"Error in /search route: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/founders/<int:id>', methods=['GET'])
def getFounder(id):
    try:
        founder = stealthDb.getFounderById(id)

        if founder:
            return jsonify(founder)
        else:
            return {}
    except Exception as e:
        print(f"Error in /founder/id route")
        return jsonify({"error": str(e)}), 500

@app.route('/api/addFounder', methods=['POST'])
def addFounder():
    try:
        # Parse incoming JSON
        founder = request.get_json()

        if founder is None:
            return jsonify({"error": "Invalid JSON"}), 400

        # Normalize booleans
        for key in ['is_current_founder', 'was_prev_founder', 'was_in_accelerator', 
                    'was_in_scaleup', 'was_in_bigtech', 'migrant', 'ai_in_curr_startup', 'is_stealth']:
            if key in founder:
                founder[key] = founder[key] == "True"

        def parse_bool(value):
            return str(value).strip().lower() == "true"
        # Insert into DB
        stealthDb.insertFounder(
            name=founder.get('name'),
            linkedin_url=founder.get('linkedin_url'),
            city=founder.get('city'),
            current_company=founder.get('current_company'),
            current_title=founder.get('current_title'),
            current_job_start=founder.get('current_job_start'),
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
            top_degree_end_date=founder.get('top_degree_end_date'),
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

        return jsonify({"message": "Founder added successfully"}), 201

    except Exception as e:
        print(f"Failed to insert founder {founder.get('name', '[unknown]')}: {e}")
        return jsonify({"error": f"Failed to insert founder: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)