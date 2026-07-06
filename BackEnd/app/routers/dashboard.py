"""Ringkasan dashboard per OPD & tahun."""
from fastapi import APIRouter, Depends
from sqlmodel import Session, func, select

from app.db import get_session
from app.models import AnalisisRisiko, CeeResponden, Risiko
from app.services import analisis as an

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/summary")
def summary(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    jumlah_responden = session.exec(
        select(func.count(CeeResponden.id)).where(
            CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun
        )
    ).one()

    risiko = session.exec(
        select(Risiko).where(Risiko.opd_id == opd_id, Risiko.tahun == tahun)
    ).all()
    ids = [r.id for r in risiko]
    amap = {}
    if ids:
        amap = {
            a.risiko_id: a
            for a in session.exec(
                select(AnalisisRisiko).where(AnalisisRisiko.risiko_id.in_(ids))
            ).all()
        }

    per_jenis: dict[str, int] = {}
    per_level: dict[str, int] = {
        an.LEVEL_RENDAH: 0,
        an.LEVEL_SEDANG: 0,
        an.LEVEL_TINGGI: 0,
        an.LEVEL_SANGAT_TINGGI: 0,
    }
    jumlah_prioritas = 0
    jumlah_dianalisis = 0
    for r in risiko:
        per_jenis[r.jenis_risiko] = per_jenis.get(r.jenis_risiko, 0) + 1
        a = amap.get(r.id)
        if a and a.skala_risiko is not None:
            jumlah_dianalisis += 1
            lvl = an.level_risiko(a.skala_risiko)
            per_level[lvl] = per_level.get(lvl, 0) + 1
            if a.is_prioritas:
                jumlah_prioritas += 1

    return {
        "opd_id": opd_id,
        "tahun": tahun,
        "jumlah_responden": jumlah_responden,
        "jumlah_risiko": len(risiko),
        "jumlah_dianalisis": jumlah_dianalisis,
        "jumlah_prioritas": jumlah_prioritas,
        "risiko_per_jenis": per_jenis,
        "risiko_per_level": per_level,
    }
