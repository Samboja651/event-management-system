# event-management-system-backend

## Setup
Create virtual environmen run `python3 -m venv .venv` \
To activate virtual environment: \
On windows run `.\.venv\Scripts\activate ` \
On Linux>ubuntu - venv is automatically activated. Alternatively run `.\.venv\bin\activate` .

## Install packages
Run this command `pip install -r .\requirement.txt`

## Configure the database
Assuming you have mysql server installed on your machine. \
To connect to mysql server locally we need:
- mysql username, by default mysql uses `root`. change otherwise.
- mysql login password.
- mysql hostname default it is `localhost` .
run this command `python .\config.py`\
open the file accounts.py and write your mysql logins.\
**Note the accounts.py file is ignored (not pushed to remote repo, so no worry your logins belong to you.)**
- Now run command `python .\app\db.py`
- open your mysql check the new db created `event_management_sys`.

## populate db with dummy data
> run this command `python .\app\seed.py `

## API END POINTS
> `/` - get the landing/home page. \
> `/events` - get all events data in database. \
> `/account/signup` - create a new account. **Note, uses post to specifically get the name, email, and password. Its expected you have the same naming of attributes in signup forms. eg `<input type="email" name="email"`**
> `/account/login` - user login
### `/account/login`
**Method:** POST  
**Description:** Allows a user to log in by submitting their email and password.  
**Request Parameters:**
- `email` (string): The user's email address.
- `password` (string): The user's password.

**Response:**
- On success: Redirects to the home page with a welcome message.
- On failure: Returns an error message "Invalid email or password!".

**Example Request:**
```http
POST /account/login
Content-Type: application/x-www-form-urlencoded

email=user@example.com&password=securepassword
```

**Example Response:**
- Success: Redirects to `/home_page`.
- Failure: Returns "Invalid email or password!".

**Notes:**
- Passwords are hashed and stored securely in the database.
- Uses the `check_password_hash` function to validate the password.
- If an error occurs, appropriate error messages are returned.

## running the app
- first run `cd .\app\`
- finally run `flask run --debug`

**Note: the current templates are dummy, for testing, replace html with main templates.**

TODO DIRECTORY STRUCTURE
