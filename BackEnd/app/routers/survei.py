"""Survei publik kuesioner CEE — responden login Google (Firebase), isi jawaban.

Endpoint publik (tanpa token): info, daftar OPD, daftar pertanyaan.
Endpoint butuh token (Bearer Firebase ID token): submit & me.
"""
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import func, or_
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.config import settings
from app.db import get_session
from app.models import (
    CeeJawaban,
    CeeResponden,
    KuesionerKategori,
    KuesionerPertanyaan,
    Opd,
)
from app.services.firebase_auth import current_user

router = APIRouter(prefix="/survei", tags=["survei"])


@router.get("/info")
def info(session: Session = Depends(get_session)):
    n = len(
        session.exec(
            select(KuesionerPertanyaan).where(KuesionerPertanyaan.aktif == 1)
        ).all()
    )
    return {
        "judul": "Survei Penilaian Lingkungan Pengendalian Intern (CEE)",
        "instansi": settings.PROJECT_NAME,
        "tahun": settings.TAHUN_ANGGARAN,
        "jumlah_pertanyaan": n,
        "skala": [
            {"nilai": 1, "label": "Tidak Setuju"},
            {"nilai": 2, "label": "Kurang Setuju"},
            {"nilai": 3, "label": "Setuju"},
            {"nilai": 4, "label": "Sangat Setuju"},
        ],
    }


@router.get("/opd")
def opd_list(session: Session = Depends(get_session)):
    rows = session.exec(
        select(Opd).where(Opd.aktif == 1).order_by(Opd.nama_pd)
    ).all()
    return [{"id_sub_pd": o.id_sub_pd, "nama_pd": o.nama_pd} for o in rows]


@router.get("/kuesioner")
def kuesioner(session: Session = Depends(get_session)):
    kats = session.exec(
        select(KuesionerKategori).order_by(KuesionerKategori.urutan)
    ).all()
    pers = session.exec(
        select(KuesionerPertanyaan)
        .where(KuesionerPertanyaan.aktif == 1)
        .order_by(KuesionerPertanyaan.urutan)
    ).all()
    by_kat: dict[int, list] = {}
    for p in pers:
        by_kat.setdefault(p.kategori_id, []).append(
            {"id": p.id, "nomor": p.nomor, "pertanyaan": p.pertanyaan}
        )
    return [
        {"id": k.id, "kode": k.kode, "nama": k.nama, "pertanyaan": by_kat.get(k.id, [])}
        for k in kats
    ]


def _norm_email(email: str | None) -> str | None:
    return (email or "").strip().lower() or None


def _find_survei(
    session: Session, email: str | None, uid: str | None, tahun: int
) -> CeeResponden | None:
    """Submission survei untuk satu tahun (lintas OPD), dicocokkan per EMAIL.

    Aturan: satu email hanya boleh mengisi survei satu kali per tahun. uid
    dipakai sebagai pencocokan tambahan (mis. bila email lama sempat berbeda),
    tetapi email adalah kunci utama.
    """
    email_norm = _norm_email(email)
    conds = []
    if email_norm:
        conds.append(func.lower(CeeResponden.email) == email_norm)
    if uid:
        conds.append(CeeResponden.firebase_uid == uid)
    if not conds:
        return None
    return session.exec(
        select(CeeResponden).where(
            CeeResponden.tahun == tahun,
            CeeResponden.sumber == "survei",
            or_(*conds),
        )
    ).first()


def _next_kode(session: Session, opd_id: int, tahun: int) -> str:
    existing = session.exec(
        select(CeeResponden.kode_responden).where(
            CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun
        )
    ).all()
    nums = [int(k[1:]) for k in existing if k and k[1:].isdigit() and k[0] in "Rr"]
    return f"R{(max(nums) + 1) if nums else 1}"


