<script setup>
import { onMounted, ref } from 'vue'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const data = ref(null)
const loading = ref(true)

const levelColor = {
  Rendah: '#22c55e',
  Sedang: '#eab308',
  Tinggi: '#f97316',
  'Sangat Tinggi': '#ef4444',
}
const jenisLabel = {
  strategis_pemda: 'Strategis Pemda',
  strategis_opd: 'Strategis OPD',
  operasional_opd: 'Operasional OPD',
}

async function load() {
  loading.value = true
  const { data: d } = await api.get('/dashboard/summary', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun },
  })
  data.value = d
  loading.value = false
}
onMounted(load)
</script>

<template>
  <div v-if="data">
    <div class="muted" style="margin-bottom: 14px">
      {{ ctx.opd?.nama_pd }} — Tahun Penilaian {{ ctx.tahun }}
    </div>
    <div class="stat-grid">
      <div class="stat">
        <div class="v">{{ data.jumlah_responden }}</div>
        <div class="l">Responden Kuesioner CEE</div>
      </div>
      <div class="stat">
        <div class="v">{{ data.jumlah_risiko }}</div>
        <div class="l">Risiko Teridentifikasi</div>
      </div>
      <div class="stat">
        <div class="v">{{ data.jumlah_dianalisis }}</div>
        <div class="l">Risiko Dianalisis</div>
      </div>
      <div class="stat">
        <div class="v" style="color: #ef4444">{{ data.jumlah_prioritas }}</div>
        <div class="l">Risiko Prioritas</div>
      </div>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 18px">
      <div class="page-card">
        <h3 style="margin-top: 0">Risiko per Level</h3>
        <div v-for="(n, lvl) in data.risiko_per_level" :key="lvl" style="margin-bottom: 10px">
          <div style="display: flex; justify-content: space-between; font-size: 0.85rem">
            <span>{{ lvl }}</span><strong>{{ n }}</strong>
          </div>
          <div style="background: #eef2f7; border-radius: 6px; height: 10px; overflow: hidden">
            <div
              :style="{
                width: (data.jumlah_dianalisis ? (n / data.jumlah_dianalisis) * 100 : 0) + '%',
                background: levelColor[lvl],
                height: '100%',
              }"
            />
          </div>
        </div>
      </div>
      <div class="page-card">
        <h3 style="margin-top: 0">Risiko per Jenis</h3>
        <table style="width: 100%; font-size: 0.88rem; border-collapse: collapse">
          <tr v-for="(n, j) in data.risiko_per_jenis" :key="j" style="border-bottom: 1px solid #eef2f7">
            <td style="padding: 8px 0">{{ jenisLabel[j] || j }}</td>
            <td style="text-align: right; font-weight: 600">{{ n }}</td>
          </tr>
          <tr v-if="!Object.keys(data.risiko_per_jenis).length">
            <td class="muted" style="padding: 8px 0">Belum ada data risiko.</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
  <div v-else-if="loading" class="muted">Memuat…</div>
</template>
