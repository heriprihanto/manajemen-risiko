"""Analisis risiko (Form 4), matriks risiko, dan penentuan prioritas (Form 5).

Skala risiko = skala dampak (1..4) x skala kemungkinan (1..4)  ->  1..16.
Level (band) mengikuti matriks analisis risiko 4x4 SPIP:
    Rendah        : skala 1-3   (risiko dapat diterima)
    Sedang        : skala 4-6
    Tinggi        : skala 8-9   (tidak dapat diterima / penanganan selanjutnya)
    Sangat Tinggi : skala 12-16 (penanganan prioritas)

Catatan Form 4: risiko yang menjadi prioritas (masuk Form 5 / dibuatkan RTP) adalah
yang skala risikonya > 4 (yaitu 6, 8, 9, 12, 16).
"""

DAMPAK_LABEL = {
    1: "Tidak Signifikan",
    2: "Kurang Signifikan",
    3: "Signifikan",
    4: "Sangat Signifikan",
}
KEMUNGKINAN_LABEL = {
    1: "Sangat Jarang",
    2: "Kemungkinan Kecil",
    3: "Kemungkinan Besar",
    4: "Hampir Pasti",
}

LEVEL_RENDAH = "Rendah"
LEVEL_SEDANG = "Sedang"
LEVEL_TINGGI = "Tinggi"
LEVEL_SANGAT_TINGGI = "Sangat Tinggi"

PRIORITAS_THRESHOLD = 4  # skala > 4 -> prioritas


def hitung_skala(dampak: int | None, kemungkinan: int | None) -> float | None:
    if dampak is None or kemungkinan is None:
        return None
    return float(dampak * kemungkinan)


def level_risiko(skala: float | None) -> str | None:
    if skala is None:
        return None
    if skala >= 12:
        return LEVEL_SANGAT_TINGGI
    if skala >= 8:
        return LEVEL_TINGGI
    if skala >= 4:
        return LEVEL_SEDANG
    return LEVEL_RENDAH


def warna_level(level: str | None) -> str:
    return {
        LEVEL_RENDAH: "#22c55e",
        LEVEL_SEDANG: "#eab308",
        LEVEL_TINGGI: "#f97316",
        LEVEL_SANGAT_TINGGI: "#ef4444",
    }.get(level, "#9ca3af")


def is_prioritas_default(skala: float | None) -> bool:
    return skala is not None and skala > PRIORITAS_THRESHOLD


def keterangan_penanganan(level: str | None) -> str:
    return {
        LEVEL_RENDAH: "Risiko dapat diterima",
        LEVEL_SEDANG: "Risiko tidak dapat diterima / penanganan selanjutnya",
        LEVEL_TINGGI: "Risiko tidak dapat diterima / penanganan selanjutnya",
        LEVEL_SANGAT_TINGGI: "Risiko tidak dapat diterima / penanganan prioritas",
    }.get(level, "")