@router.get("/status")
def survey_status(
    tahun: int,
    user: dict = Depends(current_user),
    session: Session = Depends(get_session),
):
    """Status pengisian survei akun ini pada satu tahun.

    Karena satu email hanya boleh mengisi sekali per tahun, status `submitted`
    bersifat lintas-OPD (terkunci setelah submit pertama).
    """
    resp = _find_survei(session, user.get("email"), user.get("uid"), tahun)
    if not resp:
        return {"submitted": False}
    jawaban = {
        j.pertanyaan_id: j.nilai
        for j in session.exec(
            select(CeeJawaban).where(CeeJawaban.responden_id == resp.id)
        ).all()
    }
    opd = session.get(Opd, resp.opd_id)
    return {
        "submitted": True,
        "kode_responden": resp.kode_responden,
        "opd_id": resp.opd_id,
        "opd_nama": opd.nama_pd if opd else None,
        "nama_responden": resp.nama_responden,
        "jabatan": resp.jabatan,
        "submitted_at": resp.updated_at.isoformat() if resp.updated_at else None,
        "jawaban": jawaban,
    }


@router.post("/submit")
def submit(
    payload: dict[str, Any] = Body(...),
    user: dict = Depends(current_user),
    session: Session = Depends(get_session),
):
    opd_id = payload.get("opd_id")
    tahun = payload.get("tahun")
    jabatan = payload.get("jabatan")
    # Nama responden diisi manual di form; fallback ke nama/email akun Google.
    nama_responden = (payload.get("nama_responden") or "").strip() or (
        user.get("name") or user.get("email")
    )
    jawaban = payload.get("jawaban") or {}  # {pertanyaan_id: nilai}

    if not opd_id or not tahun:
        raise HTTPException(400, "opd_id dan tahun wajib diisi")
    if not session.get(Opd, opd_id):
        raise HTTPException(404, "OPD tidak ditemukan")

    # Email wajib — jadi kunci "satu email satu tahun".
    email = _norm_email(user.get("email"))
    if not email:
        raise HTTPException(400, "Akun Google tidak memiliki email; tidak dapat mengisi survei")

    valid_pids = {
        p.id
        for p in session.exec(
            select(KuesionerPertanyaan).where(KuesionerPertanyaan.aktif == 1)
        ).all()
    }

    # Validasi jawaban
    clean: dict[int, int] = {}
    for pid, nilai in jawaban.items():
        try:
            pid_i, nilai_i = int(pid), int(nilai)
        except (TypeError, ValueError):
            continue
        if pid_i in valid_pids and 1 <= nilai_i <= 4:
            clean[pid_i] = nilai_i

    if not clean:
        raise HTTPException(400, "Tidak ada jawaban yang valid (skala 1-4)")

    # Satu email hanya boleh mengisi survei SATU KALI per tahun (lintas OPD).
    existing = _find_survei(session, email, user.get("uid"), tahun)
    if existing:
        opd = session.get(Opd, existing.opd_id)
        raise HTTPException(
            409,
            f"Email {email} sudah mengisi survei Tahun {tahun} "
            f"(OPD: {opd.nama_pd if opd else existing.opd_id}). "
            "Setiap email hanya dapat mengisi survei satu kali dalam satu tahun.",
        )

    resp = CeeResponden(
        opd_id=opd_id,
        tahun=tahun,
        kode_responden=_next_kode(session, opd_id, tahun),
        firebase_uid=user.get("uid"),
        sumber="survei",
        nama_responden=nama_responden,
        email=email,
        jabatan=jabatan,
    )
    session.add(resp)
    try:
        session.commit()
    except IntegrityError:
        # Pengaman balapan (race) — unique index parsial (lower(email), tahun)
        # untuk sumber='survei'. Lihat migrations/2026_07_27_cee_responden_email_unique.sql
        session.rollback()
        raise HTTPException(
            409,
            "Email ini sudah mengisi survei tahun ini. "
            "Setiap email hanya dapat mengisi survei satu kali dalam satu tahun.",
        ) from None
    session.refresh(resp)

    for pid, nilai in clean.items():
        session.add(CeeJawaban(responden_id=resp.id, pertanyaan_id=pid, nilai=nilai))
    session.commit()

    return {
        "ok": True,
        "kode_responden": resp.kode_responden,
        "jumlah_jawaban": len(clean),
    }
