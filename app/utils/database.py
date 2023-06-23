import os
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
if POSTGRES_PASSWORD is None:
    print("You should provide a db-password in the .env file")

POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME", "fastapi")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB_NAME}"


engine = create_engine(DATABASE_URL)

session = sessionmaker(bind=engine)()


def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {
            "message": "Database connection successful",
            "database_url": DATABASE_URL,
        }
    except Exception as e:
        return {
            "message": f"Error connecting to the database: {str(e)}",
            "database_url": DATABASE_URL,
        }
