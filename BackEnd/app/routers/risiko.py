"""Form 3a/3b/3c (identifikasi risiko), Form 4 (analisis), Form 5 (prioritas),
Matriks Risiko, Form 7 (RTP risiko)."""
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select

from app.core.security import UserDep, ensure_opd_access, guard_record
from app.db import get_session
from app.models import AnalisisRisiko, Risiko, RtpRisiko
from app.models.risiko import JENIS_RISIKO
from app.services import analisis as an

router = APIRouter(prefix="/risiko", tags=["risiko"])

JENIS_LABEL = {
    "strategis_pemda": "Risiko Strategis Pemda (Form 3.a)",
    "strategis_opd": "Risiko Strategis OPD (Form 3.b)",
    "operasional_opd": "Risiko Operasional OPD (Form 3.c)",
}


def _analisis_dict(a: AnalisisRisiko | None) -> dict[str, Any]:
    if not a:
        return {
            "skala_dampak": None,
            "skala_kemungkinan": None,
            "skala_risiko": None,
            "level": None,
            "is_prioritas": False,
        }
    return {
        "skala_dampak": a.skala_dampak,
        "skala_kemungkinan": a.skala_kemungkinan,
        "skala_risiko": a.skala_risiko,
        "level": an.level_risiko(a.skala_risiko),
        "is_prioritas": a.is_prioritas,
    }


# ----------------------- Form 3a/3b/3c: Identifikasi --------------------------
@router.get("")
def list_risiko(
    opd_id: int,
    tahun: int,
    jenis: str | None = None,
    session: Session = Depends(get_session),
):
    stmt = select(Risiko).where(Risiko.opd_id == opd_id, Risiko.tahun == tahun)
    if jenis:
        stmt = stmt.where(Risiko.jenis_risiko == jenis)
    stmt = stmt.order_by(Risiko.jenis_risiko, Risiko.urutan, Risiko.id)
    risiko = session.exec(stmt).all()

    ids = [r.id for r in risiko]
    amap: dict[int, AnalisisRisiko] = {}
    if ids:
        amap = {
            a.risiko_id: a
            for a in session.exec(
                select(AnalisisRisiko).where(AnalisisRisiko.risiko_id.in_(ids))
            ).all()
        }
    out = []
    for r in risiko:
        d = r.model_dump()
        d["analisis"] = _analisis_dict(amap.get(r.id))
        out.append(d)
    return out


