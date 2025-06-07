from flask import Flask, current_app
from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor
import json
from datetime import datetime
from createTags import createTags

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

    def dropFounderTable(self):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()

                drop_table_query = """
                DROP TABLE founder_profile
                """
                cursor.execute(drop_table_query)
                self.mysql.connection.commit()
                print("Founder profile table dropped")
                cursor.close()
            except Exception as e:
                print(f"Error creating founder profile table: {e}")

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
                    current_company VARCHAR(255),
                    current_title VARCHAR(255),
                    current_job_start VARCHAR(50),
                    time_in_current_role VARCHAR(255),
                    is_current_founder BOOLEAN,
                    curr_startup_funding_stage VARCHAR(255),
                    curr_startup_url VARCHAR(255),
                    curr_startup_info VARCHAR(255),
                    curr_startup_industry VARCHAR(255),
                    ai_in_curr_startup BOOLEAN,
                    was_prev_founder BOOLEAN,
                    all_founded_companies JSON,
                    top_degree VARCHAR(255),
                    top_degree_label VARCHAR(50),
                    top_degree_end_date VARCHAR(50),
                    was_in_accelerator BOOLEAN,
                    accelerators_worked_in JSON,
                    was_in_scaleup BOOLEAN,
                    scaleups_worked_in JSON,
                    was_in_bigtech BOOLEAN,
                    bigtechs_worked_in JSON,
                    gender ENUM('Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say'),
                    migrant BOOLEAN,
                    tags JSON,
                    is_stealth BOOLEAN,
                    linkedin_follower_count INT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                ) ENGINE=InnoDB;
                """

                cursor.execute(create_table_query)
                self.mysql.connection.commit()
                print("Founder profile table created successfully")
                cursor.close()

            except Exception as e:
                print(f"Error creating founder profile table: {e}")
 
    def insertFounder(self, name, linkedin_url=None, city=None, current_company=None, 
                      current_title=None, current_job_start=None, time_in_current_role=None, is_current_founder=False, curr_startup_funding_stage=None, 
                      curr_startup_url=None, curr_startup_info=None, curr_startup_industry=None, ai_in_curr_startup=None,
                      was_prev_founder=False, all_founded_companies=None, top_degree=None, top_degree_label=None, top_degree_end_date=None,
                      was_in_accelerator=False, accelerators_worked_in=None, was_in_scaleup=False, scaleups_worked_in=None, was_in_bigtech=False,
                      bigtechs_worked_in=None, gender=None, migrant=False, is_stealth=False, linkedin_follower_count=0):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor()
                tags = createTags(is_current_founder=is_current_founder, ai_in_curr_startup=ai_in_curr_startup, was_prev_founder=was_prev_founder,
                                  top_degree_label=top_degree_label,was_in_accelerator=was_in_accelerator, was_in_scaleup=was_in_scaleup,
                                  was_in_bigtech=was_in_bigtech, is_migrant=migrant, is_stealth=is_stealth)

                all_founded_companies__json = json.dumps(all_founded_companies) if all_founded_companies else None
                accelerators_worked_in__json = json.dumps(accelerators_worked_in) if accelerators_worked_in else None
                scaleups_worked_in__json = json.dumps(scaleups_worked_in) if scaleups_worked_in else None
                bigtechs_worked_in__json = json.dumps(bigtechs_worked_in) if bigtechs_worked_in else None

                tags_json = json.dumps(tags) if tags else None

                insert_query = """
                INSERT INTO founder_profile (
                    name, linkedin_url, city, current_company, current_title, current_job_start, time_in_current_role, is_current_founder, curr_startup_funding_stage,
                    curr_startup_url, curr_startup_info, curr_startup_industry, ai_in_curr_startup, was_prev_founder, all_founded_companies,
                    top_degree, top_degree_label, top_degree_end_date, was_in_accelerator, accelerators_worked_in, was_in_scaleup, scaleups_worked_in,
                    was_in_bigtech, bigtechs_worked_in, gender, migrant, tags, is_stealth, linkedin_follower_count
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                values = (
                    name, linkedin_url, city, current_company, current_title, current_job_start, time_in_current_role, is_current_founder, curr_startup_funding_stage,
                    curr_startup_url, curr_startup_info, curr_startup_industry, ai_in_curr_startup, was_prev_founder, all_founded_companies__json,
                    top_degree, top_degree_label, top_degree_end_date, was_in_accelerator, accelerators_worked_in__json, was_in_scaleup, scaleups_worked_in__json,
                    was_in_bigtech, bigtechs_worked_in__json, gender, migrant, tags_json, is_stealth, linkedin_follower_count
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
                    if founder.get('all_founded_companies') and isinstance(founder['all_founded_companies'], str):
                        founder['all_founded_companies'] = json.loads(founder['all_founded_companies'])

                    if founder.get('accelerators_worked_in') and isinstance(founder['accelerators_worked_in'], str):
                        founder['accelerators_worked_in'] = json.loads(founder['accelerators_worked_in'])
                    
                    if founder.get('scaleups_worked_in') and isinstance(founder['scaleups_worked_in'], str):
                        founder['scaleups_worked_in'] = json.loads(founder['scaleups_worked_in'])

                    if founder.get('bigtechs_worked_in') and isinstance(founder['bigtechs_worked_in'], str):
                        founder['bigtechs_worked_in'] = json.loads(founder['bigtechs_worked_in'])
                    
                    if founder.get('tags') and isinstance(founder['tags'], str):
                        founder['tags'] = json.loads(founder['tags'])

                return results

            except Exception as e:
                print(f"Error fetching all founders: {e}")
                return []
    
    def getFounderById(self, founder_id):
        with self.app.app_context():
            try:
                cursor = self.mysql.connection.cursor(DictCursor)

                select_query = "SELECT * FROM founder_profile WHERE id = %s"
                cursor.execute(select_query, (founder_id,))

                founder = cursor.fetchone()
                cursor.close()

                if founder and founder['tags']:
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
                cursor = self.mysql.connection.cursor(DictCursor)

                # Base query
                query = "SELECT * FROM founder_profile WHERE 1=1"
                params = []

                # Apply filters
                if 'name' in filters:
                    query += " AND name LIKE %s"
                    params.append(f"%{filters['name']}%")

                # City filter
                if 'city' in filters:
                    query += " AND city = %s"
                    params.append(filters['city'])

                # Startup name filter (only if current founder)
                if 'startup_name' in filters:
                    query += " AND is_current_founder = TRUE AND current_company LIKE %s"
                    params.append(f"%{filters['startup_name']}%")

                # Gender filter
                if 'gender' in filters:
                    query += " AND gender = %s"
                    params.append(filters['gender'])

                # Migrant filter (expects boolean)
                if 'migrant' in filters:
                    query += " AND migrant = %s"
                    params.append(filters['migrant'])

                # Tags filter (assumes list of tags and checks overlap)
                if 'tags' in filters and filters['tags']:
                    for tag in filters['tags']:
                        query += " AND JSON_CONTAINS(tags, %s)"
                        params.append(json.dumps(tag))

                cursor.execute(query, params)
                results = cursor.fetchall()
                cursor.close()

                # Parse JSON fields
                for founder in results:
                    if founder.get('tags') and isinstance(founder['tags'], str):
                        founder['tags'] = json.loads(founder['tags'])

                return results
        
            except Exception as e:
                print(f"Error searching founders: {e}")
                return []