<script setup>
import { computed, onMounted, ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import api from '@/api'
import { useContextStore } from '@/stores/context'

// Jenis risiko dikunci oleh menu (Form 3.a/3.b/3.c) lewat prop.
const props = defineProps({
  jenis: { type: String, required: true }, // strategis_pemda | strategis_opd | operasional_opd
})

const ctx = useContextStore()
const toast = useToast()
const confirm = useConfirm()

const jenisLabel = {
  strategis_pemda: 'Risiko Strategis Pemda (Form 3.a)',
  strategis_opd: 'Risiko Strategis OPD (Form 3.b)',
  operasional_opd: 'Risiko Operasional OPD (Form 3.c)',
}
const rows = ref([])
const loading = ref(true)
const dialog = ref(false)
const editing = ref({})
const isNew = ref(false)
// Form 2.b — daftar konteks strategis OPD sebagai sumber pilihan Form 3.b.
const konteksOptions = ref([])

// Form 2.a — daftar Penetapan Konteks IKU sebagai sumber pilihan Form 3.a.
const ikuOptions = ref([])

const isOperasional = computed(() => props.jenis === 'operasional_opd')
const isStrategisOpd = computed(() => props.jenis === 'strategis_opd')
const isStrategisPemda = computed(() => props.jenis === 'strategis_pemda')

// Field multi-pilihan Form 2.a disimpan sebagai teks dipisah newline.
const toList = (v) => (v ? String(v).split('\n').filter(Boolean) : [])

// Nilai lama yang tidak (lagi) ada di Form 2.a tetap ditampilkan sebagai opsi
// supaya tidak hilang saat baris risiko disimpan ulang.
const ikuSelectOptions = computed(() => {
  const cur = (editing.value.indikator_kinerja || '').trim()
  if (!cur || ikuOptions.value.some((o) => o.value === cur)) return ikuOptions.value
  return [...ikuOptions.value, { value: cur, label: cur }]
})
const selectedIku = computed(() =>
  ikuOptions.value.find((o) => o.value === editing.value.indikator_kinerja),
)

// IKU Pemda menempel pada tujuan (lvl 1) atau sasaran (lvl 2) RPJMD, jadi
// Tujuan/Sasaran Strategis diturunkan dari IKU yang dipilih (masih bisa
// disunting bila perlu).
function applyIku(e) {
  const iku = ikuOptions.value.find((o) => o.value === e?.value)
  if (iku?.induk) editing.value.tujuan_sasaran = iku.induk
}

// Label ringkas satu baris Form 2.b: pakai penetapan konteks bila diisi,
// jika tidak gabungkan tujuan/sasaran/program.
function konteksLabel(k) {
  if (!k) return ''
  const penetapan = (k.tujuan_sasaran_iku_program || '').trim()
  if (penetapan) return penetapan
  return [k.tujuan_strategis, k.sasaran_strategis, k.program].filter(Boolean).join(' / ')
}
// Kunci gabungan sumber+id supaya pilihan Form 2.b & 2.c tidak bentrok id-nya.
const konteksKey = computed({
  get: () =>
    editing.value.konteks_id != null
      ? `${editing.value.konteks_sumber || 'b'}:${editing.value.konteks_id}`
      : null,
  set: () => {}, // ditulis lewat applyKonteks
})
const selectedKonteks = computed(() =>
  konteksOptions.value.find((k) => k._key === konteksKey.value),
)
// Saat konteks dipilih, turunkan kolom Tujuan/Sasaran & IKU dari sumbernya.
function applyKonteks(e) {
  const key = e?.value ?? null
  const k = konteksOptions.value.find((o) => o._key === key)
  if (!k) {
    editing.value.konteks_id = null
    editing.value.konteks_sumber = null
    editing.value.tujuan_sasaran = null
    editing.value.indikator_kinerja = null
    return
  }
  editing.value.konteks_id = k._id
  editing.value.konteks_sumber = k._source
  if (isOperasional.value) {
    // Form 3.c: konteks = subkegiatan (kegiatan + indikator keluaran) Form 2.c.
    editing.value.kegiatan = k.keluaran_hasil_kegiatan
    editing.value.indikator_keluaran = k.keluaran_sub_kegiatan
  } else if (k._source === 'c') {
    // Indikator program Form 2.c: konteks = program + indikatornya.
    editing.value.tujuan_sasaran = k.program
    editing.value.indikator_kinerja = k.indikator_program
  } else {
    editing.value.tujuan_sasaran = konteksLabel(k)
    editing.value.indikator_kinerja = k.iku_renstra
  }
}

async function load() {
  loading.value = true
  const params = { opd_id: ctx.opdId, tahun: ctx.tahun }
  if (isStrategisOpd.value) {
    const [kb, kc] = await Promise.all([
      api.get('/konteks/strategis-opd', { params }).then((r) => r.data).catch(() => []),
      api.get('/konteks/operasional-opd', { params }).then((r) => r.data).catch(() => []),
    ])
    const opt2b = (kb || []).map((k) => ({
      ...k,
      _id: k.id,
      _source: 'b',
      _key: `b:${k.id}`,
      _label: konteksLabel(k),
    }))
    // Hanya baris indikator program Form 2.c (field indikator_program terisi).
    const opt2c = (kc || [])
      .filter((k) => (k.indikator_program || '').trim())
      .map((k) => ({
        ...k,
        _id: k.id,
        _source: 'c',
        _key: `c:${k.id}`,
        _label: `[Form 2.c] ${[k.program, k.indikator_program].filter(Boolean).join(' — ')}`,
      }))
    konteksOptions.value = [...opt2b, ...opt2c]
  } else if (isOperasional.value) {
    // Form 3.c: subkegiatan yang dicentang di Form 2.c (punya ref_subkegiatan).
    const kc = await api
      .get('/konteks/operasional-opd', { params })
      .then((r) => r.data)
      .catch(() => [])
    konteksOptions.value = (kc || [])
      .filter((k) => (k.ref_subkegiatan || '').toString().trim())
      .map((k) => ({
        ...k,
        _id: k.id,
        _source: 'c',
        _key: `c:${k.id}`,
        _label:
          [k.keluaran_hasil_kegiatan, k.keluaran_sub_kegiatan].filter(Boolean).join(' — ') ||
          k.program ||
          '(subkegiatan)',
      }))
  } else if (isStrategisPemda.value) {
    // Form 3.a: Indikator Kinerja dipilih dari Penetapan Konteks IKU Form 2.a
    // (konteks Pemda berlaku untuk seluruh OPD, jadi hanya difilter per tahun).
    // Daftar master dipakai untuk melengkapi tujuan/sasaran RPJMD induk IKU.
    const [pemda, masterIku] = await Promise.all([
      api.get('/konteks/pemda', { params: { tahun: ctx.tahun } })
        .then((r) => r.data).catch(() => null),
      api.get('/master/rpjmd/iku', { params: { tahun: ctx.tahun } })
        .then((r) => r.data).catch(() => []),
    ])
    const byValue = new Map((masterIku || []).map((m) => [m.value, m]))
    ikuOptions.value = toList(pemda?.penetapan_konteks_iku).map(
      (v) => byValue.get(v) || { value: v, label: v },
    )
  }
  const { data } = await api.get('/risiko', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun, jenis: props.jenis },
  })
  rows.value = data
  loading.value = false
}
function openNew() {
  editing.value = { jenis_risiko: props.jenis, sebab_sumber: 'Internal', cuc: 'C' }
  isNew.value = true
  dialog.value = true
}
function openEdit(r) {
  editing.value = { ...r }
  isNew.value = false
  dialog.value = true
}
async function save() {
  const payload = { ...editing.value, opd_id: ctx.opdId, tahun: ctx.tahun }
  if (isNew.value) await api.post('/risiko', payload)
  else await api.put(`/risiko/${editing.value.id}`, payload)
  dialog.value = false
  await load()
  toast.add({ severity: 'success', summary: 'Risiko tersimpan', life: 1800 })
}
function remove(r) {
  confirm.require({
    message: `Hapus risiko "${r.uraian_risiko || ''}"?`,
    header: 'Konfirmasi',
    icon: 'pi pi-exclamation-triangle',
    accept: async () => {
      await api.delete(`/risiko/${r.id}`)
      await load()
    },
  })
}
onMounted(load)
</script>

