"""Form 2a (konteks strategis Pemda — per tahun), 2b (strategis OPD), 2c (operasional OPD)."""
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Depends
from sqlmodel import Session, select

from app.db import get_session
from app.models import KonteksOperasionalOpd, KonteksStrategisOpd, KonteksStrategisPemda
from app.routers.crud_helper import make_opd_tahun_router

router = APIRouter(prefix="/konteks", tags=["konteks"])


# ----------------------- Form 2a: Konteks Strategis Pemda ---------------------
@router.get("/pemda")
def get_pemda(tahun: int, session: Session = Depends(get_session)):
    obj = session.exec(
        select(KonteksStrategisPemda).where(KonteksStrategisPemda.tahun == tahun)
    ).first()
    return obj


@router.post("/pemda")
def save_pemda(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    tahun = payload["tahun"]
    obj = session.exec(
        select(KonteksStrategisPemda).where(KonteksStrategisPemda.tahun == tahun)
    ).first()
    if not obj:
        obj = KonteksStrategisPemda(tahun=tahun)
    fields = KonteksStrategisPemda.model_fields
    for k, v in payload.items():
        if k in fields and k not in ("id", "tahun"):
            setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


# Form 2b & 2c — per OPD & tahun (umumnya satu baris, tapi diizinkan banyak)
router.include_router(
    make_opd_tahun_router(
        model=KonteksStrategisOpd, prefix="/strategis-opd", tag="konteks"
    )
)
router.include_router(
    make_opd_tahun_router(
        model=KonteksOperasionalOpd, prefix="/operasional-opd", tag="konteks"
    )
)
