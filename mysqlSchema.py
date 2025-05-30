import mysql.connector
from mysql.connector import Error
from datetime import datetime
import json

class FounderProfileDB:
    def __init__(self, host="localhost", user="root", password="", database="founder_db"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connect = None

    def connect(self):

        try:
            self.connection = mysql.connector.connect(
                host=self.host
                user=self.user
                password=self.password
            )