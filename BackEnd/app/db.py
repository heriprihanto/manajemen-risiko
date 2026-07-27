from collections.abc import Generator

from sqlmodel import Session, SQLModel, create_engine, text

from app.core.config import settings

engine = create_engine(settings.database_url, echo=False, pool_pre_ping=True)

# Kolom yang ditambahkan setelah tabel pertama kali dibuat. create_all tidak
# mengubah tabel yang sudah ada, jadi terapkan lewat ALTER idempotent.
_COLUMN_MIGRATIONS = (
    "ALTER TABLE tr_risiko ADD COLUMN IF NOT EXISTS konteks_id integer",
    "ALTER TABLE tr_risiko ADD COLUMN IF NOT EXISTS konteks_sumber varchar",
    "ALTER TABLE tr_konteks_operasional_opd ADD COLUMN IF NOT EXISTS indikator_program varchar",
    "ALTER TABLE tr_konteks_operasional_opd ADD COLUMN IF NOT EXISTS ref_subkegiatan varchar",
    "ALTER TABLE tr_konteks_operasional_opd ADD COLUMN IF NOT EXISTS ref_indikator varchar",
)


def init_db() -> None:
    # Import models so SQLModel metadata is populated before create_all.
    import app.models  # noqa: F401

    SQLModel.metadata.create_all(engine)
    with engine.begin() as conn:
        for stmt in _COLUMN_MIGRATIONS:
            conn.execute(text(stmt))


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
