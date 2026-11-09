from sqlmodel import Session

from app.models.ville import Ville
from app.api.v1.schemas.ville import VilleCreate
from app.repositories.ville_repository import (
    obtenir_ville_par_nom,
    enregistrer_ville,
)


def creer_ville(session: Session, ville_in: VilleCreate):
    ville_existante = obtenir_ville_par_nom(session, ville_in.nom)

    if ville_existante:
        return None

    ville = Ville(
        nom=ville_in.nom,
        latitude=ville_in.latitude,
        longitude=ville_in.longitude,
    )

    return enregistrer_ville(session, ville)