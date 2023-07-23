from fastapi import FastAPI
from tasks import usom, phishtank, openphish, phishstats, get_all_urls
from celery_base import app

app_fastapi = FastAPI()


usom_triggered = False
phishtank_triggered = False
openphish_triggered = False
phishstats_triggered = False


@app_fastapi.get("/usom")
async def run_usom():
    global usom_triggered
    if not usom_triggered:
        usom.delay()
        usom_triggered = True
        return {"message": "USOM task has been started"}
    else:
        return {"message": "USOM task has already been triggered"}

@app_fastapi.get("/phishtank")
async def run_phishtank():
    global phishtank_triggered
    if not phishtank_triggered:
        phishtank.delay()
        phishtank_triggered = True
        return {"message": "Phishtank task has been started"}
    else:
        return {"message": "Phishtank task has already been triggered"}

@app_fastapi.get("/openphish")
async def run_openphish():
    global openphish_triggered
    if not openphish_triggered:
        openphish.delay()
        openphish_triggered = True
        return {"message": "Openphish task has been started"}
    else:
        return {"message": "Openphish task has already been triggered"}

@app_fastapi.get("/phishstats")
async def run_phishstats():
    global phishstats_triggered
    if not phishstats_triggered:
        phishstats.delay()
        phishstats_triggered = True
        return {"message": "Phishstats task has been started"}
    else:
        return {"message": "Phishstats task has already been triggered"}


@app_fastapi.get("/urls", response_model=list[dict])
async def get_urls():
    all_urls = get_all_urls()
    return all_urls


if __name__ == "__main__":
    # Start the FastAPI server with Uvicorn
    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)
