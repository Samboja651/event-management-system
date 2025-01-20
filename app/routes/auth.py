from flask import Flask, render_template, json, request, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db, init_app

bp = Blueprint('auth', __name__, url_prefix='/api')
# auth is the name of the blueprint
# __name__ is the location of the bp 

@bp.route("/account/signup", methods = ["GET", "POST"])
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
        db = get_db()
        cursor = db.cursor()
        store_user = "INSERT INTO customers(name, email, password)VALUES(?, ?, ?)"
        cursor.execute(store_user, (name, email, hashed_password))
        db.commit()
        db.close()

        print("Account successfully created")
        return redirect(url_for("home_page"))
    except ValueError as e:
        return f"You have an Error! {e}"
    except Exception as e:
        return f"You have an Error! {e}"

@bp.route("/account/login", methods=["GET", "POST"])
def login_user():
    if request.method == "GET":
        return render_template("auth/login.html")
    
    try:
        # Fetch email and password from form submission
        email = request.form.get("email")
        user_password = request.form.get("password")
        
        # Connect to the database
        db = get_db()
        cursor = db.cursor()
        
        # Fetch user record by email
        query = "SELECT id, name, email, password FROM customers WHERE email = ?"
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
        db.close()
        return redirect(url_for("home_page"))
    
    except ValueError as e:
        return f"You have an error! {e}"
    except Exception as e:
        return f"You have an Error! {e}"