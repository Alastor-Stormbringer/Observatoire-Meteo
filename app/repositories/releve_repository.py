from sqlmodel import Session

from app.models.releve import Releve


def enregistrer_releve(session: Session, releve: Releve):
    session.add(releve)
    session.commit()
    session.refresh(releve)
    return releve