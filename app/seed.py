from db import connect_db
from accounts import username, password, hostname

# this dummy data for db
def seed_db():
    """populate db with dummy data."""
    conn = connect_db(username, hostname, password)
    cursor = conn.cursor()

    event_data = [
        ("Hactoberfest", "Come and Lets talk about security of systems", "2025-10-10", 500.0, "Tech"),
        ("Makosa in Yangu", "Enjoy a thrilling comedy, all made local.", "2025-12-10", 1000.0, "Entertaiment"),
        ("Lishe Bora", "Elimishwa jinsi ya kujikinga dhidi ya malaria.", "2025-11-10", 1000.0, "Health")
    ]
    try:
        cursor.executemany("INSERT INTO events (event_name, description, date, event_fee, categories)VALUES (%s, %s, %s, %s, %s)", event_data)
        conn.commit()
        conn.close()
        return "dummy data was successfully created."
    except Exception as e:
        return f"Error! {e}"

print(seed_db())