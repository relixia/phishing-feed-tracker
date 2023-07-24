from fastapi import FastAPI
from tasks import usom_check_time_interval, phishtank_check_time_interval, openphish_check_time_interval, phishstats_check_time_interval, get_all_urls
from celery_base import app

app_fastapi = FastAPI()


@app_fastapi.get("/urls", response_model=list[dict])
async def get_urls():
    all_urls = get_all_urls()
    return all_urls


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)
