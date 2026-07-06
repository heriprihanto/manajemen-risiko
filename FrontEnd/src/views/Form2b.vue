<script setup>
import CrudTable from '@/components/CrudTable.vue'
const columns = [
  {
    field: 'tujuan_strategis',
    label: 'Tujuan Strategis',
    type: 'select',
    optionsEndpoint: '/master/renstra/tujuan',
    editable: true,
    width: '200px',
  },
  {
    field: 'sasaran_strategis',
    label: 'Sasaran Strategis',
    type: 'select',
    optionsEndpoint: '/master/renstra/sasaran',
    dependsOn: 'tujuan_strategis',
    dependsMatch: 'tujuan_strategis',
    editable: true,
    width: '200px',
  },
  {
    field: 'iku_renstra',
    label: 'IKU Renstra',
    type: 'select',
    optionsEndpoint: '/master/renstra/iku',
    editable: true,
    width: '160px',
  },
  {
    field: 'program',
    label: 'Program',
    type: 'select',
    optionsEndpoint: '/master/renstra/program',
    editable: true,
    width: '180px',
  },
  { field: 'urusan_pemerintahan', label: 'Urusan Pemerintahan', type: 'textarea', width: '160px' },
  {
    field: 'periode_dinilai',
    label: 'Periode Dinilai',
    type: 'select',
    optionsEndpoint: '/master/renstra/tahap',
    editable: true,
    width: '120px',
  },
  { field: 'sumber_data', label: 'Sumber Data', type: 'textarea', width: '140px' },
  { field: 'tujuan_sasaran_iku_program', label: 'Penetapan Konteks (T/S/IKU/Program)', type: 'textarea', width: '220px' },
]
</script>
<template>
  <CrudTable endpoint="/konteks/strategis-opd" :columns="columns" title="Form 2.b — Konteks Strategis OPD" :numbered="false" />
</template>
