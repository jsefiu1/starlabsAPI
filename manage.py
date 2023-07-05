from fastapi import FastAPI
from app.utils.database import test_db_connection
import uvicorn
from app.routers import telegrafi, gjirafa,kosovajob,home
from app.models import Base
from app.utils.database import engine

app = FastAPI()


@app.get("/test-db")
def test_database_connection():
    return test_db_connection()

app.include_router(home.router)

app.include_router(gjirafa.router)

app.include_router(telegrafi.router)

app.include_router(kosovajob.router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
