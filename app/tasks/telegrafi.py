import requests
from fastapi_scheduler import SchedulerAdmin
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from app.utils.database import DATABASE_URL

site = AdminSite(settings=Settings(database_url=DATABASE_URL))
scheduler = SchedulerAdmin.bind(site)


@scheduler.scheduled_job("interval", hours=6)
def telegrafi1():
    url_paths = [
        "/lajme/",
        "/sport/",
        "/fun/",
        "/teknologji/",
        "/auto/",
        "/kuzhina/",
        "/shendetesi/",
        "/stili/",
        "/femra/",
        "/kultura/",
        "/magazina/",
        "/ekonomi/",
        "/bote/",
    ]
    for url_path in url_paths:
        response = requests.get(
            url="http://localhost:8000/telegrafi/scrape",
            params={"url_path": url_path, "page_numbers": 1},
        )
