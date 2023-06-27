from fastapi import FastAPI
from app.utils.database import test_db_connection
from app.routers import routers
from app.models import Base
from app.utils.database import engine

app = FastAPI()

@app.get("/test-db")
def test_database_connection():
    return test_db_connection()

app.include_router(routers.router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
