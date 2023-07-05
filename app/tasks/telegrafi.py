import requests
from app.utils.tasks import scheduler


@scheduler.scheduled_job("interval", seconds=10)
def telegrafi_scrape():
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
        requests.get(
            url="http://localhost:8000/telegrafi/scrape",
            params={"url_path": url_path, "page_numbers": 1},
        )
