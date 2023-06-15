<<<<<<< HEAD
from fastapi import FastAPI
from database import test_db_connection
=======
"""from fastapi import FastAPI
>>>>>>> 5995cd3b613ab6fc36bb83a6a5924a520151199d

app = FastAPI()

@app.get("/")
def read_root():
<<<<<<< HEAD
    return {"Hello": "World"}

@app.get("/test-db")
def test_database_connection():
    if test_db_connection():
        return {"message": "Database connection successful"}
    else:
        return {"message": "Error connecting to the database"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
=======
    return {"Hello": "World"}"""

import psycopg2
from config import config


def connect():
    connection = None
    try:
        params = config()
        print("Connecting to the postgreSQL database ...")
        connection = psycopg2.connect(**params)

        # create a cursor
        crsr = connection.cursor()
        print("PostgreSQL database version: ")
        crsr.execute("SELECT version()")
        db_version = crsr.fetchone()
        print(db_version)
        crsr.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connection is not None:
            connection.close()
            print("Database connection terminated.")


if __name__ == "__main__":
    connect()
>>>>>>> 5995cd3b613ab6fc36bb83a6a5924a520151199d
