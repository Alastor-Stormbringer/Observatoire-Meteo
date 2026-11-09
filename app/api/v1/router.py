from fastapi import APIRouter

from app.api.v1.routes.villes import router as villes_router
from app.api.v1.routes.meteo import router as meteo_router


api_router = APIRouter()

api_router.include_router(villes_router)
api_router.include_router(meteo_router)