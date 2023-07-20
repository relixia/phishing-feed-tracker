import uuid
import csv
from utilities import check_url_status_and_save, save_url
from models import URL
from celery_base import app
import requests
from utilities import Session


# TODO:
#postgres bağlantıları ve usom, phishtank, phishstats, openphish websitelerinin url linklerini env ye kaydet ordan kullan 
#fastapi yazılacak
#celery ile taskları schedule edip tekrar çalıştırma?
#dbde tekrar olup olmadığına bakılacak query 
#compose ile servis de çalıştırılacak --> dockerfile değişecek

# COMPLETED:
#models.py ve celery.py ve utilities.py 



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
    #print(usom_latest)

    session = Session()
    try:
        for url in urls:
            check_url_status_and_save(url)
    finally:
        session.close()

    print("usom finished")

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

    print("phishtank finished")
    #ben veri tabanıma şu zamanda kaydettim timestamp 



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
    print("openphish finished")


@app.task
def phishstats():
    print("Starting Phishstats...")
    url = "https://phishstats.info/phish_score.csv"
    response = requests.get(url, timeout=100000)
    response.raise_for_status()

    csv_text = response.text

    lines = csv_text.strip().split("\n")
    reader = csv.reader(lines[8:])  # header lines

    session = Session() #bu silinebilir
    try:
        for row in reader:
            if len(row) >= 3:
                url = row[2]
                check_url_status_and_save(url)
    finally:
        session.close()

    print("phishstats finished")