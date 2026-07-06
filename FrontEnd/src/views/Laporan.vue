<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import MultiSelect from 'primevue/multiselect'
import Button from 'primevue/button'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const route = useRoute()
const loading = ref(true)
const d = ref({})

const sections = [
  { key: 'f1a', form: 'Form 1.a', label: 'Rekap Kuesioner CEE (Persepsi)' },
  { key: 'f1b', form: 'Form 1.b', label: 'Reviu Dokumen CEE' },
  { key: 'f1c', form: 'Form 1.c', label: 'Simpulan CEE' },
  { key: 'f6', form: 'Form 6', label: 'RTP atas CEE' },
  { key: 'f2a', form: 'Form 2.a', label: 'Konteks Strategis Pemda' },
  { key: 'f2b', form: 'Form 2.b', label: 'Konteks Strategis OPD' },
  { key: 'f2c', form: 'Form 2.c', label: 'Konteks Operasional OPD' },
  { key: 'f3', form: 'Form 3', label: 'Identifikasi Risiko' },
  { key: 'f4', form: 'Form 4', label: 'Analisis Risiko' },
  { key: 'f5', form: 'Form 5', label: 'Daftar Risiko Prioritas' },
  { key: 'f7', form: 'Form 7', label: 'RTP atas Risiko' },
  { key: 'f8', form: 'Form 8', label: 'Informasi & Komunikasi' },
  { key: 'f9', form: 'Form 9', label: 'Rencana Pemantauan PI' },
  { key: 'f10', form: 'Form 10', label: 'Monitoring Risk Event & RTP' },
]
// Bila dibuka dari tombol "Cetak" sebuah modul (?form=<key>), batasi laporan
// ke satu bagian saja; jika tidak, tampilkan semua bagian.
const initialForm = String(route.query.form || '')
const selected = ref(
  sections.some((s) => s.key === initialForm) ? [initialForm] : sections.map((s) => s.key),
)
const isSel = (k) => selected.value.includes(k)
const opdName = computed(() => ctx.opd?.nama_pd || '-')

// Form 6 dikelompokkan per Aspek/Sub-unsur CEE.
const f6Grouped = computed(() => {
  const groups = {}
  for (const r of d.value.f6 || []) {
    const key = r.aspek_cee || '(Tanpa Sub-unsur)'
    ;(groups[key] ||= []).push(r)
  }
  return Object.entries(groups).map(([aspek, items]) => ({ aspek, items }))
})

const jenisLabel = {
  strategis_pemda: 'Risiko Strategis Pemda (Form 3.a)',
  strategis_opd: 'Risiko Strategis OPD (Form 3.b)',
  operasional_opd: 'Risiko Operasional OPD (Form 3.c)',
}
const levelColor = { Rendah: '#22c55e', Sedang: '#eab308', Tinggi: '#f97316', 'Sangat Tinggi': '#ef4444' }

async function load() {
  loading.value = true
  const p = { opd_id: ctx.opdId, tahun: ctx.tahun }
  const g = (url, params = p) => api.get(url, { params }).then((r) => r.data).catch(() => null)
  const [f1a, f1b, f1c, f6, f2a, f2b, f2c, f4, matriks, f5, f7, f8, f9, f10] = await Promise.all([
    g('/cee/form1a'), g('/cee/form1b'), g('/cee/form1c'), g('/cee/rtp-cee'),
    g('/konteks/pemda', { tahun: ctx.tahun }), g('/konteks/strategis-opd'), g('/konteks/operasional-opd'),
    g('/risiko/form4'), g('/risiko/matriks'), g('/risiko/form5'), g('/risiko/rtp'),
    g('/monitoring/infokom'), g('/monitoring/pi'), g('/monitoring/risk-event'),
  ])
  d.value = { f1a, f1b, f1c, f6, f2a, f2b, f2c, f4, matriks, f5, f7, f8, f9, f10 }
  loading.value = false
}
function cetak() {
  window.print()
}
onMounted(async () => {
  await load()
  // Auto-cetak saat dibuka via tombol Cetak modul (?print=1).
  if (route.query.print) {
    await nextTick()
    setTimeout(() => window.print(), 300)
  }
})
</script>

