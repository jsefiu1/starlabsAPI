import requests
from app.utils.tasks import scheduler


@scheduler.scheduled_job("interval", hours=6)
def douglas_scrape():
    url_paths = ["brands",
                 "parfum/01",
                 "Make-up/03",
                 "gesicht/12",
                 "koerper/13",
                 "haare/14",
                 "apotheke-gesundheit/07",
                 "home-lifestyle/15",
                 "sale/05",
                 "nachhaltigkeit/59",
                 "sommer/86",
                 "pride/90",
                 "luxuswelt/29",
                 "neuheiten/09"
                 ]
    
    for url_path in url_paths:
        requests.get(
            url="http://localhost:8000/douglas/scrape",
            params={"url_path":url_path, "page_numbers":1},
        )