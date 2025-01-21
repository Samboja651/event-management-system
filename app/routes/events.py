from flask import Flask, render_template, json, request, redirect, url_for, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db, init_app

bp = Blueprint('events', __name__, url_prefix='/api')
# auth is the name of the blueprint
# __name__ is the location of the bp 

@bp.route("/events", methods=('GET', 'POST'))
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
        return "<h1>loaded events</h1>"