<template>
  <div class="no-print toolbar">
    <MultiSelect
      v-model="selected"
      :options="sections"
      optionLabel="label"
      optionValue="key"
      display="chip"
      placeholder="Pilih form"
      style="max-width: 640px"
    >
      <template #option="{ option }">{{ option.form }} — {{ option.label }}</template>
    </MultiSelect>
    <div class="spacer" />
    <Button label="Cetak / Print Preview" icon="pi pi-print" @click="cetak" :disabled="loading" />
  </div>

  <div v-if="loading" class="muted">Memuat data laporan…</div>

  <div v-else class="report-sheet">
    <!-- ============ Form 1.a ============ -->
    <section v-if="isSel('f1a') && d.f1a" class="report-section">
      <div class="report-formno">Form 1.a</div>
      <div class="report-title">Rekapitulasi Hasil Kuesioner Penilaian Lingkungan Pengendalian (CEE)</div>
      <div class="report-subtitle">{{ opdName }} — Tahun Penilaian {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead>
          <tr>
            <th rowspan="2" style="width: 28px">No</th>
            <th rowspan="2">Pertanyaan / Sub-unsur</th>
            <th :colspan="d.f1a.responden.length || 1">Jawaban Responden</th>
            <th rowspan="2" style="width: 48px">Modus</th>
            <th rowspan="2" style="width: 120px">Simpulan</th>
          </tr>
          <tr>
            <th v-for="r in d.f1a.responden" :key="r.id" style="width: 30px">{{ r.kode_responden }}</th>
            <th v-if="!d.f1a.responden.length">—</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="kat in d.f1a.kategori" :key="kat.id">
            <tr>
              <td class="c"><b>{{ kat.kode }}</b></td>
              <td :colspan="(d.f1a.responden.length || 1) + 2"><b>{{ kat.nama }}</b></td>
              <td class="c">{{ kat.simpulan }}</td>
            </tr>
            <tr v-for="(pq, i) in kat.pertanyaan" :key="pq.id">
              <td class="c">{{ i + 1 }}</td>
              <td>{{ pq.pertanyaan }}</td>
              <td v-for="r in d.f1a.responden" :key="r.id" class="c">{{ pq.jawaban[r.id] ?? '' }}</td>
              <td v-if="!d.f1a.responden.length" class="c"></td>
              <td class="c">{{ pq.modus ?? '' }}</td>
              <td class="c">{{ pq.simpulan ?? '' }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 1.b ============ -->
    <section v-if="isSel('f1b') && d.f1b" class="report-section">
      <div class="report-formno">Form 1.b</div>
      <div class="report-title">Simpulan CEE Berdasarkan Reviu Dokumen</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 40px">No</th><th>Sub-unsur / Aspek</th><th style="width: 130px">Hasil Reviu</th><th style="width: 180px">Sumber Data</th><th>Uraian Kelemahan</th></tr></thead>
        <tbody>
          <tr v-for="r in d.f1b" :key="r.item_id">
            <td class="c">{{ r.nomor }}</td><td>{{ r.aspek }}</td>
            <td class="c">{{ r.simpulan ?? '' }}</td>
            <td>{{ r.sumber_data }}</td>
            <td>
              <ol v-if="r.kelemahan && r.kelemahan.length" class="kelemahan-ol">
                <li v-for="k in r.kelemahan" :key="k.id">{{ k.uraian }}</li>
              </ol>
              <span v-else class="pre-line">{{ r.keterangan }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 1.c ============ -->
    <section v-if="isSel('f1c') && d.f1c" class="report-section">
      <div class="report-formno">Form 1.c</div>
      <div class="report-title">Simpulan Survei Persepsi atas Lingkungan Pengendalian Intern</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 36px">No</th><th>Sub-unsur</th><th style="width: 110px">Hasil Persepsi</th><th style="width: 110px">Hasil Dokumen</th><th style="width: 110px">Simpulan</th><th>Penjelasan</th></tr></thead>
        <tbody>
          <tr v-for="r in d.f1c" :key="r.kategori_id">
            <td class="c">{{ r.no }}</td><td>{{ r.sub_unsur }}</td>
            <td class="c">{{ r.hasil_persepsi }}</td><td class="c">{{ r.hasil_dokumen }}</td>
            <td class="c">{{ r.simpulan }}</td>
            <td>
              <ol v-if="r.kelemahan && r.kelemahan.length" class="kelemahan-ol">
                <li v-for="k in r.kelemahan" :key="k.id">{{ k.uraian }}</li>
              </ol>
              <span v-else class="pre-line">{{ r.uraian_dokumen }}</span>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 6 ============ -->
    <section v-if="isSel('f6')" class="report-section">
      <div class="report-formno">Form 6</div>
      <div class="report-title">Penilaian Kegiatan Pengendalian (RTP atas CEE)</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 36px">No</th><th>Kondisi Kurang Memadai</th><th>Rencana Tindak Pengendalian</th><th>Penanggung Jawab</th><th style="width: 90px">Target</th><th style="width: 90px">Realisasi</th></tr></thead>
        <tbody>
          <template v-for="g in f6Grouped" :key="g.aspek">
            <tr><td class="c"></td><td colspan="5"><b>{{ g.aspek }}</b></td></tr>
            <tr v-for="(r, i) in g.items" :key="r.id">
              <td class="c">{{ r.no_urut || i + 1 }}</td><td>{{ r.kondisi_kerentanan }}</td><td>{{ r.rencana_tindak }}</td>
              <td>{{ r.pemilik_penanggung_jawab }}</td><td>{{ r.target_waktu }}</td><td>{{ r.realisasi_waktu }}</td>
            </tr>
          </template>
          <tr v-if="!d.f6 || !d.f6.length"><td colspan="6" class="c">Belum ada data</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 2.a ============ -->
    <section v-if="isSel('f2a')" class="report-section">
      <div class="report-formno">Form 2.a</div>
      <div class="report-title">Penetapan Konteks Risiko Strategis Pemda</div>
      <div class="report-subtitle">Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <tbody v-if="d.f2a">
          <tr><th style="width: 280px; text-align: left">Visi</th><td>{{ d.f2a.visi }}</td></tr>
          <tr><th style="text-align: left">Misi Strategis</th><td>{{ d.f2a.misi_strategis }}</td></tr>
          <tr><th style="text-align: left">Tujuan Strategis RPD</th><td>{{ d.f2a.tujuan_strategis }}</td></tr>
          <tr><th style="text-align: left">Penetapan Konteks Tujuan</th><td>{{ d.f2a.penetapan_konteks_tujuan }}</td></tr>
          <tr><th style="text-align: left">Sasaran RPD</th><td>{{ d.f2a.sasaran_rpd }}</td></tr>
          <tr><th style="text-align: left">Penetapan Konteks Sasaran</th><td>{{ d.f2a.penetapan_konteks_sasaran }}</td></tr>
          <tr><th style="text-align: left">IKU Sasaran</th><td>{{ d.f2a.iku_sasaran }}</td></tr>
          <tr><th style="text-align: left">Urusan Pemerintahan</th><td>{{ d.f2a.urusan_pemerintahan }}</td></tr>
        </tbody>
        <tbody v-else><tr><td class="c">Belum ada data</td></tr></tbody>
      </table>
    </section>

    <!-- ============ Form 2.b ============ -->
    <section v-if="isSel('f2b')" class="report-section">
      <div class="report-formno">Form 2.b</div>
      <div class="report-title">Penetapan Konteks Risiko Strategis OPD</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th>Tujuan Strategis</th><th>Sasaran Strategis</th><th>IKU Renstra</th><th>Program</th><th>Urusan</th></tr></thead>
        <tbody>
          <tr v-for="r in d.f2b" :key="r.id"><td>{{ r.tujuan_strategis }}</td><td>{{ r.sasaran_strategis }}</td><td>{{ r.iku_renstra }}</td><td>{{ r.program }}</td><td>{{ r.urusan_pemerintahan }}</td></tr>
          <tr v-if="!d.f2b || !d.f2b.length"><td colspan="5" class="c">Belum ada data</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 2.c ============ -->
    <section v-if="isSel('f2c')" class="report-section">
      <div class="report-formno">Form 2.c</div>
      <div class="report-title">Penetapan Konteks Risiko Operasional OPD</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th>Tujuan Strategis</th><th>Program</th><th>Keluaran/Hasil Kegiatan</th><th>Keluaran Sub Kegiatan</th><th>Urusan</th></tr></thead>
        <tbody>
          <tr v-for="r in d.f2c" :key="r.id"><td>{{ r.tujuan_strategis }}</td><td>{{ r.program }}</td><td>{{ r.keluaran_hasil_kegiatan }}</td><td>{{ r.keluaran_sub_kegiatan }}</td><td>{{ r.urusan_pemerintahan }}</td></tr>
          <tr v-if="!d.f2c || !d.f2c.length"><td colspan="5" class="c">Belum ada data</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 3 ============ -->
    <section v-if="isSel('f3') && d.f4" class="report-section">
      <div class="report-formno">Form 3</div>
      <div class="report-title">Kertas Kerja Identifikasi Risiko</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Tujuan/Sasaran/Kegiatan</th><th>Risiko</th><th style="width: 90px">Kode</th><th>Pemilik</th><th>Sebab</th><th style="width: 40px">C/UC</th><th>Dampak</th></tr></thead>
        <tbody>
          <template v-for="g in d.f4" :key="g.jenis">
            <tr><td class="c"></td><td colspan="7"><b>{{ jenisLabel[g.jenis] }}</b></td></tr>
            <tr v-for="(it, i) in g.items" :key="it.id">
              <td class="c">{{ i + 1 }}</td><td>{{ it.kegiatan || it.tujuan_sasaran }}</td><td>{{ it.uraian_risiko }}</td>
              <td>{{ it.kode_risiko }}</td><td>{{ it.pemilik_risiko }}</td><td>{{ it.sebab_uraian }}</td>
              <td class="c">{{ it.cuc }}</td><td>{{ it.dampak_uraian }}</td>
            </tr>
            <tr v-if="!g.items.length"><td class="c"></td><td colspan="7" class="c">Belum ada data</td></tr>
          </template>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 4 ============ -->
    <section v-if="isSel('f4') && d.f4" class="report-section">
      <div class="report-formno">Form 4</div>
      <div class="report-title">Kertas Kerja Hasil Analisis Risiko</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Risiko</th><th style="width: 90px">Kode</th><th style="width: 60px">Dampak</th><th style="width: 70px">Kemungkinan</th><th style="width: 50px">Skala</th><th style="width: 100px">Level</th></tr></thead>
        <tbody>
          <template v-for="g in d.f4" :key="g.jenis">
            <tr><td class="c"></td><td colspan="6"><b>{{ jenisLabel[g.jenis] }}</b></td></tr>
            <tr v-for="(it, i) in g.items" :key="it.id">
              <td class="c">{{ i + 1 }}</td><td>{{ it.uraian_risiko }}</td><td>{{ it.kode_risiko }}</td>
              <td class="c">{{ it.analisis.skala_dampak ?? '' }}</td><td class="c">{{ it.analisis.skala_kemungkinan ?? '' }}</td>
              <td class="c"><b>{{ it.analisis.skala_risiko ?? '' }}</b></td>
              <td class="c">{{ it.analisis.level ?? '' }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 5 ============ -->
    <section v-if="isSel('f5') && d.f5" class="report-section">
      <div class="report-formno">Form 5</div>
      <div class="report-title">Kertas Kerja Daftar Risiko Prioritas</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Risiko Prioritas</th><th style="width: 90px">Kode</th><th style="width: 50px">Skala</th><th>Pemilik</th><th>Penyebab</th><th>Dampak</th></tr></thead>
        <tbody>
          <template v-for="g in d.f5" :key="g.jenis">
            <tr v-if="g.items.length"><td class="c"></td><td colspan="6"><b>{{ jenisLabel[g.jenis] }}</b></td></tr>
            <tr v-for="(it, i) in g.items" :key="it.id">
              <td class="c">{{ i + 1 }}</td><td>{{ it.uraian_risiko }}</td><td>{{ it.kode_risiko }}</td>
              <td class="c"><b>{{ it.analisis.skala_risiko }}</b></td><td>{{ it.pemilik_risiko }}</td>
              <td>{{ it.sebab_uraian }}</td><td>{{ it.dampak_uraian }}</td>
            </tr>
          </template>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 7 ============ -->
    <section v-if="isSel('f7') && d.f7" class="report-section">
      <div class="report-formno">Form 7</div>
      <div class="report-title">Penilaian Kegiatan Pengendalian (RTP atas Hasil Identifikasi Risiko)</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Risiko Prioritas</th><th style="width: 90px">Kode</th><th>Pengendalian yang Ada</th><th>Celah</th><th>Rencana Tindak Pengendalian</th><th style="width: 90px">Target</th></tr></thead>
        <tbody>
          <tr v-for="(it, i) in d.f7" :key="it.id">
            <td class="c">{{ i + 1 }}</td><td>{{ it.uraian_risiko }}</td><td>{{ it.kode_risiko }}</td>
            <td>{{ it.rtp?.pengendalian_ada }}</td><td>{{ it.rtp?.celah_pengendalian }}</td>
            <td>{{ it.rtp?.rencana_tindak }}</td><td>{{ it.rtp?.target_waktu }}</td>
          </tr>
          <tr v-if="!d.f7 || !d.f7.length"><td colspan="7" class="c">Belum ada risiko prioritas</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 8 ============ -->
    <section v-if="isSel('f8')" class="report-section">
      <div class="report-formno">Form 8</div>
      <div class="report-title">Rencana & Realisasi Pengkomunikasian Pengendalian</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Kegiatan Pengendalian</th><th>Media/Bentuk</th><th>Penyedia</th><th>Penerima</th><th style="width: 90px">Rencana</th><th style="width: 90px">Realisasi</th></tr></thead>
        <tbody>
          <tr v-for="(r, i) in d.f8" :key="r.id">
            <td class="c">{{ r.no_urut || i + 1 }}</td><td>{{ r.kegiatan_pengendalian }}</td><td>{{ r.media_bentuk }}</td>
            <td>{{ r.penyedia_informasi }}</td><td>{{ r.penerima_informasi }}</td><td>{{ r.rencana_waktu }}</td><td>{{ r.realisasi_waktu }}</td>
          </tr>
          <tr v-if="!d.f8 || !d.f8.length"><td colspan="7" class="c">Belum ada data</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 9 ============ -->
    <section v-if="isSel('f9')" class="report-section">
      <div class="report-formno">Form 9</div>
      <div class="report-title">Rencana & Realisasi Pemantauan atas Kegiatan Pengendalian</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 28px">No</th><th>Kegiatan Pengendalian</th><th>Metode Pemantauan</th><th>Penanggung Jawab</th><th style="width: 90px">Rencana</th><th style="width: 90px">Realisasi</th></tr></thead>
        <tbody>
          <tr v-for="(r, i) in d.f9" :key="r.id">
            <td class="c">{{ r.no_urut || i + 1 }}</td><td>{{ r.kegiatan_pengendalian }}</td><td>{{ r.metode_pemantauan }}</td>
            <td>{{ r.penanggung_jawab }}</td><td>{{ r.rencana_waktu }}</td><td>{{ r.realisasi_waktu }}</td>
          </tr>
          <tr v-if="!d.f9 || !d.f9.length"><td colspan="6" class="c">Belum ada data</td></tr>
        </tbody>
      </table>
    </section>

    <!-- ============ Form 10 ============ -->
    <section v-if="isSel('f10') && d.f10" class="report-section">
      <div class="report-formno">Form 10</div>
      <div class="report-title">Pencatatan Kejadian Risiko (Risk Event) & Pelaksanaan RTP</div>
      <div class="report-subtitle">{{ opdName }} — Tahun {{ ctx.tahun }}</div>
      <table class="rpt">
        <thead><tr><th style="width: 90px">Kode</th><th>Risiko</th><th style="width: 80px">Tanggal</th><th>Sebab</th><th>Dampak</th><th>RTP</th><th>Realisasi RTP</th></tr></thead>
        <tbody>
          <template v-for="r in d.f10" :key="r.risiko_id">
            <template v-for="ev in r.events" :key="ev.id">
              <tr>
                <td>{{ r.kode_risiko }}</td><td>{{ r.uraian_risiko }}</td><td class="c">{{ ev.tanggal_terjadi }}</td>
                <td>{{ ev.sebab_kejadian }}</td><td>{{ ev.dampak_kejadian }}</td><td>{{ ev.rtp }}</td><td>{{ ev.realisasi_pelaksanaan_rtp }}</td>
              </tr>
            </template>
          </template>
          <tr v-if="!d.f10.some((r) => r.events.length)"><td colspan="7" class="c">Belum ada kejadian dicatat</td></tr>
        </tbody>
      </table>
      <div class="report-sign">
        <div class="box">
          Kota Tegal, {{ ctx.tahun }}<br />Kepala {{ opdName }}<br /><br /><br /><br />
          (...........................................)
        </div>
      </div>
    </section>
  </div>
</template>
