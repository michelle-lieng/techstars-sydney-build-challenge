import os
from dotenv import load_dotenv
from flask import Flask, jsonify
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
        founders = stealthDb.getAllFounders()
        return jsonify(founders)
    except Exception as e:
        print(f"Error in /search route: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)