import requests
from app.utils.tasks import scheduler


@scheduler.scheduled_job("interval", seconds=10)
def kosovajob_scrape():
    requests.get(
        url="http://localhost:8000/kosovajobs/scrape",
        params={"url_path": "https://kosovajob.com/"},
    )
