<script setup>
import { onMounted, ref } from 'vue'
import Textarea from 'primevue/textarea'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const toast = useToast()
const model = ref({})

const fields = [
  ['sumber_data', 'Sumber Data'],
  ['visi', 'Visi'],
  ['misi_strategis', 'Misi Strategis RPJMD'],
  ['penetapan_konteks_misi', 'Penetapan Konteks Misi'],
  ['tujuan_strategis', 'Tujuan Strategis RPD'],
  ['penetapan_konteks_tujuan', 'Penetapan Konteks Tujuan'],
  ['sasaran_rpd', 'Sasaran RPD'],
  ['penetapan_konteks_sasaran', 'Penetapan Konteks Sasaran'],
  ['iku_sasaran', 'IKU Sasaran RPD'],
  ['penetapan_konteks_iku', 'Penetapan Konteks IKU'],
  ['prioritas_program', 'Prioritas Pembangunan & Program Unggulan'],
  ['urusan_pemerintahan', 'Urusan Pemerintahan Daerah'],
  ['periode_dinilai', 'Periode yang Dinilai'],
]

async function load() {
  const { data } = await api.get('/konteks/pemda', { params: { tahun: ctx.tahun } })
  model.value = data || {}
}
async function save() {
  await api.post('/konteks/pemda', { ...model.value, tahun: ctx.tahun })
  toast.add({ severity: 'success', summary: 'Konteks Pemda tersimpan', life: 2000 })
  await load()
}
onMounted(load)
</script>

<template>
  <div class="page-card">
    <p class="muted" style="margin-top: 0">
      Penetapan konteks risiko strategis Pemerintah Daerah — berlaku untuk seluruh OPD pada Tahun {{ ctx.tahun }}.
    </p>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px">
      <div v-for="f in fields" :key="f[0]">
        <label class="muted" style="font-size: 0.82rem">{{ f[1] }}</label>
        <Textarea v-model="model[f[0]]" autoResize rows="2" style="width: 100%" />
      </div>
    </div>
    <div style="margin-top: 16px">
      <Button label="Simpan" icon="pi pi-check" @click="save" />
    </div>
  </div>
</template>
