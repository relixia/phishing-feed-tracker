import requests
from celery import Celery
from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
import uuid
import csv

Base = declarative_base()

class URL(Base):
    __tablename__ = "urls"

    id = Column(String, primary_key=True)
    url = Column(String)
    is_active = Column(Boolean, default=True)


engine = create_engine("postgresql://r3lixia:secret@localhost/phishing-feed-tracker-db")
Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)

app = Celery("tasks", broker="redis://localhost:6379/0",backend="redis://localhost:6379/0")


def check_url_status_and_save(url):
    session = Session()
    try:
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"http://{url}"

        response = requests.head(url, timeout=5)
        if response.status_code == 200:
            active_url = URL(id=str(uuid.uuid4()), url=url, is_active=True)
            save_url(session, active_url)
        else:
            inactive_url = URL(id=str(uuid.uuid4()), url=url, is_active=False)
            save_url(session, inactive_url)
    except requests.exceptions.Timeout:
        print(f"{url} is inactive (Timeout)")
        inactive_url = URL(id=str(uuid.uuid4()), url=url, is_active=False)
        save_url(session, inactive_url)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while checking {url}: {str(e)}")
        inactive_url = URL(id=str(uuid.uuid4()), url=url, is_active=False)
        save_url(session, inactive_url)
    session.close()


def save_url(session, url):
    session.add(url)
    session.commit()


#GLOBAL VARIABLE LATEST URL FOR USOM
usom_latest = ""

@app.task
def usom():
    print("Starting USOM...")
    url = "https://www.usom.gov.tr/url-list.txt"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
    response.raise_for_status()

    content = response.text

    urls = content.strip().split("\n")
    usom_latest = urls[0]
    print(usom_latest)

    session = Session()
    try:
        for url in urls:
            check_url_status_and_save(url)
    finally:
        session.close()

'''

@app.task
def usom_check_five_min():
    print("USOM 5 MIN CHECK")
    url = "https://www.usom.gov.tr/url-list.txt"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
    response.raise_for_status()
    content = response.text
    urls = content.strip().split("\n")

    session = Session()
    try:
        for url in urls:
            if(url != usom_latest):
                check_url_status_and_save(url)
            else:
                break
    finally:
        usom_latest = urls[0]
        session.close()

'''

@app.task
def phishtank():
    print("Starting Phishtank...")
    url = "http://data.phishtank.com/data/online-valid.csv"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=1000000)
    response.raise_for_status()

    content = response.text

    lines = content.strip().split("\n")
    reader = csv.reader(lines)
    next(reader) 

    urls = [row[1] for row in reader]
    print("Size of urls list:", len(urls))

    session = Session()
    try:
        # SINCE PHISHTANK DATA ONLY INCLUDES THE VALID AND ONLINE URLS, THERE IS NO NEED TO CALL check_url_status(url) FUNCTION.
        for url in urls:
            url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
            session.add(url_entry)
            session.commit()
    finally:
        session.close()

    print("IT IS DONEEEEEEEEEEEEEEEEEEEEEEEE")



@app.task
def openphish():
    print("Starting Openphish...")
    url = "https://openphish.com/feed.txt"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
    response.raise_for_status()

    content = response.text

    urls = content.strip().split("\n")

    session = Session()
    try:
        for url in urls:
            check_url_status_and_save(url)
    finally:
        session.close()
    print("IT IS DONEEEEEEEEEEEEEEEEEEEEEEEE")


@app.task
def phishstats():
    print("Starting Phishstats...")
    url = "https://phishstats.info/phish_score.csv"
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    csv_text = response.text

    lines = csv_text.strip().split("\n")
    reader = csv.reader(lines[8:])  # header lines

    session = Session()
    try:
        for row in reader:
            if len(row) >= 3:
                url = row[2]
                check_url_status_and_save(url)
    finally:
        session.close()

    print("IT IS DONEEEEEEEEEEEEEEEEEEEEEEEE")