from fastapi import FastAPI
from app.utils.database import test_db_connection
import uvicorn
from app.routers import telegrafi, gjirafa,kosovajob,douglas, home
from app.models import Base
from app.utils.database import engine
from app.tasks import (douglas as douglas_tasks)
from app.utils.tasks import site, scheduler

app = FastAPI()
   
    
    
@app.get("/test-db")
def test_database_connection():
    return test_db_connection()

app.include_router(home.router)

app.include_router(gjirafa.router)

app.include_router(telegrafi.router)

app.include_router(kosovajob.router)

app.include_router(douglas.router)


@app.on_event("startup")
async def startup():
    scheduler.start()

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
