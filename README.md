# Notes API - Flask Auth Backend

A secure REST API for a personal notes app with session-based authentication.

---

## What It Does

- Users can sign up, log in, and log out
- Each user has their own notes fully private
- Full CRUD on notes (create, read, update, delete)
- Notes are paginated so you're not loading everything at once
- Unauthorized users get blocked with the right error codes

---


## Getting Started

Make sure you have Python 3.8+ and Pipenv installed, then:

```bash
# Install dependencies
pipenv install

# Activate the virtual environment
pipenv shell

# Set up the database
flask db upgrade

# Seed some sample data
python seed.py

# Start the server
flask run
```

The API will be running at `http://127.0.0.1:5000`

---


## Running

```bash
flask run
```
## Project Structure
productivity-app/
├── app.py          # Entry point, route registration
├── config.py       # App config, db and bcrypt setup
├── models.py       # User and Note models
├── seed.py         # Sample data for testing
├── resources/
│   ├── auth.py     # Signup, login, logout, me
│   └── notes.py    # Notes CRUD
└── README.md

##  Auth Endpoints
These handle registration and login. No token needed just hit signup first.

| Method | Route | What it does |
|--------|-------|-------------|
| POST | `/signup` | Create a new account |
| POST | `/login` | Log in to an existing account |
| DELETE | `/logout` | Log out of current session |
| GET | `/me` | Check who is currently logged in |

**Example signup request:**
```json
POST /signup
{
  "username": "ethan",
  "password": "yourpassword"
}
```

---

## Notes Endpoints

All of these require you to be logged in. If you're not, you'll get a `401`. If you try to touch someone else's note, you'll get a `403`.

| Method | Route | What it does |
|--------|-------|-------------|
| GET | `/notes?page=1` | Get your notes (5 per page) |
| POST | `/notes` | Create a new note |
| PATCH | `/notes/<id>` | Update one of your notes |
| DELETE | `/notes/<id>` | Delete one of your notes |

**Example create note request:**
```json
POST /notes
{
  "title": "Shopping list",
  "content": "Milk, eggs, bread"
}
```

---

## Notes

- Passwords are hashed with Bcrypt never stored in plain text
- Sessions are used to keep users logged in
- Every note is tied to the user who created it no crossover