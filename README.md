# Web App Manajemen Risiko — Pemerintah Kota Tegal

Aplikasi penyelenggaraan **Manajemen Risiko SPIP**, hasil transformasi dari
`Kertas Kerja Manajemen Risiko.xls` menjadi aplikasi web per OPD (Organisasi
Perangkat Daerah).

- **Backend**: Python · FastAPI · SQLModel/SQLAlchemy · PostgreSQL
- **Frontend**: Vue 3 · PrimeVue (Vite)
- **Data**: per OPD (`ta_opd`) dan per Tahun Penilaian

## Alur / Form yang didukung

| Menu | Sumber Excel | Keterangan |
|------|--------------|-----------|
| Dashboard | — | Ringkasan responden, jumlah & level risiko, prioritas |
| Form 1.a Kuesioner | `Form 1.a CEE persepsi` + `KUESIONER` | Input responden **R1..Rn dinamis** & jawaban 1–4, **modus** & simpulan otomatis |
| Form 1.b Reviu Dokumen | `Form 1.b` | Penilaian Memadai/Kurang Memadai per aspek |
| Form 1.c Simpulan CEE | `Form 1.c` | Gabungan persepsi + dokumen (otomatis) |
| Form 6 RTP atas CEE | `Form 6 RTP CE` | Rencana tindak pengendalian lingkungan |
| Form 2.a/2.b/2.c Konteks | `Form 2a/2b/2c` | Konteks strategis Pemda / strategis OPD / operasional OPD |
| Form 3 Identifikasi | `Form 3a/3b/3c` | Identifikasi risiko strategis Pemda, strategis OPD, operasional OPD |
| Form 4 Analisis | `Form 4` | Skala dampak × kemungkinan → skala & level risiko |
| Matriks Risiko | `Matrik Risiko` | Heatmap 4×4 sebaran risiko |
| Form 5 Prioritas | `Form 5` | Daftar risiko prioritas (skala > 4) — otomatis |
| Form 7 RTP Risiko | `Form 7` | RTP atas risiko prioritas |
| Form 8 Info & Komunikasi | `Form 8` | Pengkomunikasian pengendalian |
| Form 9 Rencana Pemantauan | `Form 9` | Pemantauan kegiatan pengendalian |
| Form 10 Monitoring Event | `Form 10` | Pencatatan kejadian risiko & realisasi RTP |
| Cetak Laporan | semua | Print preview / cetak ke PDF, pilih form |
| **Survei Publik** (`/survei`) | `Form 1.a` | Form kuesioner CEE untuk pegawai, login Google (Firebase) |

## Survei Publik (Login Google / Firebase)

Halaman `/survei` adalah form publik tanpa shell admin. Pegawai **masuk dengan akun
Google** (Firebase Authentication), memilih OPD, lalu mengisi 37 pertanyaan CEE.
Jawaban tersimpan sebagai responden (`R1..Rn`) pada Form 1.a OPD bersangkutan — satu
submission per akun Google (kirim ulang memperbarui jawaban).

- **Frontend**: `src/firebase.js` (config project `manajemen-risiko-98127`), `src/views/Survei.vue`.
- **Backend**: `app/routers/survei.py` + `app/services/firebase_auth.py` — memverifikasi
  Firebase ID token via Google JWKS (RS256), **tanpa service account**. Project ID di
  `FIREBASE_PROJECT_ID` (config).

> **Aktivasi sekali di Firebase Console**: Authentication → Sign-in method → aktifkan
> **Google**; pastikan domain (`localhost`, domain produksi) ada di *Authorized domains*.
> Bagikan tautan `/survei` ke pegawai (tombol "Buka Survei Publik" ada di sidebar admin).

### Logika perhitungan utama
- **Simpulan kuesioner**: simpulan pertanyaan *Memadai* bila **modus** jawaban 3/4,
  *Kurang Memadai* bila 1/2. Sub-unsur *Memadai* bila seluruh pertanyaannya Memadai.
- **Skala risiko** = skala dampak (1–4) × skala kemungkinan (1–4). Level: Rendah (1–3),
  Sedang (4–6), Tinggi (8–9), Sangat Tinggi (12–16). Risiko **prioritas** bila skala > 4.

## Menjalankan

### 1. Backend (port 8077)
Konfigurasi database ada di `BackEnd/.env` (target: `db_manajemen_risiko`).

```bash
cd BackEnd
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python init_db.py     # buat tabel + seed kuesioner + salin ta_opd (sekali saja)
./run.sh                        # atau: .venv/bin/uvicorn app.main:app --reload --port 8077
```
Dokumentasi API: http://localhost:8077/docs

> `init_db.py` menyalin master OPD dari database `manajemen_risiko` (server yang sama)
> bila tabel `ta_opd` di database target masih kosong.

### 2. Frontend (port 5173)
```bash
cd FrontEnd
npm install
npm run dev
```
Buka http://localhost:5173 — pilih **OPD** dan **Tahun** di kanan atas; seluruh form
mengikuti konteks tersebut. Vite mem-proxy `/api` ke backend `:8077`.

## Struktur
```
BackEnd/
  app/
    core/config.py        # baca .env
    db.py                 # engine + session
    models/               # SQLModel: master, cee, konteks, risiko, monitoring
    services/             # cee.py (modus/simpulan), analisis.py (skala/level/matriks)
    routers/              # master, cee, konteks, risiko, monitoring, dashboard
    seed_data.py          # 8 kategori + 37 pertanyaan CEE (dari Excel)
  init_db.py
FrontEnd/
  src/
    stores/context.js     # OPD + Tahun aktif (persist localStorage)
    components/CrudTable.vue
    views/                # Dashboard + Form1a..Form10, Matriks
```
