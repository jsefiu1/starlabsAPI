import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import yaml
from fastapi import FastAPI

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "joni")
DB_NAME = os.getenv("DB_NAME", "fastapi")

with open("config.yaml") as file:
    config = yaml.safe_load(file)

db_settings = config["db"]
DB_HOST = db_settings.get("host", DB_HOST)
DB_PORT = db_settings.get("port", DB_PORT)
DB_USER = db_settings.get("user", DB_USER)
DB_PASSWORD = db_settings.get("password", DB_PASSWORD)
DB_NAME = db_settings.get("name", DB_NAME)

# Create the database URL
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db")
def test_db_connection():
    try:
        with engine.connect() as connection:
            connection.execute("SELECT 1")
        return {"message": "Database connection successful"}
    except Exception as e:
        return {"message": f"Error connecting to the database: {str(e)}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
