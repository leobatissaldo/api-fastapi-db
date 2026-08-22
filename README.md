# Task List API with JWT and Database

A FastAPI based REST API with SQLite and JWT authentication database persistance using SQLAlchemy ORM.

## Features
- Create an account
- Token verification every 30 minutes
- Application is usable only if you are logged in(endpoints)
- Create tasks 
- Delete tasks 
- Mark tasks as done
- List all tasks with their status and id
- Check your last created tasks
- Password stored as a hash

## Technologies
- Python 3 
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy ORM
- SQLite
- JWT
- Passlib(Bcrypt)

## How to run

Run the script:

pip install -r requirements.txt

uvicorn main:app
