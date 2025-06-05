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

if __name__ == '__main__':
    app.run(debug=True)