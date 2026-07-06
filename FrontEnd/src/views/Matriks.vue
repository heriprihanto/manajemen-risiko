<script setup>
import { onMounted, ref } from 'vue'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const data = ref(null)

// Warna sel sesuai skala (kemungkinan k * dampak d)
function cellColor(k, d) {
  const s = k * d
  if (s >= 12) return '#ef4444'
  if (s >= 8) return '#f97316'
  if (s >= 4) return '#eab308'
  return '#22c55e'
}
function cellItems(k, d) {
  return (data.value?.cells?.[`${k}-${d}`]) || []
}

async function load() {
  const { data: d } = await api.get('/risiko/matriks', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun },
  })
  data.value = d
}
onMounted(load)
</script>

<template>
  <div v-if="data" class="page-card">
    <p class="muted" style="margin-top: 0">
      Sebaran risiko pada matriks analisis 4×4 (Kemungkinan × Dampak). Angka pada sel adalah skala risiko.
    </p>
    <table class="matrix">
      <thead>
        <tr>
          <th class="corner" colspan="2" rowspan="2">Matriks Risiko</th>
          <th :colspan="4" class="axis">Dampak / Konsekuensi →</th>
        </tr>
        <tr>
          <th v-for="d in [1, 2, 3, 4]" :key="d" class="hd">{{ data.dampak_label[d] }}<br /><small>{{ d }}</small></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="k in [4, 3, 2, 1]" :key="k">
          <th v-if="k === 4" class="axis vert" rowspan="4"><span>Kemungkinan ↑</span></th>
          <th class="hd">{{ data.kemungkinan_label[k] }}<br /><small>{{ k }}</small></th>
          <td v-for="d in [1, 2, 3, 4]" :key="d" class="cell" :style="{ background: cellColor(k, d) + '33', borderColor: cellColor(k, d) }">
            <div class="score" :style="{ color: cellColor(k, d) }">{{ k * d }}</div>
            <div v-for="(it, i) in cellItems(k, d)" :key="i" class="chip" :title="it.uraian">
              {{ it.kode || it.uraian }}
            </div>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="legend">
      <span><i style="background: #22c55e" />Rendah (1–3)</span>
      <span><i style="background: #eab308" />Sedang (4–6)</span>
      <span><i style="background: #f97316" />Tinggi (8–9)</span>
      <span><i style="background: #ef4444" />Sangat Tinggi (12–16)</span>
    </div>
  </div>
</template>

<style scoped>
.matrix { border-collapse: collapse; width: 100%; }
.matrix th, .matrix td { border: 1px solid #e2e8f0; padding: 6px; text-align: center; }
.corner { background: #f1f5f9; }
.axis { background: #f8fafc; font-weight: 600; }
.axis.vert span { writing-mode: vertical-rl; transform: rotate(180deg); white-space: nowrap; }
.hd { background: #f8fafc; font-size: 0.78rem; width: 130px; }
.cell { height: 96px; vertical-align: top; border-width: 2px; }
.score { font-weight: 700; font-size: 1.1rem; }
.chip { background: #ffffffcc; border-radius: 4px; font-size: 0.7rem; padding: 1px 5px; margin: 2px auto; display: inline-block; }
.legend { display: flex; gap: 18px; margin-top: 14px; font-size: 0.82rem; flex-wrap: wrap; }
.legend i { display: inline-block; width: 14px; height: 14px; border-radius: 3px; margin-right: 6px; vertical-align: middle; }
</style>
