import requests
from celery_config import app

@app.task
def reverse(text):
    return text[::-1]

    