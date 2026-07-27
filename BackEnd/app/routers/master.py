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


@router.get("/opd/{opd_id}/print-context")
def opd_print_context(opd_id: int, session: Session = Depends(get_session)):
    """Data kop & tanda tangan cetak Form 2.b.

    `bidang_urusan` (text[]) hanya terisi di baris PD induk (id_sub_pd = id_pd),
    jadi diresolusi lewat join ke baris induk lalu digabung jadi satu string.
    """
    row = session.exec(
        text(
            "SELECT o.nama_pd, o.nama_kepala, o.nip_kepala, o.jabatan_kepala, "
            "       COALESCE(p.bidang_urusan, o.bidang_urusan) AS bidang_urusan "
            "FROM ta_opd o "
            "LEFT JOIN ta_opd p ON p.id_sub_pd = o.id_pd "
            "WHERE o.id_sub_pd = :opd_id"
        ).bindparams(opd_id=opd_id)
    ).first()
    if not row:
        return {}
    bu = row.bidang_urusan
    bidang = ", ".join(bu) if isinstance(bu, (list, tuple)) else (bu or "")
    return {
        "nama_pd": row.nama_pd,
        "nama_kepala": row.nama_kepala,
        "nip_kepala": row.nip_kepala,
        "jabatan_kepala": row.jabatan_kepala,
        "bidang_urusan": bidang,
    }


@router.get("/renja/subkegiatan")
def list_renja_subkegiatan(
    opd_id: int, tahun: int, session: Session = Depends(get_session)
):
    """Data checklist Form 2.c: subkegiatan (+indikator lvl-7 keluaran) dan
    indikator program (lvl-5) yang bisa dicentang sendiri. `id_sub_pd` renja =
    opd_id aplikasi (tanpa peta). Mengembalikan {subkegiatan, indikator_program}."""
    subs = session.exec(
        text(
            "SELECT idsubkegiatan, idprogram, idkegiatan, kode_sub_kegiatan, "
            "       nm_program, nm_kegiatan, nm_sub_kegiatan "
            "FROM renja_subkegiatan "
            "WHERE id_sub_pd = :opd_id AND tahun = :tahun "
            "ORDER BY kode_sub_kegiatan"
        ).bindparams(opd_id=opd_id, tahun=tahun)
    ).all()
    # nama & induk per id (untuk melabeli indikator program/kegiatan).
    prog_nama = {str(s.idprogram): s.nm_program for s in subs}
    keg_nama = {str(s.idkegiatan): s.nm_kegiatan for s in subs}
    keg_prog = {str(s.idkegiatan): str(s.idprogram) for s in subs}

    def _tgt(target, satuan):
        return " ".join(x for x in (target, satuan) if x)

    def _label(tolok, satuan, target):
        extra = _tgt(target, satuan)
        return f"{tolok} ({extra})" if extra else tolok

    # Indikator level-7 = keluaran subkegiatan (id_parent = idsubkegiatan).
    ind_sub = session.exec(
        text(
            "SELECT ri.id_parent, ri.tolok_ukur, ri.satuan, ri.target "
            "FROM renja_indikator ri "
            "JOIN renja_subkegiatan sk ON sk.idsubkegiatan = ri.id_parent "
            "WHERE sk.id_sub_pd = :opd_id AND sk.tahun = :tahun AND ri.lvl = 7 "
            "ORDER BY ri.nomor"
        ).bindparams(opd_id=opd_id, tahun=tahun)
    ).all()
    by_sub: dict[str, list[str]] = {}
    by_sub_list: dict[str, list[dict]] = {}  # terstruktur untuk cetak
    for r in ind_sub:
        if r.tolok_ukur:
            by_sub.setdefault(str(r.id_parent), []).append(
                _label(r.tolok_ukur, r.satuan, r.target)
            )
            by_sub_list.setdefault(str(r.id_parent), []).append(
                {"tolok": r.tolok_ukur, "target": _tgt(r.target, r.satuan)}
            )

    # Indikator level-5 = indikator program (id_parent = idprogram) & level-6 =
    # indikator kegiatan (id_parent = idkegiatan); tiap baris punya id sendiri
    # agar bisa dicentang terpisah.
    ind_prog = session.exec(
        text(
            "SELECT ri.id, ri.id_parent, ri.tolok_ukur, ri.satuan, ri.target "
            "FROM renja_indikator ri "
            "WHERE ri.lvl = 5 AND ri.id_parent IN ("
            "  SELECT DISTINCT idprogram FROM renja_subkegiatan "
            "  WHERE id_sub_pd = :opd_id AND tahun = :tahun) "
            "ORDER BY ri.nomor"
        ).bindparams(opd_id=opd_id, tahun=tahun)
    ).all()
    ind_keg = session.exec(
        text(
            "SELECT ri.id, ri.id_parent, ri.tolok_ukur, ri.satuan, ri.target "
            "FROM renja_indikator ri "
            "WHERE ri.lvl = 6 AND ri.id_parent IN ("
            "  SELECT DISTINCT idkegiatan FROM renja_subkegiatan "
            "  WHERE id_sub_pd = :opd_id AND tahun = :tahun) "
            "ORDER BY ri.nomor"
        ).bindparams(opd_id=opd_id, tahun=tahun)
    ).all()

    subkegiatan = [
        {
            "idsubkegiatan": str(s.idsubkegiatan),
            "idprogram": str(s.idprogram),
            "idkegiatan": str(s.idkegiatan),
            "kode_sub_kegiatan": s.kode_sub_kegiatan,
            "nm_program": s.nm_program,
            "nm_kegiatan": s.nm_kegiatan,
            "nm_sub_kegiatan": s.nm_sub_kegiatan,
            "indikator": "; ".join(by_sub.get(str(s.idsubkegiatan), [])),
            "indikator_list": by_sub_list.get(str(s.idsubkegiatan), []),
        }
        for s in subs
    ]
    indikator_program = [
        {
            "id": str(r.id),
            "idprogram": str(r.id_parent),
            "nm_program": prog_nama.get(str(r.id_parent)),
            "label": _label(r.tolok_ukur, r.satuan, r.target),
            "tolok": r.tolok_ukur,
            "target": _tgt(r.target, r.satuan),
        }
        for r in ind_prog
        if r.tolok_ukur
    ]
    indikator_kegiatan = [
        {
            "id": str(r.id),
            "idkegiatan": str(r.id_parent),
            "idprogram": keg_prog.get(str(r.id_parent)),
            "nm_program": prog_nama.get(keg_prog.get(str(r.id_parent))),
            "nm_kegiatan": keg_nama.get(str(r.id_parent)),
            "label": _label(r.tolok_ukur, r.satuan, r.target),
            "tolok": r.tolok_ukur,
            "target": _tgt(r.target, r.satuan),
        }
        for r in ind_keg
        if r.tolok_ukur
    ]
    return {
        "subkegiatan": subkegiatan,
        "indikator_program": indikator_program,
        "indikator_kegiatan": indikator_kegiatan,
    }


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
