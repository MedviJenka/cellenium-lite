import uvicorn
from fastapi import FastAPI
from backend.api.v1.bini import api
from backend.settings import Config
from backend.utils.logger import Logfire
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.api.health_schema import HealthResponseSchema


log = Logfire(name='bini_api_client')

METADATA = {
    'title': "Bini AI Vision API",
    'description': "Computer Vision Agent API for image analysis",
    'version':Config.API_VERSION,
    'lifespan': api.lifespan
}


app = FastAPI(**METADATA)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(api.router)


@app.get('/')
def root() -> RedirectResponse:
    """root directory redirect to docs"""
    return RedirectResponse(url='/docs')


@app.get('/health')
def health() -> HealthResponseSchema:
    log.fire.info("Health check endpoint called")
    return HealthResponseSchema(api=Config.API_VERSION, env=Config.ENV)


if __name__ == "__main__":

    # TODO: conduct a research about workers which will handle the traffic
    # The common formula for worker count in Gunicorn (and by extension FastAPI) is:
    # workers = (CPU cores × 2) + 1

    uvicorn.run(app="services.bini:app", host="0.0.0.0", port=8081, log_level="info", use_colors=True)
