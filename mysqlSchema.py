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

    def dbConnect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password
            )
            print("MySQL connection established")

            cursor = self.connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
            cursor.close()

            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print(f"Connect to database: {self.database}")

        except Error as e:
            print(f"Error connecting to MySQL: {e}")

    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("MySQL connection closed")

    def createFounderProfileTable(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()

            create_table_query = """
            CREATE TABLE IF NOT EXISTS founder_profile (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                linkedin_url VARCHAR(255),
                city VARCHAR(100),
                startup_name VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                profile_completeness TINYINT UNSIGNED DEFAULT 0 CHECK (profile_completeness BETWEEN 0 AND 100),
                tags JSON,
                gender ENUM('Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say'),
                ethnicity VARCHAR(100),
                data_source VARCHAR(100)
            ) ENGINE=InnoDB;
            """

            cursor.execute(create_table_query)
            self.connection.commit()
            print("Founder profile table created successfully")
            cursor.close()

        except Error as e:
            print(f"Error creating founder profile table: {e}")
        
    def insertFounder(self, name, linkedin_url=None, city=None, startup_name=None, 
                      profile_completeness=0, tags=None, gender=None, ethnicity=None, 
                      data_source=None):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()

            cursor = self.connection.cursor()

            tags_json = json.dumps(tags) if tags else None

            insert_query = """
            INSERT INTO founder_profile (
                name, linkedin_url, city, startup_name, profile_completeness,
                tags, gender, ethnicity, data_source
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            values = (
                name, linkedin_url, city, startup_name, profile_completeness, tags_json, gender, ethnicity, data_source
            )

            cursor.execute(insert_query, values)
            self.connection.commit()

            founder_id = cursor.lastrowid
            print(f"Founder profile inserted successfully with ID: {founder_id}")
            cursor.close()

            return founder_id
        
        except Error as e:
            print(f"Error inserting founder profile: {e}")
            return None
    
    def deleteFounder(self, founder_id):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            
            # SQL query to delete a founder profile
            delete_query = "DELETE FROM founder_profile WHERE id = %s"
            cursor.execute(delete_query, (founder_id,))
            self.connection.commit()
            
            success = cursor.rowcount > 0
            cursor.close()
            
            if success:
                print(f"Founder profile with ID {founder_id} deleted successfully")
            else:
                print(f"No founder profile found with ID {founder_id}")
                
            return success
            
        except Error as e:
            print(f"Error deleting founder profile: {e}")
            return False

    def getAllFounders(self):
        try:
            if not self.connection or not self.connection.is_connected():
                self.db_connect()
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM founder_profile")
            results = cursor.fetchall()
            cursor.close()

            return results

        except Error as e:
            print(f"Error fetching all founders: {e}")
            return []
    
    def getFounderById(self. founder_id):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect
        
            cursor = self.connection.cursor(dictionary=True)

            select_query = "SELECT * FROM founder_profile WHERE id = %s"
            cursor.execute(select_query, (founder_id))

            founder = cursor.fetchone()
            cursor.close()

            if founder and founder['tages']:
                founder['tags'] = json.loads(founder['tags'])

            return founder

        except Error as e:
            print(f"Error retrieving founder profile: {e}")
            return None
    
    def updateFounder(self, founder_id, **kwargs):
        try:
            if not self.connection or not self.connection.is_connected():
                self.connect()
                
            cursor = self.connection.cursor()
            
            if 'tags' in kwargs and kwargs['tags']:
                kwargs['tags'] = json.dumps(kwargs['tags'])
                
            set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())
            values.append(founder_id)
            
            update_query = f"UPDATE founder_profile SET {set_clause} WHERE id = %s"
            
            cursor.execute(update_query, values)
            self.connection.commit()
            
            success = cursor.rowcount > 0
            cursor.close()
            
            if success:
                print(f"Founder profile with ID {founder_id} updated successfully")
            else:
                print(f"No founder profile found with ID {founder_id}")
                
            return success
            
        except Error as e:
            print(f"Error updating founder profile: {e}")
            return False