from flask import flash, Flask, render_template, json, request, redirect, url_for
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
        confirm_password =request.form.get("confirm_password")

        # Basic validation
        if not name or not email or not user_password or not confirm_password:
            flash("All fields are required.")
            return render_template('auth/signuo.html')
        
        if user_password != confirm_password:
            flash("Password do not match.")
            return render_template('auth/signup.html')
        
        if len(user_password) < 8:
            flash("Password must be at least 8 characters long.")
            return render_template('auth/signup.html')
        
        # hash the password
        hashed_password = generate_password_hash(user_password)

        # store user
        conn = connect_db(username, hostname, password)
        cursor = conn.cursor()
        store_user = "INSERT INTO customers(name, email, password)VALUES(%s, %s, %s)"
        cursor.execute(store_user, (name, email, hashed_password))
        conn.commit()
        conn.close()

        flash("Account successfully created")
        return redirect(url_for("home_page"))
    except mysql.connector.Error as e:
        flash(f"Database error: {e}")
        return render_template('auth/signup.html')
    pass

@app.route("/account/login", methods = ["GET", "POST"])
def login_user():
    if request.method == "GET":
        pass
        return render_template("auth/login.html")
    
    try:
        # Fetch emal and password from the submissin form
        email = request.form.get("email")
        user_password = request.form.get("password")

        # Basic validation
        if not email or not password:
            flash("Both email and password are required.")
            return render_template('auth/login.html')
        
        # Fetch the user record from the database
        conn = connect_db(username, hostname, password)
        cursor = conn.cursor()
        fetch_user = "SELECT email, paasword FROM customers WHERE email = %s"

        cursor.execute(fetch_user, (email,))
        user_record = cursor.fetchone()

        # Check if user exists
        if not user_record:
            flash("User does not exist.")
            return render_template('auth?login.html')
        
        # Validate password
        stored_email, stored_password = user_record
        if not check_password_hash(stored_password,user_password):
            flash("Incorrect password.")
            return render_template('auth/login.html')
        
        # Close database connection
        conn.close()

        # Redirect to home page if login is successful
        flash("Logged in successfully.")
        return redirect(url_for(home_page))
    except mysql.connector.Error as e:
        flash(f"Database error: {e}")
        return render_template('auth/login.html')
    pass