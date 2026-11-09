from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep
from app.models.releve import Releve
from app.api.v1.schemas.meteo import MeteoRead
from app.repositories.ville_repository import obtenir_ville
from app.repositories.releve_repository import enregistrer_releve
from app.services.meteo_service import obtenir_meteo_actuelle


router = APIRouter(prefix="/meteo", tags=["Météo"])


@router.get("/{ville_id}", response_model=MeteoRead)
def obtenir_meteo(ville_id: int, session: SessionDep):
    ville = obtenir_ville(session, ville_id)

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

    enregistrer_releve(session, releve)

    return MeteoRead(ville=ville.nom, **donnees)