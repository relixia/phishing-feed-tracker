import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from models import URL
import uuid


Session = sessionmaker(bind=create_engine("postgresql://r3lixia:secret@localhost/phishing-feed-tracker-db"))

def check_url_status_and_save(url):
    try:
        response = requests.get(url, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False