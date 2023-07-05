from fastapi import FastAPI
from app.utils.database import test_db_connection, engine, DATABASE_URL
from app.routers import telegrafi, gjirafa, kosovajob, home
from app.models import Base
import uvicorn
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from app.tasks.gjirafa import gjirafa1



app = FastAPI()

site = AdminSite(settings=Settings(database_url=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)
site.mount_app(app)

@app.get("/test-db")
def test_database_connection():
    return test_db_connection()

app.include_router(home.router)

@app.on_event("startup")
async def startup():
    scheduler.start()

app.include_router(gjirafa.router)

app.include_router(telegrafi.router)

app.include_router(kosovajob.router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
