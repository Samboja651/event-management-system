import sqlite3, click
from flask import current_app


def get_db():
    db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types = sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row #tells the connection to return rows that behave like dicts. it allows accessing the columns by names
    return db

def seed_db():
    """populate db with dummy data."""
    db = get_db()
    cursor = db.cursor()

    event_data = [
        ("Hactoberfest", "Come and Lets talk about security of systems", "2025-10-10", 500.0, "Tech"),
        ("Makosa in Yangu", "Enjoy a thrilling comedy, all made local.", "2025-12-10", 1000.0, "Entertaiment"),
        ("Lishe Bora", "Elimishwa jinsi ya kujikinga dhidi ya malaria.", "2025-11-10", 1000.0, "Health")
    ]
    cursor.executemany("INSERT INTO events (event_name, description, date, event_fee, categories)VALUES (?, ?, ?, ?, ?)", event_data)
    db.commit()
    db.close()

    
def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql")as schema:
        db.executescript(schema.read().decode("utf-8"))
    seed_db() # fist time server runs, populate db with dummy data
    db.close()


def delete_db():
    db = get_db()
    cursor = db.cursor()
    statement = "DROP DATABASE ?"
    cursor.execute(statement, current_app.config["DATABASE"])
    db.commit() # not sure this line is relevant
    db.close()

@click.command("init-db")
def init_db_command():
    """create new tables if the don't exists"""
    init_db()
    click.echo("Initialized the database.")

@click.command("delete-db")
def delete_db_command():
    """delete database"""
    click.echo("Database was deleted.")

def init_app(app):
    app.cli.add_command(init_db_command)
    app.cli.add_command(delete_db_command)