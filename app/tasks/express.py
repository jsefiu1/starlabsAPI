import requests
from fastapi_scheduler import SchedulerAdmin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from app.utils.database import DATABASE_URL

site = AdminSite(settings=Settings(database_url=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)

@scheduler.scheduled_job("interval", hours=6)
def Express_scrape():
    requests.get(
        url="http://localhost:8000/gazetaexpress/scrape",
        params={"url_path": "lajme", "limit": 20, "offset": 0},
    )

