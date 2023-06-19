import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy.sql import text
import yaml

__all__ = ["test_db_connection"]

load_dotenv()

DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "joni")
DB_NAME = os.getenv("POSTGRES_DB", "fastapi")


DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)


def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return True

    except Exception as e:
        print(f"Database connection error: {str(e)}")
        return False

        # http://localhost:8080/
