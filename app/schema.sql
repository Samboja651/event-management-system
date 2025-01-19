use event_management_sys;
CREATE TABLE IF NOT EXISTS EVENTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_name VARCHAR(255) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    event_image VARCHAR(255),
    event_fee DECIMAL(10, 2) NOT NULL,
    capacity INT NOT NULL DEFAULT 200, -- Maximum number of attendees
    categories VARCHAR(255) DEFAULT 'General' -- Category of the event
);
CREATE TABLE IF NOT EXISTS CUSTOMERS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS EVENT_MANAGERS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);
CREATE TABLE IF NOT EXISTS PAYMENTS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    payment_method VARCHAR(255) NOT NULL,
    event_id INT NOT NULL,
    customer_id INT NOT NULL,
    amount_paid DECIMAL(10, 2) NOT NULL,
    ratings INT CHECK (ratings BETWEEN 1 AND 5), -- Customer rating for the event
    FOREIGN KEY (event_id) REFERENCES EVENTS(id),
    FOREIGN KEY (customer_id) REFERENCES CUSTOMERS(id)
);
CREATE TABLE IF NOT EXISTS NOTIFICATIONS (
    id INT AUTO_INCREMENT PRIMARY KEY,
    event_manager_id INT NOT NULL,
    message TEXT NOT NULL,
    notification_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (event_manager_id) REFERENCES EVENT_MANAGERS(id)
);
-- Trigger to notify event manager of new payment
DELIMITER $$

CREATE TRIGGER notify_event_manager_after_payment
AFTER INSERT ON PAYMENTS
FOR EACH ROW
BEGIN
    DECLARE manager_id INT;

    -- Get the event manager for the event
    SELECT id INTO manager_id
    FROM EVENT_MANAGERS
    WHERE id = (SELECT id FROM EVENTS WHERE id = NEW.event_id);

    -- Insert a notification into the NOTIFICATIONS table
    INSERT INTO NOTIFICATIONS (event_manager_id, message)
    VALUES (
        manager_id,
        CONCAT('A new payment has been made for Event ID: ', NEW.event_id)
    );
END $$

DELIMITER ;
-- this trigger is not automatically executed from my code, haven't figured how, you can comy the trigger and execute directly on this database.