<template>
  <div class="toolbar">
    <span class="muted">{{ jenisLabel[jenis] }} — {{ ctx.opd?.nama_pd }} — {{ ctx.tahun }}</span>
    <div class="spacer" />
    <Button label="Tambah Risiko" icon="pi pi-plus" size="small" @click="openNew" />
  </div>

  <div class="page-card" style="padding: 0">
    <DataTable :value="rows" :loading="loading" size="small" stripedRows scrollable>
      <Column header="No" :style="{ width: '46px' }">
        <template #body="{ index }">{{ index + 1 }}</template>
      </Column>
      <Column field="kode_risiko" header="Kode" :style="{ minWidth: '110px' }" />
      <Column :header="isOperasional ? 'Kegiatan' : 'Tujuan/Sasaran'" :style="{ minWidth: '180px' }">
        <template #body="{ data }">{{ data.kegiatan || data.tujuan_sasaran }}</template>
      </Column>
      <Column field="uraian_risiko" header="Risiko" :style="{ minWidth: '220px' }" />
      <Column field="pemilik_risiko" header="Pemilik" :style="{ minWidth: '130px' }" />
      <Column field="sebab_uraian" header="Sebab" :style="{ minWidth: '180px' }" />
      <Column field="cuc" header="C/UC" :style="{ width: '70px' }" />
      <Column field="dampak_uraian" header="Dampak" :style="{ minWidth: '180px' }" />
      <Column header="" :style="{ width: '90px' }">
        <template #body="{ data }">
          <Button icon="pi pi-pencil" text rounded size="small" @click="openEdit(data)" />
          <Button icon="pi pi-trash" text rounded size="small" severity="danger" @click="remove(data)" />
        </template>
      </Column>
      <template #empty><div class="muted" style="padding: 14px">Belum ada risiko untuk jenis ini.</div></template>
    </DataTable>
  </div>

  <Dialog v-model:visible="dialog" :header="jenisLabel[jenis]" modal style="width: 720px">
    <div class="grid-2" style="gap: 12px; padding-top: 6px">
      <template v-if="isOperasional">
        <div style="grid-column: 1 / -1">
          <label class="muted lbl">Indikator Subkegiatan (dari Form 2.c)</label>
          <Select
            :modelValue="konteksKey"
            :options="konteksOptions"
            optionLabel="_label"
            optionValue="_key"
            filter
            placeholder="Pilih subkegiatan yang dinilai"
            style="width: 100%"
            @change="applyKonteks"
          />
          <small v-if="!konteksOptions.length" class="muted">
            Belum ada subkegiatan dipilih pada Form 2.c — Konteks Operasional OPD untuk OPD & tahun ini.
          </small>
        </div>
        <div v-if="selectedKonteks" style="grid-column: 1 / -1" class="konteks-ref">
          <div><span class="muted">Program:</span> {{ selectedKonteks.program || '—' }}</div>
          <div><span class="muted">Kegiatan:</span> {{ selectedKonteks.keluaran_hasil_kegiatan || '—' }}</div>
          <div><span class="muted">Indikator Subkegiatan:</span> {{ selectedKonteks.keluaran_sub_kegiatan || '—' }}</div>
        </div>
        <div>
          <label class="muted lbl">Tahap Kegiatan</label>
          <Select
            v-model="editing.tahap_kegiatan"
            :options="['Pelaksanaan', 'Pertanggungjawaban']"
            placeholder="Pilih tahap"
            style="width: 100%"
          />
        </div>
      </template>
      <template v-else-if="isStrategisOpd">
        <div style="grid-column: 1 / -1">
          <label class="muted lbl">Tujuan/Sasaran/IKU/Program (dari Form 2.b)</label>
          <Select
            :modelValue="konteksKey"
            :options="konteksOptions"
            optionLabel="_label"
            optionValue="_key"
            filter
            placeholder="Pilih konteks (Form 2.b / indikator program Form 2.c)"
            style="width: 100%"
            @change="applyKonteks"
          />
          <small v-if="!konteksOptions.length" class="muted">
            Belum ada data pada Form 2.b / Form 2.c untuk OPD & tahun ini.
          </small>
        </div>
        <div v-if="selectedKonteks" style="grid-column: 1 / -1" class="konteks-ref">
          <div>
            <span class="muted">Sumber:</span>
            {{ selectedKonteks._source === 'c' ? 'Form 2.c — Indikator Program' : 'Form 2.b — Konteks Strategis OPD' }}
          </div>
          <template v-if="selectedKonteks._source === 'c'">
            <div><span class="muted">Program:</span> {{ selectedKonteks.program || '—' }}</div>
            <div><span class="muted">Indikator Program:</span> {{ selectedKonteks.indikator_program || '—' }}</div>
          </template>
          <template v-else>
            <div><span class="muted">Tujuan:</span> {{ selectedKonteks.tujuan_strategis || '—' }}</div>
            <div><span class="muted">Sasaran:</span> {{ selectedKonteks.sasaran_strategis || '—' }}</div>
            <div><span class="muted">IKU Renstra:</span> {{ selectedKonteks.iku_renstra || '—' }}</div>
            <div><span class="muted">Program:</span> {{ selectedKonteks.program || '—' }}</div>
          </template>
        </div>
      </template>
      <template v-else>
        <div style="grid-column: 1 / -1">
          <label class="muted lbl">Indikator Kinerja (dari Form 2.a)</label>
          <Select
            v-model="editing.indikator_kinerja"
            :options="ikuSelectOptions"
            optionLabel="label"
            optionValue="value"
            filter
            showClear
            placeholder="Pilih IKU yang dinilai"
            style="width: 100%"
            @change="applyIku"
          >
            <template #option="{ option }">
              <div>
                <div>{{ option.label }}</div>
                <small v-if="option.induk" class="muted">
                  {{ option.induk_jenis }}: {{ option.induk }}
                </small>
              </div>
            </template>
          </Select>
          <small v-if="!ikuOptions.length" class="muted">
            Belum ada Penetapan Konteks IKU pada Form 2.a — Konteks Strategis Pemda untuk tahun ini.
          </small>
        </div>
        <div v-if="selectedIku?.induk" style="grid-column: 1 / -1" class="konteks-ref">
          <div>
            <span class="muted">{{ selectedIku.induk_jenis }} RPJMD:</span> {{ selectedIku.induk }}
          </div>
        </div>
        <div style="grid-column: 1 / -1">
          <label class="muted lbl">Tujuan/Sasaran Strategis</label>
          <Textarea v-model="editing.tujuan_sasaran" autoResize rows="2" style="width: 100%" />
        </div>
      </template>
      <div style="grid-column: 1 / -1">
        <label class="muted lbl">Uraian Risiko</label>
        <Textarea v-model="editing.uraian_risiko" autoResize rows="2" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">Kode Risiko</label>
        <InputText v-model="editing.kode_risiko" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">Pemilik Risiko</label>
        <InputText v-model="editing.pemilik_risiko" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">Sebab (Uraian)</label>
        <Textarea v-model="editing.sebab_uraian" autoResize rows="2" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">Sumber Sebab</label>
        <Select v-model="editing.sebab_sumber" :options="['Internal', 'Eksternal', 'Internal/Eksternal']" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">C / UC</label>
        <Select v-model="editing.cuc" :options="['C', 'UC']" style="width: 100%" />
      </div>
      <div>
        <label class="muted lbl">Dampak — Pihak Terkena</label>
        <InputText v-model="editing.dampak_pihak_terkena" style="width: 100%" />
      </div>
      <div style="grid-column: 1 / -1">
        <label class="muted lbl">Dampak (Uraian)</label>
        <Textarea v-model="editing.dampak_uraian" autoResize rows="2" style="width: 100%" />
      </div>
    </div>
    <template #footer>
      <Button label="Batal" text @click="dialog = false" />
      <Button label="Simpan" icon="pi pi-check" @click="save" />
    </template>
  </Dialog>
</template>

<style scoped>
.lbl { font-size: 0.8rem; display: block; margin-bottom: 2px; }
.konteks-ref {
  font-size: 0.82rem;
  line-height: 1.5;
  background: var(--p-surface-100, #f4f4f5);
  border-radius: 6px;
  padding: 8px 10px;
}
</style>
