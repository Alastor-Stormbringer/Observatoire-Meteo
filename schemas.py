from datetime import datetime

from sqlmodel import Field, SQLModel


class VilleCreate(SQLModel):
    nom: str = Field(min_length=1)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class VilleRead(SQLModel):
    id: int
    nom: str
    latitude: float
    longitude: float


class MeteoRead(SQLModel):
    ville: str
    temperature: float
    vitesse_vent: float
    date_heure: datetime
    unite_temperature: str
    unite_vitesse_vent: str

