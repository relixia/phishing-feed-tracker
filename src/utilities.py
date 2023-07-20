import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from models import URL
import uuid


Session = sessionmaker(bind=create_engine("postgresql://r3lixia:secret@localhost/phishing-feed-tracker-db"))

def check_url_status_and_save(url):
    session = Session()
    try:
        try:
            url_entry = session.query(URL).filter(URL.url == url).one()
            url_entry.is_active = True
        except NoResultFound:
            url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
            session.add(url_entry)
        session.commit()
    finally:
        session.close()

def save_url(url):
    session = Session()
    try:
        url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
        session.add(url_entry)
        session.commit()
    finally:
        session.close()
