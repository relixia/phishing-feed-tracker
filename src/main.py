from tasks import usom, phishtank, openphish, phishstats
from celery_base import app

if __name__ == "__main__":
    phishtank.delay()

    usom.delay()

    openphish.delay()
    
    phishstats.delay()