<script setup>
import CrudTable from '@/components/CrudTable.vue'
const columns = [
  { field: 'tujuan_strategis', label: 'Tujuan Strategis', type: 'textarea', width: '200px' },
  { field: 'program', label: 'Program', type: 'textarea', width: '200px' },
  { field: 'keluaran_hasil_kegiatan', label: 'Keluaran/Hasil Kegiatan', type: 'textarea', width: '200px' },
  { field: 'keluaran_sub_kegiatan', label: 'Keluaran Sub Kegiatan', type: 'textarea', width: '200px' },
  { field: 'urusan_pemerintahan', label: 'Urusan Pemerintahan', type: 'textarea', width: '160px' },
  { field: 'periode_dinilai', label: 'Periode Dinilai', width: '120px' },
  { field: 'sumber_data', label: 'Sumber Data', type: 'textarea', width: '140px' },
]
</script>
<template>
  <CrudTable endpoint="/konteks/operasional-opd" :columns="columns" title="Form 2.c — Konteks Operasional OPD" :numbered="false" />
</template>
