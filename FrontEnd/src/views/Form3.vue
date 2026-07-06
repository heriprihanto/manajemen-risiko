<script setup>
import { computed, onMounted, ref } from 'vue'
import DataTable from 'primevue/datatable'
import Column from 'primevue/column'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import Select from 'primevue/select'
import SelectButton from 'primevue/selectbutton'
import { useToast } from 'primevue/usetoast'
import { useConfirm } from 'primevue/useconfirm'
import api from '@/api'
import { useContextStore } from '@/stores/context'

const ctx = useContextStore()
const toast = useToast()
const confirm = useConfirm()

const jenisOptions = [
  { label: 'Strategis Pemda (3.a)', value: 'strategis_pemda' },
  { label: 'Strategis OPD (3.b)', value: 'strategis_opd' },
  { label: 'Operasional OPD (3.c)', value: 'operasional_opd' },
]
const jenis = ref('operasional_opd')
const rows = ref([])
const loading = ref(true)
const dialog = ref(false)
const editing = ref({})
const isNew = ref(false)

const isOperasional = computed(() => editing.value.jenis_risiko === 'operasional_opd')

async function load() {
  loading.value = true
  const { data } = await api.get('/risiko', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun, jenis: jenis.value },
  })
  rows.value = data
  loading.value = false
}
function openNew() {
  editing.value = { jenis_risiko: jenis.value, sebab_sumber: 'Internal', cuc: 'C' }
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
    <SelectButton v-model="jenis" :options="jenisOptions" optionLabel="label" optionValue="value" @change="load" />
    <div class="spacer" />
    <Button label="Tambah Risiko" icon="pi pi-plus" size="small" @click="openNew" />
  </div>

  <div class="page-card" style="padding: 0">
    <DataTable :value="rows" :loading="loading" size="small" stripedRows scrollable>
      <Column header="No" :style="{ width: '46px' }">
        <template #body="{ index }">{{ index + 1 }}</template>
      </Column>
      <Column field="kode_risiko" header="Kode" :style="{ minWidth: '110px' }" />
      <Column :header="jenis === 'operasional_opd' ? 'Kegiatan' : 'Tujuan/Sasaran'" :style="{ minWidth: '180px' }">
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

  <Dialog v-model:visible="dialog" header="Identifikasi Risiko" modal style="width: 720px">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; padding-top: 6px">
      <div style="grid-column: 1 / -1">
        <label class="muted lbl">Jenis Risiko</label>
        <Select v-model="editing.jenis_risiko" :options="jenisOptions" optionLabel="label" optionValue="value" style="width: 100%" />
      </div>
      <template v-if="isOperasional">
        <div>
          <label class="muted lbl">Kegiatan</label>
          <Textarea v-model="editing.kegiatan" autoResize rows="2" style="width: 100%" />
        </div>
        <div>
          <label class="muted lbl">Tahap Kegiatan</label>
          <InputText v-model="editing.tahap_kegiatan" style="width: 100%" />
        </div>
        <div style="grid-column: 1 / -1">
          <label class="muted lbl">Indikator Keluaran</label>
          <Textarea v-model="editing.indikator_keluaran" autoResize rows="2" style="width: 100%" />
        </div>
      </template>
      <template v-else>
        <div>
          <label class="muted lbl">Tujuan/Sasaran Strategis</label>
          <Textarea v-model="editing.tujuan_sasaran" autoResize rows="2" style="width: 100%" />
        </div>
        <div>
          <label class="muted lbl">Indikator Kinerja</label>
          <Textarea v-model="editing.indikator_kinerja" autoResize rows="2" style="width: 100%" />
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
</style>
