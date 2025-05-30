import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

mysqlPass = os.getenv('MYSQL_PASSWORD')

stealthDb = mysql.connector.connect(
    host ="localhost",
    user ="root",
    password =mysqlPass
)

print(stealthDb)

stealthDb.close()