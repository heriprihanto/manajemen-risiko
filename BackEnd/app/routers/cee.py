"""Form 1.a (kuesioner persepsi), 1.b (reviu dokumen), 1.c (simpulan), Form 6 (RTP CEE)."""
from datetime import datetime
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session, select

from app.core.security import AdminDep, UserDep, guard_record
from app.db import get_session
from app.models import (
    CeeDokumenItem,
    CeeDokumenKelemahan,
    CeeDokumenNilai,
    CeeJawaban,
    CeeResponden,
    CeeSimpulan,
    KuesionerKategori,
    KuesionerPertanyaan,
    RtpCee,
)
from app.routers.crud_helper import make_opd_tahun_router
from app.services import cee as svc

router = APIRouter(prefix="/cee", tags=["cee"])


# ----------------------------- Form 1.a: Responden ----------------------------
@router.get("/responden")
def list_responden(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    return session.exec(
        select(CeeResponden)
        .where(CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun)
        .order_by(CeeResponden.id)
    ).all()


def _next_kode(session: Session, opd_id: int, tahun: int) -> str:
    existing = session.exec(
        select(CeeResponden.kode_responden).where(
            CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun
        )
    ).all()
    nums = []
    for k in existing:
        if k and k.upper().startswith("R") and k[1:].isdigit():
            nums.append(int(k[1:]))
    return f"R{(max(nums) + 1) if nums else 1}"


@router.post("/responden")
def create_responden(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    opd_id, tahun = payload["opd_id"], payload["tahun"]
    kode = payload.get("kode_responden") or _next_kode(session, opd_id, tahun)
    obj = CeeResponden(
        opd_id=opd_id,
        tahun=tahun,
        kode_responden=kode,
        nama_responden=payload.get("nama_responden"),
        jabatan=payload.get("jabatan"),
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put("/responden/{rid}")
def update_responden(
    rid: int,
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    obj = guard_record(user, session.get(CeeResponden, rid), "Responden")
    for f in ("kode_responden", "nama_responden", "jabatan"):
        if f in payload:
            setattr(obj, f, payload[f])
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/responden/{rid}")
def delete_responden(
    rid: int, session: Session = Depends(get_session), user: dict = UserDep
):
    obj = guard_record(user, session.get(CeeResponden, rid), "Responden")
    for j in session.exec(select(CeeJawaban).where(CeeJawaban.responden_id == rid)).all():
        session.delete(j)
    session.delete(obj)
    session.commit()
    return {"ok": True}


# ----------------------------- Form 1.a: Jawaban ------------------------------
@router.post("/jawaban")
def save_jawaban(
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    """Simpan/replace satu sel jawaban (responden x pertanyaan)."""
    rid = payload["responden_id"]
    guard_record(user, session.get(CeeResponden, rid), "Responden")
    pid = payload["pertanyaan_id"]
    nilai = payload.get("nilai")
    existing = session.exec(
        select(CeeJawaban).where(
            CeeJawaban.responden_id == rid, CeeJawaban.pertanyaan_id == pid
        )
    ).first()
    if nilai in (None, ""):
        if existing:
            session.delete(existing)
            session.commit()
        return {"ok": True, "deleted": True}
    if existing:
        existing.nilai = int(nilai)
        session.add(existing)
    else:
        session.add(CeeJawaban(responden_id=rid, pertanyaan_id=pid, nilai=int(nilai)))
    session.commit()
    return {"ok": True}


# ----------------------- Form 1.a: Matriks + simpulan -------------------------
@router.get("/form1a")
def form_1a(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Rekap kuesioner: responden (kolom R1..Rn), jawaban, modus & simpulan per
    pertanyaan dan per sub-unsur (persepsi)."""
    responden = session.exec(
        select(CeeResponden)
        .where(CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun)
        .order_by(CeeResponden.id)
    ).all()
    rid_list = [r.id for r in responden]

    jawaban_map: dict[tuple[int, int], int] = {}
    if rid_list:
        for j in session.exec(
            select(CeeJawaban).where(CeeJawaban.responden_id.in_(rid_list))
        ).all():
            jawaban_map[(j.pertanyaan_id, j.responden_id)] = j.nilai

    kats = session.exec(
        select(KuesionerKategori).order_by(KuesionerKategori.urutan)
    ).all()
    pers = session.exec(
        select(KuesionerPertanyaan)
        .where(KuesionerPertanyaan.aktif == 1)
        .order_by(KuesionerPertanyaan.urutan)
    ).all()
    per_by_kat: dict[int, list[KuesionerPertanyaan]] = {}
    for p in pers:
        per_by_kat.setdefault(p.kategori_id, []).append(p)

    kategori_out = []
    for k in kats:
        pert_out = []
        predikat_list = []
        for p in per_by_kat.get(k.id, []):
            nilai_per_responden = {
                r.id: jawaban_map.get((p.id, r.id)) for r in responden
            }
            md = svc.modus(list(nilai_per_responden.values()))
            pred = svc.predikat_dari_nilai(md)
            predikat_list.append(pred)
            pert_out.append(
                {
                    "id": p.id,
                    "nomor": p.nomor,
                    "pertanyaan": p.pertanyaan,
                    "jawaban": nilai_per_responden,
                    "modus": md,
                    "simpulan": pred,
                }
            )
        kategori_out.append(
            {
                "id": k.id,
                "kode": k.kode,
                "nama": k.nama,
                "simpulan": svc.simpulan_subunsur(predikat_list),
                "pertanyaan": pert_out,
            }
        )

    return {
        "opd_id": opd_id,
        "tahun": tahun,
        "responden": responden,
        "kategori": kategori_out,
    }


# ------------------- Rincian hasil survei (per responden) ---------------------
@router.get("/survei-hasil")
def survei_hasil(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Rincian hasil survei: tiap responden beserta identitas & jawaban per
    pertanyaan (untuk menu admin 'Rincian Hasil Survei')."""
    responden = session.exec(
        select(CeeResponden)
        .where(CeeResponden.opd_id == opd_id, CeeResponden.tahun == tahun)
        .order_by(CeeResponden.id)
    ).all()
    rid_list = [r.id for r in responden]

    jawaban_by_resp: dict[int, dict[int, int]] = {}
    if rid_list:
        for j in session.exec(
            select(CeeJawaban).where(CeeJawaban.responden_id.in_(rid_list))
        ).all():
            jawaban_by_resp.setdefault(j.responden_id, {})[j.pertanyaan_id] = j.nilai

    kats = session.exec(
        select(KuesionerKategori).order_by(KuesionerKategori.urutan)
    ).all()
    pers = session.exec(
        select(KuesionerPertanyaan)
        .where(KuesionerPertanyaan.aktif == 1)
        .order_by(KuesionerPertanyaan.urutan)
    ).all()
    per_by_kat: dict[int, list[KuesionerPertanyaan]] = {}
    for p in pers:
        per_by_kat.setdefault(p.kategori_id, []).append(p)
    kategori_out = [
        {
            "id": k.id,
            "kode": k.kode,
            "nama": k.nama,
            "pertanyaan": [
                {"id": p.id, "nomor": p.nomor, "pertanyaan": p.pertanyaan}
                for p in per_by_kat.get(k.id, [])
            ],
        }
        for k in kats
    ]

    resp_out = []
    for r in responden:
        jw = jawaban_by_resp.get(r.id, {})
        nilai_list = [v for v in jw.values() if v is not None]
        rata = round(sum(nilai_list) / len(nilai_list), 2) if nilai_list else None
        resp_out.append(
            {
                "id": r.id,
                "kode_responden": r.kode_responden,
                "nama_responden": r.nama_responden,
                "jabatan": r.jabatan,
                "email": r.email,
                "sumber": r.sumber,
                "submitted_at": r.updated_at.isoformat() if r.updated_at else None,
                "jawaban": {str(pid): nilai for pid, nilai in jw.items()},
                "jumlah_jawaban": len(nilai_list),
                "rata_rata": rata,
            }
        )

    return {
        "opd_id": opd_id,
        "tahun": tahun,
        "total_pertanyaan": len(pers),
        "kategori": kategori_out,
        "responden": resp_out,
    }


@router.delete("/survei-hasil/{rid}")
def delete_survei_hasil(
    rid: int, session: Session = Depends(get_session), user: dict = AdminDep
):
    """Hapus satu hasil survei (responden + jawaban). Khusus Admin."""
    obj = session.get(CeeResponden, rid)
    if obj is None:
        raise HTTPException(404, "Responden tidak ditemukan")
    for j in session.exec(select(CeeJawaban).where(CeeJawaban.responden_id == rid)).all():
        session.delete(j)
    session.delete(obj)
    session.commit()
    return {"ok": True}


# --------------------------- Form 1.b: Reviu dokumen --------------------------
@router.get("/form1b")
def form_1b(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    items = session.exec(select(CeeDokumenItem).order_by(CeeDokumenItem.urutan)).all()
    nilai = {
        n.item_id: n
        for n in session.exec(
            select(CeeDokumenNilai).where(
                CeeDokumenNilai.opd_id == opd_id, CeeDokumenNilai.tahun == tahun
            )
        ).all()
    }
    # Uraian kelemahan (boleh >1 per aspek), dikelompokkan per item.
    kelemahan: dict[int, list[CeeDokumenKelemahan]] = {}
    for k in session.exec(
        select(CeeDokumenKelemahan)
        .where(
            CeeDokumenKelemahan.opd_id == opd_id,
            CeeDokumenKelemahan.tahun == tahun,
        )
        .order_by(CeeDokumenKelemahan.urutan, CeeDokumenKelemahan.id)
    ).all():
        kelemahan.setdefault(k.item_id, []).append(k)

    out = []
    for it in items:
        n = nilai.get(it.id)
        ks = kelemahan.get(it.id, [])
        # keterangan gabungan (baris per uraian) untuk Form 1.c & Laporan.
        gabungan = "\n".join(k.uraian for k in ks) or (n.keterangan if n else None)
        out.append(
            {
                "item_id": it.id,
                "nomor": it.nomor,
                "aspek": it.aspek,
                "nilai": n.nilai if n else None,
                "sumber_data": n.sumber_data if n else None,
                "keterangan": gabungan,
                "kelemahan": [
                    {"id": k.id, "uraian": k.uraian, "urutan": k.urutan} for k in ks
                ],
                "simpulan": svc.predikat_dokumen(n.nilai if n else None),
            }
        )
    return out


@router.post("/form1b")
def save_1b(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    opd_id, tahun, item_id = payload["opd_id"], payload["tahun"], payload["item_id"]
    obj = session.exec(
        select(CeeDokumenNilai).where(
            CeeDokumenNilai.opd_id == opd_id,
            CeeDokumenNilai.tahun == tahun,
            CeeDokumenNilai.item_id == item_id,
        )
    ).first()
    if not obj:
        obj = CeeDokumenNilai(opd_id=opd_id, tahun=tahun, item_id=item_id)
    obj.nilai = payload.get("nilai")
    if "sumber_data" in payload:
        obj.sumber_data = payload.get("sumber_data")
    if "keterangan" in payload:  # uraian kelemahan kini di tabel terpisah
        obj.keterangan = payload.get("keterangan")
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    return {"ok": True}


# --------- Form 1.b: Uraian kelemahan (boleh lebih dari satu per aspek) -------
@router.post("/form1b/kelemahan")
def add_kelemahan(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    obj = CeeDokumenKelemahan(
        opd_id=payload["opd_id"],
        tahun=payload["tahun"],
        item_id=payload["item_id"],
        uraian=(payload.get("uraian") or "").strip(),
        urutan=payload.get("urutan") or 0,
    )
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.put("/form1b/kelemahan/{kid}")
def update_kelemahan(
    kid: int,
    payload: dict[str, Any] = Body(...),
    session: Session = Depends(get_session),
    user: dict = UserDep,
):
    obj = guard_record(user, session.get(CeeDokumenKelemahan, kid), "Uraian kelemahan")
    if "uraian" in payload:
        obj.uraian = (payload.get("uraian") or "").strip()
    if "urutan" in payload:
        obj.urutan = payload["urutan"]
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


@router.delete("/form1b/kelemahan/{kid}")
def delete_kelemahan(
    kid: int, session: Session = Depends(get_session), user: dict = UserDep
):
    obj = guard_record(user, session.get(CeeDokumenKelemahan, kid), "Uraian kelemahan")
    session.delete(obj)
    session.commit()
    return {"ok": True}


# ------------------------------ Form 1.c: Simpulan ----------------------------
@router.get("/form1c")
def form_1c(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Gabungan simpulan persepsi (1.a) + reviu dokumen (1.b) per sub-unsur."""
    f1a = form_1a(opd_id, tahun, session)
    f1b = {row["aspek"]: row for row in form_1b(opd_id, tahun, session)}

    # Override simpulan manual (bila admin/OPD menyunting) per sub-unsur.
    override = {
        s.kategori_id: s.predikat
        for s in session.exec(
            select(CeeSimpulan).where(
                CeeSimpulan.opd_id == opd_id, CeeSimpulan.tahun == tahun
            )
        ).all()
    }

    out = []
    for idx, kat in enumerate(f1a["kategori"], start=1):
        persepsi = kat["simpulan"]
        dok = f1b.get(kat["nama"])
        dokumen = dok["simpulan"] if dok else None
        simpulan_auto = svc.simpulan_gabungan(persepsi, dokumen)
        manual = override.get(kat["id"])
        out.append(
            {
                "no": idx,
                "kategori_id": kat["id"],
                "sub_unsur": kat["nama"],
                "hasil_persepsi": persepsi,
                "hasil_dokumen": dokumen,
                "uraian_dokumen": (dok or {}).get("keterangan"),
                "kelemahan": (dok or {}).get("kelemahan", []),
                "simpulan_auto": simpulan_auto,
                "simpulan_manual": manual is not None,
                "simpulan": manual if manual is not None else simpulan_auto,
            }
        )
    return out


@router.post("/form1c/simpulan")
def save_simpulan(
    payload: dict[str, Any] = Body(...), session: Session = Depends(get_session)
):
    """Simpan/override simpulan Form 1.c per sub-unsur. Kosong = kembali otomatis."""
    opd_id, tahun = payload["opd_id"], payload["tahun"]
    kategori_id = payload["kategori_id"]
    simpulan = (payload.get("simpulan") or "").strip() or None

    obj = session.exec(
        select(CeeSimpulan).where(
            CeeSimpulan.opd_id == opd_id,
            CeeSimpulan.tahun == tahun,
            CeeSimpulan.kategori_id == kategori_id,
        )
    ).first()
    if simpulan is None:
        if obj:
            session.delete(obj)
            session.commit()
        return {"ok": True, "simpulan_manual": False}
    if not obj:
        obj = CeeSimpulan(opd_id=opd_id, tahun=tahun, kategori_id=kategori_id)
    obj.predikat = simpulan
    obj.updated_at = datetime.utcnow()
    session.add(obj)
    session.commit()
    return {"ok": True, "simpulan_manual": True}


@router.get("/form1c/aspek")
def form1c_aspek(opd_id: int, tahun: int, session: Session = Depends(get_session)):
    """Opsi Aspek/Sub-unsur CEE (Form 6) dari Form 1.c: sub-unsur yang Kurang
    Memadai atau memiliki uraian permasalahan. Kurang Memadai tampil lebih dulu."""
    seen: dict[str, bool] = {}
    for r in form_1c(opd_id, tahun, session):
        km = r["simpulan"] == svc.KURANG
        if r["kelemahan"] or km:
            seen[r["sub_unsur"]] = seen.get(r["sub_unsur"], False) or km
    out = [{"label": k, "value": k, "kurang_memadai": v} for k, v in seen.items()]
    out.sort(key=lambda o: not o["kurang_memadai"])
    return out


@router.get("/form1c/permasalahan")
def form1c_permasalahan(
    opd_id: int, tahun: int, session: Session = Depends(get_session)
):
    """Opsi 'uraian permasalahan' dari Form 1.c untuk mengisi Kondisi Kurang
    Memadai di Form 6. Tiap opsi membawa aspek_cee (untuk cascading)."""
    out = []
    for r in form_1c(opd_id, tahun, session):
        for k in r["kelemahan"]:
            out.append(
                {
                    "label": k["uraian"],
                    "value": k["uraian"],
                    "aspek_cee": r["sub_unsur"],
                    "kurang_memadai": r["simpulan"] == svc.KURANG,
                }
            )
    out.sort(key=lambda o: not o["kurang_memadai"])
    return out


# ------------------------------- Form 6: RTP CEE ------------------------------
rtp_cee_router = make_opd_tahun_router(
    model=RtpCee, prefix="/rtp-cee", tag="cee", order_by="no_urut"
)
router.include_router(rtp_cee_router)
