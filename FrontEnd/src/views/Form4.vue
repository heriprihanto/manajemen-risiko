<script setup>
import { onMounted, ref } from 'vue'
import Select from 'primevue/select'
import Checkbox from 'primevue/checkbox'
import { useToast } from 'primevue/usetoast'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const toast = useToast()
const groups = ref([])

const skalaOptions = [1, 2, 3, 4].map((v) => ({ label: String(v), value: v }))
const levelColor = {
  Rendah: '#22c55e', Sedang: '#eab308', Tinggi: '#f97316', 'Sangat Tinggi': '#ef4444',
}

async function load() {
  const { data } = await api.get('/risiko/form4', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun },
  })
  groups.value = data
}
async function saveAnalisis(item, { recalcPrioritas = false } = {}) {
  const a = item.analisis
  const payload = {
    risiko_id: item.id,
    skala_dampak: a.skala_dampak,
    skala_kemungkinan: a.skala_kemungkinan,
  }
  // Saat dampak/kemungkinan diubah, biarkan backend menghitung ulang is_prioritas default.
  if (!recalcPrioritas) payload.is_prioritas = a.is_prioritas
  const { data } = await api.post('/risiko/analisis', payload)
  Object.assign(item.analisis, data)
  toast.add({ severity: 'success', summary: 'Analisis tersimpan', life: 1200 })
}
onMounted(load)
</script>

<template>
  <p class="muted" style="margin-top: 0">
    Skala Risiko = Skala Dampak × Skala Kemungkinan. Risiko dengan skala &gt; 4 otomatis menjadi
    <strong>prioritas</strong> (dapat disesuaikan manual).
  </p>
  <div v-for="g in groups" :key="g.jenis" class="page-card" style="margin-bottom: 16px; padding: 0">
    <div style="padding: 10px 14px; font-weight: 600; background: #eff6ff; border-bottom: 1px solid #e2e8f0">
      {{ g.label }} ({{ g.items.length }})
    </div>
    <table class="grid-table">
      <thead>
        <tr>
          <th style="width: 40px">No</th>
          <th style="text-align: left; min-width: 240px">Risiko</th>
          <th style="width: 110px">Kode</th>
          <th style="width: 110px">Dampak</th>
          <th style="width: 130px">Kemungkinan</th>
          <th style="width: 70px">Skala</th>
          <th style="width: 120px">Level</th>
          <th style="width: 80px">Prioritas</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(it, i) in g.items" :key="it.id">
          <td style="text-align: center">{{ i + 1 }}</td>
          <td>{{ it.uraian_risiko }}</td>
          <td style="text-align: center">{{ it.kode_risiko }}</td>
          <td style="text-align: center">
            <Select v-model="it.analisis.skala_dampak" :options="skalaOptions" optionLabel="label" optionValue="value"
              placeholder="—" style="width: 84px" @change="saveAnalisis(it, { recalcPrioritas: true })" />
          </td>
          <td style="text-align: center">
            <Select v-model="it.analisis.skala_kemungkinan" :options="skalaOptions" optionLabel="label" optionValue="value"
              placeholder="—" style="width: 84px" @change="saveAnalisis(it, { recalcPrioritas: true })" />
          </td>
          <td style="text-align: center; font-weight: 700">{{ it.analisis.skala_risiko ?? '–' }}</td>
          <td style="text-align: center">
            <span v-if="it.analisis.level" class="pill" :style="{ background: levelColor[it.analisis.level] + '22', color: levelColor[it.analisis.level] }">
              {{ it.analisis.level }}
            </span>
          </td>
          <td style="text-align: center">
            <Checkbox v-model="it.analisis.is_prioritas" binary @change="saveAnalisis(it)" />
          </td>
        </tr>
        <tr v-if="!g.items.length"><td colspan="8" class="muted" style="padding: 12px">Belum ada risiko.</td></tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.grid-table { border-collapse: collapse; width: 100%; font-size: 0.85rem; }
.grid-table th, .grid-table td { border: 1px solid #e2e8f0; padding: 6px 10px; }
.grid-table thead th { background: #f8fafc; font-weight: 600; }
</style>
