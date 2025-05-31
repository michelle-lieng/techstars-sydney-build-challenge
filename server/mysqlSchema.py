from flask import Flask, current_app
from flask_mysqldb import MySQL
import json
from datetime import datetime

class FounderProfileDB:
    def __init__(self, app=None, host="localhost", user="root", password="", database="founder_db"):
        self.app = app
        self.mysql = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database

        if app is not None:
            self.initApp(app)

    def initApp(self, app):
        self.app = app

        app.config['MYSQL_HOST'] = self.host
        app.config['MYSQL_USER'] = self.user
        app.config['MYSQL_PASSWORD'] = self.password
        app.config['MYSQL_DB'] = self.database
        app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

        self.mysql = MySQL(app)

        with app.app_context():
            self.createDatabaseIfNotExists(self.database)
            self.createFounderProfileTable()

    def createDatabaseIfNotExists(self, database):
        originalDb = self.app.config.get('MYSQL_DB')

        try:
            self.app.config['MYSQL_DB'] = ''

            conn = self.mysql.connection
            cursor = conn.cursor()

            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
            conn.commit()

            cursor.close()
            print(f"Database {database} created or already exists")
        except Exception as e:
            print(f"Error creating database: {e}")
        finally:
            self.app.config['MYSQL_DB'] = originalDb

    def createFounderProfileTable(self):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()

                create_table_query = """
                CREATE TABLE IF NOT EXISTS founder_profile (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255),
                    linkedin_url VARCHAR(255),
                    city VARCHAR(100),
                    startup_name VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    profile_completeness TINYINT UNSIGNED DEFAULT 0 CHECK (profile_completeness BETWEEN 0 AND 100),
                    tags JSON,
                    gender ENUM('Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say'),
                    ethnicity VARCHAR(100),
                    migrant BOOLEAN,
                    data_source VARCHAR(100)
                ) ENGINE=InnoDB;
                """

                cursor.execute(create_table_query)
                self.mysql.connection.commit()
                print("Founder profile table created successfully")
                cursor.close()

            except Exception as e:
                print(f"Error creating founder profile table: {e}")


        
    def insertFounder(self, name, linkedin_url=None, city=None, startup_name=None, 
                      profile_completeness=0, tags=None, gender=None, ethnicity=None, 
                      migrant=None, data_source=None):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()

                tags_json = json.dumps(tags) if tags else None

                insert_query = """
                INSERT INTO founder_profile (
                    name, linkedin_url, city, startup_name, profile_completeness,
                    tags, gender, ethnicity, migrant, data_source
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    name, linkedin_url, city, startup_name, profile_completeness, tags_json, gender, ethnicity, migrant, data_source
                )

                cursor.execute(insert_query, values)
                self.mysql.connection.commit()

                founder_id = cursor.lastrowid
                print(f"Founder profile inserted successfully with ID: {founder_id}")
                cursor.close()

                return founder_id
            
            except Exception as e:
                print(f"Error inserting founder profile: {e}")
                return None
        
    def deleteFounder(self, founder_id):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()
                
                # SQL query to delete a founder profile
                delete_query = "DELETE FROM founder_profile WHERE id = %s"
                cursor.execute(delete_query, (founder_id,))
                self.mysql.connection.commit()
                
                success = cursor.rowcount > 0
                cursor.close()
                
                if success:
                    print(f"Founder profile with ID {founder_id} deleted successfully")
                else:
                    print(f"No founder profile found with ID {founder_id}")
                    
                return success
                
            except Exception as e:
                print(f"Error deleting founder profile: {e}")
                return False

    def getAllFounders(self):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()
                cursor.execute("SELECT * FROM founder_profile")
                results = cursor.fetchall()
                cursor.close()

                for founder in results:
                    if founder.get('tags') and isinstance(founder['tags'], str):
                        founder['tags'] = json.loads(founder['tags'])

                return results

            except Exception as e:
                print(f"Error fetching all founders: {e}")
                return []
    
    def getFounderById(self, founder_id):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor(dictionary=True)

                select_query = "SELECT * FROM founder_profile WHERE id = %s"
                cursor.execute(select_query, (founder_id))

                founder = cursor.fetchone()
                cursor.close()

                if founder and founder['tages']:
                    founder['tags'] = json.loads(founder['tags'])

                return founder

            except Exception as e:
                print(f"Error retrieving founder profile: {e}")
                return None
    
    def updateFounder(self, founder_id, **kwargs):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()
                
                if 'tags' in kwargs and kwargs['tags']:
                    kwargs['tags'] = json.dumps(kwargs['tags'])
                    
                set_clause = ", ".join([f"{key} = %s" for key in kwargs.keys()])
                values = list(kwargs.values())
                values.append(founder_id)
                
                update_query = f"UPDATE founder_profile SET {set_clause} WHERE id = %s"
                
                cursor.execute(update_query, values)
                self.mysql.connection.commit()
                
                success = cursor.rowcount > 0
                cursor.close()
                
                if success:
                    print(f"Founder profile with ID {founder_id} updated successfully")
                else:
                    print(f"No founder profile found with ID {founder_id}")
                    
                return success
                
            except Exception as e:
                print(f"Error updating founder profile: {e}")
                return False
    
    def searchFounders(self, filters):
    with self.app.app_context():
        try:
            cursor = self.mysql.connection.cursor()

            # Base query
            query = "SELECT * FROM founder_profile WHERE 1=1"
            params = []

            # Apply filters
            if 'name' in filters:
                query += " AND name LIKE %s"
                params.append(f"%{filters['name']}%")
            if 'city' in filters:
                query += " AND city = %s"
                params.append(filters['city'])
            if 'startup_name' in filters:
                query += " AND startup_name LIKE %s"
                params.append(f"%{filters['startup_name']}%")
            if 'gender' in filters:
                query += " AND gender = %s"
                params.append(filters['gender'])
            if 'ethnicity' in filters:
                query += " AND ethnicity = %s"
                params.append(filters['ethnicity'])
            if 'migrant' in filters:
                query += " AND migrant = %s"
                params.append(filters['migrant'])

            cursor.execute(query, params)
            results = cursor.fetchall()
            cursor.close()

            # Convert tags from JSON string to Python list
            for founder in results:
                if founder.get('tags') and isinstance(founder['tags'], str):
                    founder['tags'] = json.loads(founder['tags'])

            return results

        except Exception as e:
            print(f"Error searching founders: {e}")
            return []