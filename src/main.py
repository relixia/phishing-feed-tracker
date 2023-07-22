from tasks import usom, phishtank, openphish, phishstats
from celery_base import app
from fastapi import FastAPI

app_fastapi = FastAPI()  # Create a new FastAPI app

# Define FastAPI endpoints for each task
@app_fastapi.get("/usom")
async def run_usom():
    usom.delay()
    return {"message": "USOM task has been started"}

@app_fastapi.get("/phishtank")
async def run_phishtank():
    phishtank.delay()
    return {"message": "Phishtank task has been started"}

@app_fastapi.get("/openphish")
async def run_openphish():
    openphish.delay()
    return {"message": "Openphish task has been started"}

@app_fastapi.get("/phishstats")
async def run_phishstats():
    phishstats.delay()
    return {"message": "Phishstats task has been started"}

if __name__ == "__main__":
    # Start the FastAPI server with Uvicorn
    import uvicorn
    uvicorn.run(app_fastapi, host="0.0.0.0", port=8000)