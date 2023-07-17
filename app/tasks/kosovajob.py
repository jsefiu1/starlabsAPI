import requests
from app.utils.tasks import scheduler


@scheduler.scheduled_job("interval", hours=6)
def kosovajob_scrape():
    requests.get(
        url="http://localhost:8000/kosovajobs/scrape",
        params={"url_path": "https://kosovajob.com/"},
    )

