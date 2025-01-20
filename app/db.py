import mysql.connector
import os

DATABASE = os.getenv("MYSQL_DATABASE")
USERNAME = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOSTNAME = os.getenv("MYSQLHOST")

def create_db(USERNAME: str, PASSWORD: str, host: str):
    try:
        with mysql.connector.connect(
            user = USERNAME,
            host = host,
            PASSWORD = PASSWORD
        ) as connection:
            create_db = "CREATE DATABASE event_management_sys"
            with connection.cursor() as cursor:
                cursor.execute(create_db)
                print("db successfully created")
    except Exception as e:
        print(e)

# create_db(USERNAME, PASSWORD, HOSTNAME)

def connect_db(USERNAME, HOSTNAME, PASSWORD):
   try:
       connection = mysql.connector.connect(
           user = USERNAME,
           host = HOSTNAME,
           PASSWORD = PASSWORD,
           database = "event_management_sys"
       )
       print("Database is now connected.")
       return connection
   except Exception as error:
       return f"Error! Check if Database exists, addition info: {error}"

def create_tables():
    try:
        connection = connect_db(USERNAME, HOSTNAME, PASSWORD)
        cursor = connection.cursor()

        with open("./app/schema.sql", mode = "r", encoding="utf-8") as schema:
            db_schema = schema.read().split(";")
        for statement in db_schema:
            if statement.strip():
                cursor.execute(statement.strip(";"))
        connection.commit()
        connection.close()
        print("Tables successfully created.")
    except FileExistsError as e:
        return e
    except Exception as error:
        return error

create_tables()