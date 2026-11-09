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

    #Définit les données que notre API accepte ou renvoie, grâce à la validation Pydantic.