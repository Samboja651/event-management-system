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

    @app.route("/", methods=('GET', 'POST'))
    def get_all_events():
        if request.method == "GET":
            def __get_events():
                db = get_db()
                cursor = db.cursor()
                get_events = "SELECT event_name, description, date, event_image, event_fee, categories FROM events"
                cursor.execute(get_events)
                records = cursor.fetchall()
                db.close()
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

    init_app(app) # to initialize db run flask --app app init-db
    # register routes
    app.register_blueprint(auth.bp)
    app.register_blueprint(events.bp)

    return app

app = create_app()

if __name__ == "__main__":
    app = create_app()