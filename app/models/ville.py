from sqlmodel import Field, SQLModel


class Ville(SQLModel, table=True):
    """Informations sur les villes suivies."""

    id: int | None = Field(default=None, primary_key=True)
    nom: str = Field(nullable=False)
    latitude: float = Field(nullable=False)
    longitude: float = Field(nullable=False)

#Représente la table SQLite, grâce à SQLModel