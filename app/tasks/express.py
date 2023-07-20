import requests
from fastapi_scheduler import SchedulerAdmin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from app.utils.database import DATABASE_URL

site = AdminSite(settings=Settings(database_url=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)

@scheduler.scheduled_job("interval", hours=6)
def Express_scrape():
    url_paths = [
        "lajme",
        "sport",
        "op-ed",
        "roze",
        "shneta",
    ]
    for url_path in url_paths:
        requests.get(
            url="http://localhost:8000/gazetaexpress/scrape",
            params={"url_path": url_path, "limit": 10, "offset": 0},
        )

