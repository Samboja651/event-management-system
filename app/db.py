import mysql.connector
from accounts import username, password, hostname


def create_db(username: str, password: str, host: str):
    try:
        with mysql.connector.connect(
            user = username,
            host = host,
            password = password
        ) as connection:
            create_db = "CREATE DATABASE event_management_sys"
            with connection.cursor() as cursor:
                cursor.execute(create_db)
                print("db successfully created")
    except Exception as e:
        print(e)

# create_db(username, password, hostname)

def connect_db(username, hostname, password):
   try:
       connection = mysql.connector.connect(
           user = username,
           host = hostname,
           password = password,
           database = "event_management_sys"
       )
       print("Database is now connected.")
       return connection
   except Exception as error:
       return f"Error! Check if Database exists, addition info: {error}"

def create_tables():
    try:
        connection = connect_db(username, hostname, password)
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