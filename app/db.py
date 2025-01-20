import sqlite3, click
from flask import current_app

DATABASE = "event_management_sys.db"

def get_db():
    db = sqlite3.connect(DATABASE)
    return db

def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql")as schema:
        db.executescript(schema.read().decode("utf-8"))

def delete_db():
    db = get_db()
    cursor = db.cursor()
    statement = "DROP DATABASE ?"
    cursor.execute(statement, DATABASE)
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