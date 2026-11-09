from sqlmodel import Session, select

from app.models.ville import Ville


def lister_villes(session: Session):
    return session.exec(select(Ville).order_by(Ville.nom)).all()


def obtenir_ville(session: Session, ville_id: int):
    return session.get(Ville, ville_id)


def obtenir_ville_par_nom(session: Session, nom: str):
    return session.exec(
        select(Ville).where(Ville.nom == nom)
    ).first()

def enregistrer_ville(session: Session, ville: Ville):
    session.add(ville)
    session.commit()
    session.refresh(ville)
    return ville