import uuid
import csv
from utilities import check_url_status_and_save
from models import URL, WebsiteInfo
from celery_base import app
import requests
from utilities import Session


# TODO:

# COMPLETED:
#models.py ve celery.py ve utilities.py 
#fastapi yazılacak
#celery ile taskları schedule edip tekrar çalıştırma?
#compose ile servis de çalıştırılacak --> dockerfile değişecek

#----------------------------------------------------API FUNCTIONS-------------------------------------------------------------

@app.task
def get_all_urls():
    session = Session()
    try:
        urls = session.query(URL).all()
        return [{"url": url.url, "is_active": url.is_active} for url in urls]
    finally:
        session.close()

#----------------------------------------------------DAILY FUNCTIONS-------------------------------------------------------------

@app.task
def check_url_status_daily():
    session = Session()
    try:
        urls = session.query(URL).all()
        for url in urls:
            is_active = check_url_status_and_save(url.url)
            url.is_active = is_active
            session.commit()
    finally:
        session.close()

#----------------------------------------------------USOM FUNCTIONS-------------------------------------------------------------

@app.task
def usom_check_time_interval():
    print("USOM 15 MIN CHECK")
    url = "https://www.usom.gov.tr/url-list.txt"
    try:
        response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
        response.raise_for_status()
        content = response.text
        urls = content.strip().split("\n")

        session = Session()
        try:
            
            website_info = session.query(WebsiteInfo).first()
            if not website_info:
                website_info = WebsiteInfo(
                    openphish_latest_url="", openphish_count=0,
                    usom_latest_url="", usom_count=0,
                    phishtank_latest_url="", phishtank_count=0,
                    phishstats_latest_url="", phishstats_count=0
                )
                session.add(website_info)
                session.commit()

            for url in urls:
                if url != website_info.usom_latest_url:
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    website_info.usom_count += 1
                    session.add(url_entry)
                else:
                    break
            website_info.usom_latest_url = urls[0]
            session.commit()
        finally:
            print(f"USOM finished. Total count: {website_info.usom_count}")
            session.close()

    except requests.exceptions.RequestException as e:
        print(f"USOM website is down or under maintenance: {e}")
        pass


#----------------------------------------------------PHISHTANK FUNCTIONS-------------------------------------------------------------

@app.task
def phishtank_check_time_interval():
    print("PHISHTANK 15 MIN CHECK")
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
            website_info = session.query(WebsiteInfo).first()
            if not website_info:
                website_info = WebsiteInfo(
                    openphish_latest_url="", openphish_count=0,
                    usom_latest_url="", usom_count=0,
                    phishtank_latest_url="", phishtank_count=0,
                    phishstats_latest_url="", phishstats_count=0
                )
                session.add(website_info)
                session.commit()

            for url in urls:
                if url != website_info.phishtank_latest_url:
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    website_info.phishtank_count += 1
                    session.add(url_entry)
                else:
                    break
            website_info.phishtank_latest_url = urls[0]
            session.commit()
        finally:
            print(f"Phishtank finished. Total count: {website_info.phishtank_count}")
            session.close()

    except requests.exceptions.RequestException as e:
        print(f"PhishTank website is down or under maintenance: {e}")
        pass



#----------------------------------------------------OPENPISH FUNCTIONS-------------------------------------------------------------

@app.task
def openphish_check_time_interval():
    print("OPENPHISH 15 MIN CHECK")
    url = "https://openphish.com/feed.txt"
    try:
        response = requests.get(url, headers={"User-Agent": "Your User-Agent"}, timeout=10)
        response.raise_for_status()
        content = response.text

        urls = content.strip().split("\n")

        session = Session()
        try:
            website_info = session.query(WebsiteInfo).first()
            if not website_info:
                website_info = WebsiteInfo(
                    openphish_latest_url="", openphish_count=0,
                    usom_latest_url="", usom_count=0,
                    phishtank_latest_url="", phishtank_count=0,
                    phishstats_latest_url="", phishstats_count=0
                )
                session.add(website_info)
                session.commit()

            for url in urls:
                if url != website_info.openphish_latest_url:
                    url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                    website_info.openphish_count += 1
                    session.add(url_entry)
                else:
                    break
            website_info.openphish_latest_url = urls[0]
            session.commit()
        finally:
            print(f"Openphish finished. Total count: {website_info.openphish_count}")
            session.close()
    except requests.exceptions.RequestException as e:
        print(f"Openphish website is down or under maintenance: {e}")
        pass

#----------------------------------------------------PHISHSTATS FUNCTIONS-------------------------------------------------------------

@app.task
def phishstats_check_time_interval():
    print("PHISHSTATS 15 MIN CHECK")
    url = "https://phishstats.info/phish_score.csv"
    try:
        response = requests.get(url, timeout=100000)
        response.raise_for_status()

        csv_text = response.text

        lines = csv_text.strip().split("\n")
        reader = csv.reader(lines[8:])  # header lines

        session = Session()
        try:
            website_info = session.query(WebsiteInfo).first()
            if not website_info:
                website_info = WebsiteInfo(
                    openphish_latest_url="", openphish_count=0,
                    usom_latest_url="", usom_count=0,
                    phishtank_latest_url="", phishtank_count=0,
                    phishstats_latest_url="", phishstats_count=0
                )
                session.add(website_info)
                session.commit()

            for row in reader:
                if len(row) >= 3:
                    url = row[2]
                    if url != website_info.phishstats_latest_url:
                        url_entry = URL(id=str(uuid.uuid4()), url=url, is_active=True)
                        website_info.phishstats_count += 1
                        session.add(url_entry)
                    else:
                        break
            website_info.phishstats_latest_url = reader.__next__()[2]
            session.commit()
        finally:
            print(f"Phishstats finished. Total count: {website_info.phishstats_count}")
            session.close()
    except requests.exceptions.RequestException as e:
        print(f"Phishstats website is down or under maintenance: {e}")
        pass
