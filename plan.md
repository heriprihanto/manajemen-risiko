Buat Web App Manajemen Risiko
backend : python, fastapi, sqlalchemy, sqlmodel
database : postgresql, configurasi di @BackEnd/.env
frontend : VueJS, PrimeVue
Transform file Excel @Kertas Kerja Manajemen Risiko.xls menjadi aplikasi manajemen risiko
Sheet Form 1.a CEE persepsi merupakan hasil kuisioner ( sheet KUISIONER), koolom R1, R2 - R29 dinamis merupakan nilai hasil kuisioner,
sheet lainnya saling terhubung satu sama lain
data per OPD (Organisasi Perangkat Daerah), sudah ada tabel ta_opd di database


buat Authentifikasi, Login dengan JWT
sudah ada tabel sso_users untuk data pengguna
login menggunakan query SELECT * FROM public.sso_users u WHERE u.username = :username  AND password = encode_passwd(:username, :password)
field role_id merupakan role pengguna 1 Admin, 4 OPD
field opds merupakan array dari id OPD, karena satu pengguna bisa lebih dari satu OPD

Halaman Form 2.b — Konteks Strategis OPD
Form Entri :
Field Tujuan pilih dari tabel renstra_tujuan
Field Sasaran pilih dari tabel renstra_sasaran
Field Program pilih dari tabel renstra_program

Halaman Form 2.b — Konteks Strategis OPD
Form Entri :
field periode dinilai pilih dari tabel renstra_tahap

Halaman Form 2.b — Konteks Strategis OPD
Form Entri :
field IKU Renstra pilih dari tabel renstra_indikator_tujuan_sasaran where iku=1

Halaman Form 2.b — Konteks Strategis OPD
hapus field Urusan Pemerintahan
Penetapan Konteks (T/S/IKU/Program)

Printout cetak seperti contoh PDF
perhatikan blok warna hijau, adalah semua yang ada di tabel renstra
blok kuning hanya data yang dientri di Form 2.b — Konteks Strategis OPD
Bidang urusan dari field bidang_urusan tabel ta_opd


Revisi printout Form 2.b — Konteks Strategis OPD :
Tujuan Strategis, Sasaran Strategis, IKU Renstra OPD, Program adalah semua data yang ada di tabel renstra
"Tujuan, Sasaran, IKU dan Program yang akan dilakukan penilaian risiko" adalah data yang dientri di Form 2.b — Konteks Strategis OPD


Revisi printout Form 2.b — Konteks Strategis OPD :
Kolom "Tujuan, Sasaran, IKU dan Program yang akan dilakukan penilaian risiko" adalah data yang hanya dientri di Form 2.b — Konteks Strategis OPD bukan semua data yang ada di renstra

Revisi Entri Form 2.c — Konteks Operasional OPD
hanya memilih indikator pada tabel renja_indikator, centang subkegiatan yang dipilih yang akan dilakukan penilaian risiko
renja_indikator berelasi dengan tabel renja_subkegiatan dengan id_parent = idsubkegiatan

Revisi Entri Form 2.c — Konteks Operasional OPD
indikator kegiatan bisa dicentang sebagai  indikator yang dipilih yang akan dilakukan penilaian risiko
renja_indikator berelasi dengan tabel renja_subkegiatan dengan id_parent = idkegiatan


Pisahkan Form 3.a, 3.b, 3.c menjadi menu tersendiri jangan digabung


Form 3.b — Identifikasi Risiko Strategis OPD
menggunakan data dari Form 2.b — Konteks Strategis OPD, pengguna hanya melengkapi :
Risiko :
- Uraian Risiko
- Kode Risiko
- Pemilik Risiko

Sebab :
- Uraian 
- Sumber : Internal, Eksternal, Internal / Eksternal
- C/ UC

Dampak :
- Uraian
- Pihak yang Terkena

Form 3.b — Identifikasi Risiko Strategis OPD :
pilihan Tujuan/Sasaran/IKU/Program tambahkan data dari indikator program pada Form 2.c — Konteks Operasional OPD

Form 3.c — Identifikasi Risiko Operasional OPD
data dari pilihan indikator subkegiatan yang dipilih pada Form 2.c — Konteks Operasional OPD

Form 3.c — Identifikasi Risiko Operasional OPD
field tahap dibuat select : Pelaksanaan, Pertanggungjawaban


Form 3.c — Identifikasi Risiko Operasional OPD
field kode risiko dibuat otomatis dengan format :
RSO.


Pemilik / Penanggug jawab yang sudah dientri di Form 3.b — Identifikasi Risiko Strategis OPD akan tersimpan selalu sama untuk Form selanjutnya


Print Out / cetak Form 9, tambahkan grouping by jenis risiko


Print Out / cetak Form 10, tambahkan grouping by jenis risiko

Buat menu (hanya untuk admin) untuk manajemen daftar pertanyaan yang akan dipublish untuk kuisioner 
tambahkan chaptcha pada login

sidebar menu, background dengan gradasi

text pada sidebar menu lebih kontras dengan background supaya lebih jelas terbaca

