import os
from dotenv import load_dotenv
from flask import Flask
from mysqlSchema import FounderProfileDB

load_dotenv()

mysqlPass = os.getenv('MYSQL_PASSWORD')

app = Flask(__name__)
stealthDb = FounderProfileDB(app=app, password=mysqlPass)

print(stealthDb)

stealthDb.createFounderProfileTable()

founderId = stealthDb.insertFounder(
    name="Alice Example",
    linkedin_url="https://linkedin.com/in/alice",
    city="Melbourne",
    startup_name="CoolStartup",
    profile_completeness=90,
    tags=["AI", "Founder", "Australia"],
    gender="Female",
    ethnicity="Asian",
    data_source="Manual Entry"
)

founders = stealthDb.getAllFounders()
for founder in founders:
    print(founder)

stealthDb.deleteFounder(founder_id=founderId)

if __name__ == '__main__':
    app.run(debug=True)