from contextlib import asynccontextmanager
from datetime import datetime

import requests
from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import creer_tables, get_session
from models.releve import Releve
from models.ville import Ville
from schemas import MeteoRead, VilleCreate, VilleRead

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


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


def obtenir_meteo_actuelle(latitude: float, longitude: float) -> dict:
    """Interroge l'API Open-Meteo pour récupérer la météo actuelle."""
    try:
        response = requests.get(
            OPEN_METEO_URL,
            params={
                "latitude": latitude,
                "longitude": longitude,
                "current": "temperature_2m,wind_speed_10m",
            },
            timeout=10,
        )
        response.raise_for_status()
        data = response.json()
        current = data["current"]
        units = data["current_units"]
        return {
            "temperature": float(current["temperature_2m"]),
            "vitesse_vent": float(current["wind_speed_10m"]),
            "date_heure": datetime.fromisoformat(current["time"]),
            "unite_temperature": units["temperature_2m"],
            "unite_vitesse_vent": units["wind_speed_10m"],
        }
    except (requests.RequestException, KeyError, TypeError, ValueError) as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Impossible de récupérer les données météo depuis Open-Meteo.",
        ) from exc


@app.post("/villes", response_model=VilleRead, status_code=status.HTTP_201_CREATED, tags=["Villes"])
def creer_ville(ville_in: VilleCreate, session: Session = Depends(get_session)):
    ville_existante = session.exec(select(Ville).where(Ville.nom == ville_in.nom)).first()
    if ville_existante:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La ville « {ville_in.nom} » existe déjà.",
        )

    ville = Ville(
        nom=ville_in.nom,
        latitude=ville_in.latitude,
        longitude=ville_in.longitude,
    )
    session.add(ville)
    session.commit()
    session.refresh(ville)
    return ville


@app.get("/villes", response_model=list[VilleRead], tags=["Villes"])
def lister_villes(session: Session = Depends(get_session)):
    return session.exec(select(Ville).order_by(Ville.nom)).all()


@app.get("/villes/{ville_id}", response_model=VilleRead, tags=["Villes"])
def obtenir_ville(ville_id: int, session: Session = Depends(get_session)):
    ville = session.get(Ville, ville_id)
    if ville is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ville introuvable.",
        )
    return ville


@app.get("/meteo/{ville_id}", response_model=MeteoRead, tags=["Météo"])
def obtenir_meteo(ville_id: int, session: Session = Depends(get_session)):
    ville = session.get(Ville, ville_id)
    if ville is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ville introuvable.",
        )

    donnees = obtenir_meteo_actuelle(ville.latitude, ville.longitude)

    releve = Releve(
        ville_id=ville.id,
        temperature=donnees["temperature"],
        vitesse_vent=donnees["vitesse_vent"],
        date_heure=donnees["date_heure"],
    )
    session.add(releve)
    session.commit()

    return MeteoRead(ville=ville.nom, **donnees)
