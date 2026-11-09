from fastapi import APIRouter, HTTPException, status
from app.api.deps import SessionDep
from app.api.v1.schemas.ville import VilleCreate, VilleRead
from app.repositories.ville_repository import (
    lister_villes as recuperer_villes_db,
    obtenir_ville as recuperer_ville_db,
)
from app.services.ville_service import creer_ville as creer_ville_service

router = APIRouter(prefix="/villes", tags=["Villes"])

@router.post("", response_model=VilleRead, status_code=status.HTTP_201_CREATED)
def creer_ville(ville_in: VilleCreate, session: SessionDep):
    ville = creer_ville_service(session, ville_in)

    if ville is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La ville « {ville_in.nom} » existe déjà.",
        )

    return ville


@router.get("", response_model=list[VilleRead])
def lister_villes(session: SessionDep):
    return recuperer_villes_db(session)


@router.get("/{ville_id}", response_model=VilleRead)
def obtenir_ville(ville_id: int, session: SessionDep):
    ville = recuperer_ville_db(session, ville_id)

    if ville is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ville introuvable.",
        )

    return ville