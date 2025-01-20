CREATE TABLE IF NOT EXISTS EVENTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name VARCHAR(50) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    event_image BLOB NULL,
    event_fee DECIMAL(10, 2) NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 200, -- Maximum number of attendees
    categories VARCHAR(50) DEFAULT 'General' -- Category of the event
);

CREATE TABLE IF NOT EXISTS CUSTOMERS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(50) NOT NULL,
    role VARCHAR(50) NOT NULL
);

CREATE TABLE IF NOT EXISTS PAYMENTS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    payment_method VARCHAR(50) NOT NULL,
    event_id INTEGER NOT NULL,
    customer_id INTEGER NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    ratings INTEGER CHECK (ratings BETWEEN 1 AND 5), -- Customer rating for the event
    FOREIGN KEY (event_id) REFERENCES EVENTS(id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(id)
);

CREATE TABLE IF NOT EXISTS NOTIFICATIONS (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_manager_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_manager_id) REFERENCES EVENT_MANAGERS(id)
);

-- Trigger to notify event manager of new payment
CREATE TRIGGER notify_event_manager_after_payment
AFTER INSERT ON PAYMENTS
FOR EACH ROW
BEGIN
    INSERT INTO NOTIFICATIONS (event_manager_id, message)
    VALUES (
        (SELECT id FROM EVENT_MANAGERS WHERE id = (SELECT id FROM EVENTS WHERE id = NEW.event_id)),
        'A new payment has been made for Event ID: ' || NEW.event_id
    );
END;
