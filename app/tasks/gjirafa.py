import requests
from fastapi_scheduler import SchedulerAdmin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from app.utils.database import DATABASE_URL

site = AdminSite(settings=Settings(database_url=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)

@scheduler.scheduled_job("interval", hours=6)
def gjirafa1():

    url_paths = [
        "/kozmetike",
        "/aksesore",
        "/veshje",
        "/shtepi",
        "/sport",
        "/teknologji",
        "femije",
        "librari",
        "/vegla-pune",
        "/auto",
        "/shendet",
        "/ushqime-pije",
    ]

    for url_path in url_paths:
        response = requests.get(
            url="http://localhost:8000/gjirafa/scrape",
            params={"url_path": url_path, "page_numbers": 1},
        )
