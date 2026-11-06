from sqlmodel import Session, SQLModel, create_engine

import models.releve
import models.ville

DATABASE_URL = "sqlite:///./meteo.db"
engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def creer_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    creer_tables()
    print("Les tables ont été créées avec succès !")

