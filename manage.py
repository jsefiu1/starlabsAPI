from fastapi import FastAPI
import uvicorn
from app.routers import telegrafi, gjirafa, kosovajob, home, ofertasuksesi
from app.models import Base
from app.utils.database import engine
from app.tasks import (
    telegrafi as telegrafi_tasks,
    gjirafa as gjirafa_tasks,
    kosovajob as kosovajob_tasks,
)
from app.utils.tasks import site, scheduler

app = FastAPI()

site.mount_app(app)


@app.on_event("startup")
async def startup():
    scheduler.start()


app.include_router(home.router)
app.include_router(gjirafa.router)
app.include_router(telegrafi.router)
app.include_router(kosovajob.router)
app.include_router(ofertasuksesi.router)

Base.metadata.create_all(engine)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
