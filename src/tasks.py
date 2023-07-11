from celery import Celery
from playwright.sync_api import sync_playwright
from sqlalchemy import create_engine, Column, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

# Configure the SQLAlchemy engine and session
engine = create_engine('postgresql://r3lixia:secret@localhost/phishing-feed-tracker-db')
Session = sessionmaker(bind=engine)

Base = declarative_base()

# Define the WebsiteData model
class WebsiteData(Base):
    __tablename__ = 'website_data'

    id = Column(String, primary_key=True)
    website = Column(String)
    id_in_website = Column(String)
    phishing_url = Column(String)
    submitted_by = Column(String)
    targeted_brand = Column(String)
    time_stamp = Column(String)

@app.task
def crawl_website_1():

    print("Starting crawl_website_1 task...")

    # Launch the Playwright browser instance
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)

        # Create a new browser context
        context = browser.new_context()

        # Create a new page within the context
        page = context.new_page()

        # Navigate to the website
        page.goto('https://www.phishtank.com')

        # Get all the phish_detail links
        links = page.query_selector_all('a[href^="phish_detail.php?phish_id="]')

        # Extract and store the data
        for link in links:
            href = link.get_attribute('href')
            url = f'https://www.phishtank.com/{href}'
            
            # visit the individual website
            page.goto(url)

            # scraping/crawling actions:
            timestamp = page.inner_text('span.small').split(' by\n')[0].strip()
            submitted_by = page.query_selector('span.small b a').inner_text()
            id_in_website = page.inner_text('h2').split('#')[-1].split()[0]
            phishing_url = page.query_selector('span[style="word-wrap:break-word;"] b').inner_text()
            targeted_brand = None  # PhishTank doesn't provide targeted brand info

            # Save the data to the database
            session = Session()
            data = WebsiteData(
                website='PhishTank',
                id_in_website=id_in_website,
                phishing_url=phishing_url,
                submitted_by=submitted_by,
                targeted_brand=targeted_brand,
                time_stamp=timestamp
            )
            session.add(data)
            session.commit()
            session.close()

        # Close the browser context and browser
        context.close()
        browser.close()
        print("Crawling of Website 1 completed successfully.")

@app.task
def crawl_website_2():
    print("hey")
    # CODE CODE CODE

@app.task
def crawl_website_3():
    print("hey")
    # MORE CODE CODE CODE


if __name__ == '__main__':
    print("başla")
    #browser = playwright.chromium.launch(headless=False)
    result = crawl_website_1.delay()
    print("task started")
    result.get()
    print("bit")
    #crawl_website_2.delay()
    #crawl_website_3.delay()