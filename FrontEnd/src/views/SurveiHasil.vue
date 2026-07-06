<script setup>
import { computed, onMounted, ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import SelectButton from 'primevue/selectbutton'
import Tag from 'primevue/tag'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const loading = ref(true)
const data = ref(null)
const expanded = ref([])
const sumber = ref('all')

const sumberOptions = [
  { label: 'Semua', value: 'all' },
  { label: 'Survei Publik', value: 'survei' },
  { label: 'Input Admin', value: 'admin' },
]

const skalaLabel = {
  1: 'Tidak Setuju',
  2: 'Kurang Setuju',
  3: 'Setuju',
  4: 'Sangat Setuju',
}

const responden = computed(() => {
  const list = data.value?.responden || []
  return sumber.value === 'all' ? list : list.filter((r) => r.sumber === sumber.value)
})
const totalResp = computed(() => responden.value.length)
const rataKeseluruhan = computed(() => {
  const vals = responden.value.map((r) => r.rata_rata).filter((v) => v != null)
  if (!vals.length) return '–'
  return (vals.reduce((a, b) => a + b, 0) / vals.length).toFixed(2)
})
const totalPertanyaan = computed(() => data.value?.total_pertanyaan || 0)

function fmtDate(iso) {
  if (!iso) return '–'
  try {
    return new Date(iso).toLocaleString('id-ID', { dateStyle: 'medium', timeStyle: 'short' })
  } catch {
    return iso
  }
}
function nilaiColor(v) {
  if (v == null) return 'secondary'
  if (v >= 3) return 'success'
  return 'danger'
}

async function load() {
  loading.value = true
  expanded.value = []
  const { data: d } = await api.get('/cee/survei-hasil', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun },
  })
  data.value = d
  loading.value = false
}

onMounted(load)
</script>

<template>
  <div class="toolbar no-print">
    <span class="muted">{{ ctx.opd?.nama_pd }} — {{ ctx.tahun }}</span>
    <div class="spacer" />
    <SelectButton v-model="sumber" :options="sumberOptions" optionLabel="label" optionValue="value" />
  </div>

  <div v-if="loading" class="muted">Memuat rincian hasil survei…</div>

  <template v-else>
    <div class="stat-grid" style="margin-bottom: 16px">
      <div class="stat"><div class="v">{{ totalResp }}</div><div class="l">Responden</div></div>
      <div class="stat"><div class="v">{{ totalPertanyaan }}</div><div class="l">Pertanyaan per Responden</div></div>
      <div class="stat"><div class="v">{{ rataKeseluruhan }}</div><div class="l">Rata-rata Skor (1–4)</div></div>
    </div>

    <div class="page-card" style="padding: 0">
      <DataTable
        v-model:expandedRows="expanded"
        :value="responden"
        dataKey="id"
        size="small"
        stripedRows
        scrollable
      >
        <Column expander :style="{ width: '42px' }" />
        <Column field="kode_responden" header="Kode" :style="{ width: '70px' }" />
        <Column header="Nama Responden" :style="{ minWidth: '180px' }">
          <template #body="{ data: r }">{{ r.nama_responden || '–' }}</template>
        </Column>
        <Column header="Jabatan" :style="{ minWidth: '150px' }">
          <template #body="{ data: r }">{{ r.jabatan || '–' }}</template>
        </Column>
        <Column header="Email" :style="{ minWidth: '190px' }">
          <template #body="{ data: r }"><span class="muted">{{ r.email || '–' }}</span></template>
        </Column>
        <Column header="Sumber" :style="{ width: '120px' }">
          <template #body="{ data: r }">
            <Tag
              :value="r.sumber === 'survei' ? 'Survei Publik' : 'Input Admin'"
              :severity="r.sumber === 'survei' ? 'info' : 'secondary'"
            />
          </template>
        </Column>
        <Column header="Terisi" :style="{ width: '90px' }">
          <template #body="{ data: r }">{{ r.jumlah_jawaban }} / {{ totalPertanyaan }}</template>
        </Column>
        <Column header="Rata-rata" :style="{ width: '90px' }">
          <template #body="{ data: r }"><strong>{{ r.rata_rata ?? '–' }}</strong></template>
        </Column>
        <Column header="Waktu Pengisian" :style="{ minWidth: '160px' }">
          <template #body="{ data: r }"><span class="muted">{{ fmtDate(r.submitted_at) }}</span></template>
        </Column>

        <template #expansion="{ data: r }">
          <div class="detail">
            <div v-for="kat in data.kategori" :key="kat.id" class="detail-kat">
              <div class="detail-head">{{ kat.kode }}. {{ kat.nama }}</div>
              <table class="detail-table">
                <tbody>
                  <tr v-for="(p, i) in kat.pertanyaan" :key="p.id">
                    <td class="c muted" style="width: 32px">{{ i + 1 }}</td>
                    <td>{{ p.pertanyaan }}</td>
                    <td class="c" style="width: 150px">
                      <Tag
                        v-if="r.jawaban[p.id] != null"
                        :value="`${r.jawaban[p.id]} — ${skalaLabel[r.jawaban[p.id]]}`"
                        :severity="nilaiColor(r.jawaban[p.id])"
                      />
                      <span v-else class="muted">Belum dijawab</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </template>

        <template #empty><div class="muted" style="padding: 14px">Belum ada responden survei.</div></template>
      </DataTable>
    </div>
  </template>
</template>

<style scoped>
.detail { padding: 8px 14px 14px; background: #f8fafc; }
.detail-kat { margin-bottom: 12px; }
.detail-head { font-weight: 600; color: #0f172a; margin: 8px 0 4px; }
.detail-table { border-collapse: collapse; width: 100%; font-size: 0.82rem; background: #fff; }
.detail-table td { border: 1px solid #e2e8f0; padding: 4px 8px; vertical-align: top; }
.detail-table td.c { text-align: center; }
</style>
