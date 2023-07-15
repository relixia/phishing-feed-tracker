# phishing-feed-tracker
This is a python service that tracks 4 phishing feed websites of:
https://www.usom.gov.tr/adres
https://www.phishtank.com/index.php
https://openphish.com/index.html
https://phishstats.info/#

The service crawl every phishing url via Celery and Redis, and checks the status of the url by assigning unique ids for each of them. Then, the data is saved in PostgreSQL database from Docker Compose. The saving process is completed by SQLAlchemy. Poetry is used for dependency management and packaging.

Here is a screenshot of service's Celery in the working state:
<img width="1079" alt="Ekran Resmi 2023-07-15 23 01 33" src="https://github.com/relixia/phishing-feed-tracker/assets/77904399/1ec0f966-5841-4743-a706-40505864343f">

Here is a screenshot of database:
<img width="1470" alt="Ekran Resmi 2023-07-15 22 53 53" src="https://github.com/relixia/phishing-feed-tracker/assets/77904399/92b6a03c-dfb1-447c-bda9-e3f9c24f1b87">

The service is dockerized and ready to use.

PS: After you run the program and want to stop Celery, use the following command:
kill -9 $(ps aux | grep celery | grep -v grep | awk '{print $2}' | tr '\n' ' ') > /dev/null 2>&1



