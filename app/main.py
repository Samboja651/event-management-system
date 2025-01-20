from flask import Flask, render_template, json, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from db import connect_db
import mysql.connector
import os

app = Flask(__name__)
app.config["MYSQL_DATABASE"] = os.getenv("MYSQL_DATABASE")
app.config["MYSQLUSER"] = os.getenv("MYSQLUSER")
app.config["MYSQLPASSWORD"] = os.getenv("MYSQL_PASSWORD")
app.config["MYSQLHOST"] = os.getenv("MYSQLHOST")
app.config["ENV"] = "PRODUCTION"
app.config["DEBUG"] = "FALSE"

# now env variables to local variables
DATABASE = os.getenv("MYSQL_DATABASE")
USERNAME = os.getenv("MYSQLUSER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOSTNAME = os.getenv("MYSQLHOST")


@app.get("/")
def home_page():
    return "<h1>hello! HAKUNA MATATA.</h1>"
    # return render_template("")

@app.get("/events")
def get_all_events():

    def __get_events():
        conn = connect_db(USERNAME, HOSTNAME, PASSWORD)
        cursor = conn.cursor()
        get_events = "SELECT event_name, description, date, event_image, event_fee, categories FROM events"
        cursor.execute(get_events)
        records = cursor.fetchall()
        conn.close()
        return records
    
    events = __get_events()
    keys = ["event_name", "description", "date", "event_image", "event_fee", "categories"]
    event_list = [dict(zip(keys, event)) for event in events]
    """
    how above lines works.
    the keys are selected columns inside events table.
    events is an object returned by fetching records inside events table.
    events object has this data structure [(), (), ()]
    we loop throught the events to get each event in form ('', '', '')
    the len of keys and event match.
    zip(keys, event) combines each item in each key and event item respectively. we get (key, event_item)
    dict(zip) converts the zip into dictionary.
    then finally we append the dict into the list.
    """
    event_list = json.dumps(event_list, indent = 4) # convert to json. api format.
    return event_list

@app.route("/account/signup", methods = ["GET", "POST"])
def create_account():
    if request.method == "GET":
        pass
        return render_template("/auth/signup.html")
    try:
        name = request.form.get("name")
        email = request.form.get("email")
        user_password = request.form["password"]
        
        # hash the password
        hashed_password = generate_password_hash(user_password)
        # store user
        conn = connect_db(USERNAME, HOSTNAME, PASSWORD)
        cursor = conn.cursor()
        store_user = "INSERT INTO customers(name, email, password)VALUES(%s, %s, %s)"
        cursor.execute(store_user, (name, email, hashed_password))
        conn.commit()
        conn.close()

        print("Account successfully created")
        return redirect(url_for("home_page"))
    except ValueError as e:
        return f"You have an Error! {e}"
    except mysql.connector.Error as e:
        return f"You have an Error! {e}"
    pass

@app.route("/account/login", methods = ["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("auth/login.html")
    # TODO: FETCH email and password from form submission

    # TODO: FETCH the user record from the database. Validate user exists

    # TODO: use the module check_password_hash() to validate password

    # TODO: finally redirect user to home page.
    pass