from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import creer_tables
from app.api.v1.router import api_router

@asynccontextmanager
async def lifespan(_: FastAPI):
    creer_tables()
    yield


app = FastAPI(
    title="API Météo",
    description="Gestion des villes suivies et consultation de leur météo actuelle.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(api_router)


#Config et démarrage de fastAPI.