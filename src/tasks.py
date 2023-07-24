import uuid
import csv
from utilities import check_url_status_and_save, save_url
from models import URL
from celery_base import app
import requests
from utilities import Session


# TODO:
#compose ile servis de çalıştırılacak --> dockerfile değişecek

# COMPLETED:
#models.py ve celery.py ve utilities.py 
#fastapi yazılacak
#celery ile taskları schedule edip tekrar çalıştırma?



@app.task
def get_all_urls():
    session = Session()
    try:
        urls = session.query(URL).all()
        return [{"url": url.url, "is_active": url.is_active} for url in urls]
    finally:
        session.close()


#----------------------------------------------------USOM FUNCTIONS-------------------------------------------------------------

#GLOBAL VARIABLE LATEST URL FOR USOM
usom_latest = ""
usom_total = 0

'''
@app.task
def usom():
    print("Starting USOM...")
    url = "https://www.usom.gov.tr/url-list.txt"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
    response.raise_for_status()

    content = response.text

    urls = content.strip().split("\n")
    global usom_latest
    usom_latest = urls[0]
    print(usom_latest)

    session = Session()
    try:
        for url in urls:
            check_url_status_and_save(url)
    finally:
        session.close()

    print("usom finished")
'''


@app.task
def usom_check_time_interval():
    global usom_latest
    global usom_total
    print("USOM 30 MIN CHECK")
    url = "https://www.usom.gov.tr/url-list.txt"
    try:
        response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
        response.raise_for_status()
        content = response.text
        urls = content.strip().split("\n")

        session = Session()
        try:
            for url in urls:
                if(url != usom_latest):
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    session.add(url_entry)
                    session.commit()
                    usom_total += 1
                else:
                    break
        finally:
            usom_latest = urls[0]
            print(f"USOM finished. Total count: {usom_total}")
            session.close()
    except requests.exceptions.RequestException as e:
        print(f"USOM website is down or under maintenance: {e}")
        pass


#----------------------------------------------------PHISHTANK FUNCTIONS-------------------------------------------------------------

#GLOBAL VARIABLE LATEST URL FOR PHISHTANK
phishtank_latest = ""
phishtank_total = 0

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
    global phishtank_latest 
    phishtank_latest = urls[0]

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
'''

@app.task
def phishtank_check_time_interval():
    global phishtank_latest
    global phishtank_total
    print("PHISHTANK 30 MIN CHECK")
    url = "http://data.phishtank.com/data/online-valid.csv"
    try:
        response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=1000000)
        response.raise_for_status()
        content = response.text

        lines = content.strip().split("\n")
        reader = csv.reader(lines)
        next(reader)

        urls = [row[1] for row in reader]

        session = Session()
        try:
            for url in urls:
                if (url != phishtank_latest):
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    phishtank_total += 1
                    session.add(url_entry)
                    session.commit()
                else:
                    break
        finally:
            phishtank_latest = urls[0]
            session.close()

        print(f"Phishtank finished. Total count: {phishtank_total}")
    except requests.exceptions.RequestException as e:
        print(f"PhishTank website is down or under maintenance: {e}")
        pass



#----------------------------------------------------OPENPISH FUNCTIONS-------------------------------------------------------------

#GLOBAL VARIABLE LATEST URL FOR OPENPHISH
openphish_latest = ""
openphish_total = 0

'''
@app.task
def openphish():
    print("Starting Openphish...")
    url = "https://openphish.com/feed.txt"
    response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
    response.raise_for_status()

    content = response.text

    urls = content.strip().split("\n")
    global openphish_latest
    openphish_latest = urls[0]

    session = Session()
    try:
        for url in urls:
            check_url_status_and_save(url)
    finally:
        session.close()
    print("openphish finished")
'''

@app.task
def openphish_check_time_interval():
    global openphish_latest
    global openphish_total
    print("OPENPHISH 30 MIN CHECK")
    url = "https://openphish.com/feed.txt"
    try:
        response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
        response.raise_for_status()
        content = response.text

        urls = content.strip().split("\n")

        session = Session()
        try:
            for url in urls:
                if (url != openphish_latest):
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    openphish_total += 1
                    session.add(url_entry)
                    session.commit()
                else:
                    break
        finally:
            openphish_latest = urls[0]
            session.close()

        print(f"Openphish finished. Total count: {openphish_total}")
    except requests.exceptions.RequestException as e:
        print(f"Openphish website is down or under maintenance: {e}")
        pass

#----------------------------------------------------PHISHSTATS FUNCTIONS-------------------------------------------------------------

#GLOBAL VARIABLE LATEST URL FOR PHISHSTATS
phishstats_latest = ""
phishstats_total = 0

'''
@app.task
def phishstats():
    print("Starting Phishstats...")
    url = "https://phishstats.info/phish_score.csv"
    response = requests.get(url, timeout=100000)
    response.raise_for_status()

    csv_text = response.text

    lines = csv_text.strip().split("\n")
    reader = csv.reader(lines[8:])  # header lines
    global phishstats_latest
    phishstats_latest = reader.__next__()[2]
    print(phishstats_latest)

    session = Session()
    try:
        for row in reader:
            if len(row) >= 3:
                url = row[2]
                check_url_status_and_save(url)
    finally:
        session.close()

    print("phishstats finished")

'''

@app.task
def phishstats_check_time_interval():
    global phishstats_latest
    global phishstats_total
    print("PHISHSTATS 5 MIN CHECK")
    url = "https://phishstats.info/phish_score.csv"
    try:
        response = requests.get(url, timeout=100000)
        response.raise_for_status()

        csv_text = response.text

        lines = csv_text.strip().split("\n")
        reader = csv.reader(lines[8:])  # header lines

        session = Session()
        try:
            for row in reader:
                if len(row) >= 3:
                    url = row[2]
                    if (url != phishstats_latest):
                        check_url_status_and_save(url)
                        phishstats_total += 1
                    else:
                        break
        finally:
            session.close()

        print(f"Phishstats finished. Total count: {phishstats_total}")
    except requests.exceptions.RequestException as e:
        print(f"Phishstats website is down or under maintenance: {e}")
        pass
