from fastapi import FastAPI
from database import test_db_connection

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/test-db")
def test_database_connection():
    if test_db_connection():
        return {"message": "Database connection successful"}
    else:
        return {"message": "Error connecting to the database"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)