from sqlmodel import Session, SQLModel, create_engine
from app.core.config import DATABASE_URL
import app.models.releve
import app.models.ville

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

