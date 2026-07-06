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