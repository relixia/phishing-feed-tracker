import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm.exc import NoResultFound
from models import URL, Base

database_uri = 'postgresql://r3lixia:secret@phishing-feed-tracker-db:5432/phishing-feed-tracker-db'
engine = create_engine(database_uri)
Base.metadata.create_all(engine)


Session = sessionmaker(bind=create_engine("postgresql://r3lixia:secret@lphishing-feed-tracker-db:5432/phishing-feed-tracker-db"))

def check_url_status_and_save(url):
    try:
        response = requests.get(url, timeout=10)
        #o url'ye gidildikten sonra farklı library ile ile ss alınıp dbye koyulabilir
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False