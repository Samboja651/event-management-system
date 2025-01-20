from flask import Flask, render_template, json, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from accounts import username, password, hostname
from db import connect_db
import mysql.connector

app = Flask(__name__)



@app.get("/")
def home_page():
    return "<h1>hello! HAKUNA MATATA.</h1>"
    # return render_template("")

@app.get("/events")
def get_all_events():

    def __get_events():
        conn = connect_db(username, hostname, password)
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
        conn = connect_db(username, hostname, password)
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
@app.route("/account/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    try:
        # Fetch email and password from form submission
        email = request.form.get("email")
        user_password = request.form.get("password")
        
        # Connect to the database
        conn = connect_db(username, hostname, password)
        cursor = conn.cursor()
        
        # Fetch user record by email
        query = "SELECT id, name, email, password FROM customers WHERE email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        
        # If user does not exist, return error
        if not user:
            return "Invalid email or password!"
        
        # Validate the password using check_password_hash
        stored_password_hash = user[3]  # Password is the 4th column in the returned record
        if not check_password_hash(stored_password_hash, user_password):
            return "Invalid email or password!"
        
        # If the password matches, login is successful. Redirect to home page.
        print(f"Welcome back, {user[1]}!")
        conn.close()
        return redirect(url_for("home_page"))
    
    except ValueError as e:
        return f"You have an error! {e}"
    except mysql.connector.Error as e:
        return f"Database error: {e}"