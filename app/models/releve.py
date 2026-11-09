from datetime import datetime

from sqlmodel import Field, SQLModel


class Releve(SQLModel, table=True):
    """Informations sur les relevés météorologiques."""

    id: int | None = Field(default=None, primary_key=True)
    ville_id: int = Field(foreign_key="ville.id")
    temperature: float = Field(nullable=False)
    vitesse_vent: float = Field(nullable=False)
    date_heure: datetime = Field(nullable=False)

