import requests
from app.utils.tasks import scheduler

@scheduler.scheduled_job("interval", hours=6)
def ofertasuksesi_scrape():
  url_paths = [
    "1-patundshmeri",
    "2-automjete",
    "3-rreth-punes",
    "4-pc-tv-etj",
    "5-celular",
    "6-shtepia-juaj",
    "7-bashkepunim",
    "8-sherbime",
    "9-bujqesi",
    "10-kafshe",
    "11-interesi-juaj",
    "12-te-ndryshme",
    ]
  
  for url_path in url_paths:
    requests.get("http://localhost:8000/ofertasuksesi/scrape",
                 params={"category": url_path, "page": 1})