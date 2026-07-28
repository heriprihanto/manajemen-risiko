"""Ekspor laporan ke Excel (.xlsx) — isi & tampilan mengikuti Cetak Laporan."""
from urllib.parse import quote

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.db import get_session
from app.services.excel_laporan import SECTION_KEYS, build_workbook

router = APIRouter(prefix="/laporan", tags=["laporan"])

XLSX_MIME = (
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)


@router.get("/excel")
def export_excel(
    opd_id: int,
    tahun: int,
    forms: str | None = None,
    session: Session = Depends(get_session),
):
    """Unduh laporan sebagai workbook: satu sheet per form.

    `forms` = daftar kunci bagian dipisah koma (mis. `f3a,f3b`); kosong = semua.
    """
    keys = [k.strip() for k in (forms or "").split(",") if k.strip()]
    unknown = [k for k in keys if k not in SECTION_KEYS]
    if unknown:
        raise HTTPException(400, f"Form tidak dikenal: {', '.join(unknown)}")

    buf = build_workbook(session, opd_id, tahun, keys or None)
    nama = f"Laporan Manajemen Risiko {tahun}.xlsx"
    return StreamingResponse(
        buf,
        media_type=XLSX_MIME,
        headers={
            "Content-Disposition": (
                f"attachment; filename*=UTF-8''{quote(nama)}"
            )
        },
    )
