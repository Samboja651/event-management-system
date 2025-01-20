from flask import Flask, render_template, json, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from .db import get_db, init_app
import os
from .routes import auth, events

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        DATABASE = os.path.join(app.instance_path, 'event_management_sys.db')
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # ignore as folder exists
        pass

    @app.get("/")
    def home_page():
        return "<h1>hello! HAKUNA MATATA.</h1>"
        # return render_template("")

    init_app(app) # to initialize db run flask --app app init-db
    # register routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(events.bp)

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()