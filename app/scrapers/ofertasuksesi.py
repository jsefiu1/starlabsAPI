from bs4 import BeautifulSoup
import requests
from app.utils.database import session
from app.models.ofertasuksesi import Data
from sqlalchemy.orm.exc import NoResultFound
from datetime import date
from datetime import datetime, timedelta

def scrape(category: str, page: int):
    web_link = f"https://www.ofertasuksesi.com/kategorite/{category}/?page={page}"
    website = requests.get(url=web_link)
    soup = BeautifulSoup(website.content, "html.parser")
    parent_divs = soup.find_all("div", class_="col-sm-8")
    all_descriptions = soup.find_all("div", class_="col-sm-4")
    img_url = soup.find_all("div", class_="col-sm-4")
    new_offers = []
    
    for parent_div, description, image  in zip(parent_divs, all_descriptions, img_url):
        offer_title = parent_div.find("h4").text
        location = parent_div.find("span", class_="label-city").text.replace("ë", "e").replace("ç", "c")
        description = description.find("a").get("href")
        img = image.find("img").get("src")
        replace_location = location.replace(" ", "")
        date_scraped = datetime.now()

        existing_offer = session.query(Data).filter(Data.title == offer_title, Data.location == replace_location, Data.info == description, Data.image == img).all()
        if existing_offer:
            data = {
                "title": offer_title,
                "info": description,
                "location": replace_location,
                "image": img,
            }
            new_offers.append(data)
        else:
            data = {
                "title": offer_title,
                "info": description,
                "location": replace_location,
                "image": img,
            }
            new_offer = Data(title=offer_title, info=description, location=replace_location, image=img, date_scraped=date_scraped)
            session.add(new_offer)
            new_offers.append(data)

    session.commit()
    session.close()
    return new_offers
