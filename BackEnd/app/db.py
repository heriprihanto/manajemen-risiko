from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)


def init_db() -> None:
    # Import models so SQLModel metadata is populated before create_all.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
