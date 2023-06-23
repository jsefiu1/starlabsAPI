from fastapi import FastAPI
from app.utils.database import test_db_connection
import uvicorn
from app.routers import gjirafa50


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/test-db")
def test_database_connection():
    return test_db_connection()


app.include_router(gjirafa50.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