@router.post("")
def create_risiko(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    if payload.get("jenis_risiko") not in JENIS_RISIKO:
        raise HTTPException(400, f"jenis_risiko harus salah satu dari {JENIS_RISIKO}")
    obj = Risiko()
    fields = Risiko.model_fields
    for k, v in payload.items():
        if k in fields and k not in ("id", "created_at"):
            setattr(obj, k, v)
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put("/{rid}")
def update_risiko(
    rid: int,
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    obj = guard_record(user, session.get(Risiko, rid), "Risiko")
    fields = Risiko.model_fields
    for k, v in payload.items():
        if k in fields and k not in ("id", "created_at", "opd_id"):
            setattr(obj, k, v)
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/{rid}")
def delete_risiko(
    rid: int, session: Session = Depends(get_session), user: dict = UserDep
):
    obj = guard_record(user, session.get(Risiko, rid), "Risiko")
    for a in session.exec(
        select(AnalisisRisiko).where(AnalisisRisiko.risiko_id == rid)
    ).all():
        session.delete(a)
    for rt in session.exec(select(RtpRisiko).where(RtpRisiko.risiko_id == rid)).all():
        session.delete(rt)
    session.delete(obj)
    session.commit()
    return {"ok": True}


# ----------------------------- Form 4: Analisis ------------------------------
@router.post("/analisis")
def save_analisis(
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    risiko_id = payload["risiko_id"]
    guard_record(user, session.get(Risiko, risiko_id), "Risiko")
    dampak = payload.get("skala_dampak")
    kemungkinan = payload.get("skala_kemungkinan")
    skala = an.hitung_skala(dampak, kemungkinan)

    obj = session.exec(
        select(AnalisisRisiko).where(AnalisisRisiko.risiko_id == risiko_id)
    ).first()
    if not obj:
        obj = AnalisisRisiko(risiko_id=risiko_id)
    obj.skala_dampak = dampak
    obj.skala_kemungkinan = kemungkinan
    obj.skala_risiko = skala
    # is_prioritas: pakai nilai eksplisit bila dikirim, kalau tidak gunakan default.
    if "is_prioritas" in payload and payload["is_prioritas"] is not None:
        obj.is_prioritas = bool(payload["is_prioritas"])
    else:
        obj.is_prioritas = an.is_prioritas_default(skala)
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return _analisis_dict(obj)


@router.get("/form4")
def form_4(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Hasil analisis risiko, dikelompokkan per jenis."""
    rows = list_risiko(opd_id, tahun, None, session)
    grouped: dict[str, list] = {j: [] for j in JENIS_RISIKO}
    for r in rows:
        grouped.setdefault(r["jenis_risiko"], []).append(r)
    return [
        {"jenis": j, "label": JENIS_LABEL[j], "items": grouped.get(j, [])}
        for j in JENIS_RISIKO
    ]


# ------------------------------ Matriks Risiko -------------------------------
@router.get("/matriks")
def matriks(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Sebaran risiko dalam matriks 4x4 (kemungkinan x dampak)."""
    rows = list_risiko(opd_id, tahun, None, session)
    cells: dict[str, list] = {}
    for r in rows:
        a = r["analisis"]
        d, k = a["skala_dampak"], a["skala_kemungkinan"]
        if d and k:
            cells.setdefault(f"{k}-{d}", []).append(
                {"kode": r.get("kode_risiko"), "uraian": r.get("uraian_risiko")}
            )
    return {
        "dampak_label": an.DAMPAK_LABEL,
        "kemungkinan_label": an.KEMUNGKINAN_LABEL,
        "cells": cells,
    }


# ------------------------------ Form 5: Prioritas ----------------------------
@router.get("/form5")
def form_5(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Daftar risiko prioritas (is_prioritas=True), diurutkan skala menurun."""
    rows = list_risiko(opd_id, tahun, None, session)
    prioritas = [r for r in rows if r["analisis"]["is_prioritas"]]
    prioritas.sort(key=lambda r: r["analisis"]["skala_risiko"] or 0, reverse=True)
    grouped: dict[str, list] = {j: [] for j in JENIS_RISIKO}
    for r in prioritas:
        grouped.setdefault(r["jenis_risiko"], []).append(r)
    return [
        {"jenis": j, "label": JENIS_LABEL[j], "items": grouped.get(j, [])}
        for j in JENIS_RISIKO
    ]


# ------------------------------ Form 7: RTP Risiko ---------------------------
@router.get("/rtp")
def list_rtp(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Risiko prioritas + RTP-nya (Form 7)."""
    rows = list_risiko(opd_id, tahun, None, session)
    prioritas = [r for r in rows if r["analisis"]["is_prioritas"]]
    ids = [r["id"] for r in prioritas]
    rtp_map: dict[int, RtpRisiko] = {}
    if ids:
        rtp_map = {
            rt.risiko_id: rt
            for rt in session.exec(
                select(RtpRisiko).where(RtpRisiko.risiko_id.in_(ids))
            ).all()
        }
    out = []
    for r in prioritas:
        rt = rtp_map.get(r["id"])
        rtp = rt.model_dump() if rt else None
        if rtp is not None:
            # Pemilik/penanggung jawab selalu mengikuti Form 3.b (satu sumber
            # data) — tampilkan nilai terkini meski RTP disimpan lebih dulu.
            rtp["pemilik_penanggung_jawab"] = r.get("pemilik_risiko")
        out.append({**r, "rtp": rtp})
    return out


@router.post("/rtp")
def save_rtp(
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    risiko_id = payload["risiko_id"]
    risiko = session.get(Risiko, risiko_id)
    guard_record(user, risiko, "Risiko")
    obj = session.exec(
        select(RtpRisiko).where(RtpRisiko.risiko_id == risiko_id)
    ).first()
    if not obj:
        obj = RtpRisiko(risiko_id=risiko_id)
    fields = RtpRisiko.model_fields
    # pemilik_penanggung_jawab tidak diambil dari client — selalu ikut Form 3.b.
    for k, v in payload.items():
        if k in fields and k not in ("id", "risiko_id", "pemilik_penanggung_jawab"):
            setattr(obj, k, v)
    obj.pemilik_penanggung_jawab = risiko.pemilik_risiko
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj
