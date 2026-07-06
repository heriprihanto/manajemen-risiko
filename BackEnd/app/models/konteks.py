"""Penetapan konteks risiko — Form 2a (Pemda), 2b (Strategis OPD), 2c (Operasional OPD)."""
from datetime import datetime

from sqlmodel import Field, SQLModel


class KonteksStrategisPemda(SQLModel, table=True):
    """Form 2a — penetapan konteks risiko strategis pemerintah daerah (per tahun)."""
    __tablename__ = "tr_konteks_strategis_pemda"

    id: int | None = Field(default=None, primary_key=True)
    tahun: int = Field(index=True)
    visi: str | None = None
    misi_strategis: str | None = None
    penetapan_konteks_misi: str | None = None
    tujuan_strategis: str | None = None
    penetapan_konteks_tujuan: str | None = None
    sasaran_rpd: str | None = None
    penetapan_konteks_sasaran: str | None = None
    iku_sasaran: str | None = None
    penetapan_konteks_iku: str | None = None
    prioritas_program: str | None = None
    urusan_pemerintahan: str | None = None
    sumber_data: str | None = None
    periode_dinilai: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class KonteksStrategisOpd(SQLModel, table=True):
    """Form 2b — penetapan konteks risiko strategis OPD."""
    __tablename__ = "tr_konteks_strategis_opd"

    id: int | None = Field(default=None, primary_key=True)
    opd_id: int = Field(index=True)
    tahun: int = Field(index=True)
    sumber_data: str | None = None
    tujuan_strategis: str | None = None
    sasaran_strategis: str | None = None
    iku_renstra: str | None = None
    program: str | None = None
    tujuan_sasaran_iku_program: str | None = None
    urusan_pemerintahan: str | None = None
    periode_dinilai: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class KonteksOperasionalOpd(SQLModel, table=True):
    """Form 2c — penetapan konteks risiko operasional OPD."""
    __tablename__ = "tr_konteks_operasional_opd"

    id: int | None = Field(default=None, primary_key=True)
    opd_id: int = Field(index=True)
    tahun: int = Field(index=True)
    sumber_data: str | None = None
    tujuan_strategis: str | None = None
    program: str | None = None
    keluaran_hasil_kegiatan: str | None = None
    keluaran_sub_kegiatan: str | None = None
    urusan_pemerintahan: str | None = None
    periode_dinilai: str | None = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
