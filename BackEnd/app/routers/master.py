"""Endpoint master/referensi: OPD, katalog kuesioner CEE, item dokumen CEE."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlmodel import Session, select

from app.db import get_session
from app.models import CeeDokumenItem, KuesionerKategori, KuesionerPertanyaan, Opd

router = APIRouter(prefix="/master", tags=["master"])


def _id_pd(session: Session, opd_id: int) -> int | None:
    """Peta opd_id aplikasi (ta_opd.id_sub_pd) ke id_pd yang dipakai tabel renstra."""
    return session.exec(
        select(Opd.id_pd).where(Opd.id_sub_pd == opd_id)
    ).first()


@router.get("/opd")
def list_opd(aktif_only: bool = True, session: Session = Depends(get_session)):
    stmt = select(Opd)
    if aktif_only:
        stmt = stmt.where(Opd.aktif == 1)
    stmt = stmt.order_by(Opd.nama_pd)
    return session.exec(stmt).all()


@router.get("/opd/{opd_id}")
def get_opd(opd_id: int, session: Session = Depends(get_session)):
    return session.get(Opd, opd_id)


@router.get("/kuesioner")
def list_kuesioner(session: Session = Depends(get_session)):
    """Kategori (sub-unsur) beserta daftar pertanyaannya."""
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
        by_kat.setdefault(p.kategori_id, []).append(p)
    return [
        {
            "id": k.id,
            "kode": k.kode,
            "nama": k.nama,
            "urutan": k.urutan,
            "pertanyaan": by_kat.get(k.id, []),
        }
        for k in kats
    ]


@router.get("/dokumen-item")
def list_dokumen_item(session: Session = Depends(get_session)):
    return session.exec(
        select(CeeDokumenItem).order_by(CeeDokumenItem.urutan)
    ).all()


# --------------------- Renstra OPD (sumber pilihan Form 2.b) -------------------
# Opsi dikembalikan sbg {value,label}; value = teks uraian yang disimpan apa
# adanya di kolom konteks (agar laporan tetap terbaca), label = versi bernomor.
@router.get("/renstra/tujuan")
def list_renstra_tujuan(
    opd_id: int, tahun: int, session: Session = Depends(get_session)
):
    id_pd = _id_pd(session, opd_id)
    if id_pd is None:
        return []
    rows = session.exec(
        text(
            "SELECT nomor, uraitujuan FROM renstra_tujuan "
            "WHERE id_pd = :pd AND tahun = :tahun "
            "ORDER BY nomor"
        ).bindparams(pd=id_pd, tahun=tahun)
    ).all()
    return [
        {"value": r.uraitujuan, "label": f"{r.nomor}. {r.uraitujuan}"}
        for r in rows
        if r.uraitujuan
    ]


@router.get("/renstra/sasaran")
def list_renstra_sasaran(
    opd_id: int, tahun: int, session: Session = Depends(get_session)
):
    """Menyertakan `tujuan_strategis` (uraian tujuan induk) untuk cascading."""
    id_pd = _id_pd(session, opd_id)
    if id_pd is None:
        return []
    rows = session.exec(
        text(
            "SELECT s.nomor, s.uraisasaran, t.uraitujuan "
            "FROM renstra_sasaran s "
            "JOIN renstra_tujuan t ON t.idtujuan = s.idtujuan "
            "WHERE s.id_pd = :pd AND s.tahun = :tahun "
            "ORDER BY t.nomor, s.nomor"
        ).bindparams(pd=id_pd, tahun=tahun)
    ).all()
    return [
        {
            "value": r.uraisasaran,
            "label": f"{r.nomor}. {r.uraisasaran}",
            "tujuan_strategis": r.uraitujuan,
        }
        for r in rows
        if r.uraisasaran
    ]


@router.get("/renstra/iku")
def list_renstra_iku(opd_id: int, session: Session = Depends(get_session)):
    """Indikator Kinerja Utama (iku=1) renstra OPD untuk field IKU Renstra."""
    id_pd = _id_pd(session, opd_id)
    if id_pd is None:
        return []
    rows = session.exec(
        text(
            "SELECT indikator FROM renstra_indikator_tujuan_sasaran "
            "WHERE id_pd = :pd AND iku = '1' "
            "ORDER BY urut"
        ).bindparams(pd=id_pd)
    ).all()
    return [
        {"value": r.indikator, "label": r.indikator}
        for r in rows
        if r.indikator
    ]


@router.get("/renstra/tahap")
def list_renstra_tahap(session: Session = Depends(get_session)):
    """Periode renstra (mis. '2025 - 2029') untuk field Periode Dinilai."""
    rows = session.exec(
        text(
            "SELECT nama_renstra, periode FROM renstra_tahap "
            "ORDER BY tahun1"
        )
    ).all()
    return [
        {
            "value": r.periode,
            "label": f"{r.nama_renstra} {r.periode}".strip()
            if r.nama_renstra
            else r.periode,
        }
        for r in rows
        if r.periode
    ]


@router.get("/renstra/program")
def list_renstra_program(opd_id: int, session: Session = Depends(get_session)):
    id_pd = _id_pd(session, opd_id)
    if id_pd is None:
        return []
    rows = session.exec(
        text(
            "SELECT no, kodeprogram, uraiprogram FROM renstra_program "
            "WHERE id_pd = :pd ORDER BY no"
        ).bindparams(pd=id_pd)
    ).all()
    return [
        {"value": r.uraiprogram, "label": f"{r.kodeprogram} — {r.uraiprogram}"}
        for r in rows
        if r.uraiprogram
    ]
