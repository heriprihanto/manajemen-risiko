<script setup>
import { onMounted, ref } from 'vue'
import { useToast } from 'primevue/usetoast'
import Button from 'primevue/button'
import Dialog from 'primevue/dialog'
import InputText from 'primevue/inputtext'
import { useConfirm } from 'primevue/useconfirm'
import api from '@/api'
import { useContextStore } from '@/stores/context'
import AppLoader from '@/components/AppLoader.vue'

const ctx = useContextStore()
const toast = useToast()
const confirm = useConfirm()
const form = ref(null)
const loading = ref(true)
const showAdd = ref(false)
const newResp = ref({ nama_responden: '', jabatan: '' })

async function load() {
  loading.value = true
  const { data } = await api.get('/cee/form1a', {
    params: { opd_id: ctx.opdId, tahun: ctx.tahun },
  })
  form.value = data
  loading.value = false
}

async function addResponden() {
  await api.post('/cee/responden', {
    opd_id: ctx.opdId,
    tahun: ctx.tahun,
    nama_responden: newResp.value.nama_responden,
    jabatan: newResp.value.jabatan,
  })
  showAdd.value = false
  newResp.value = { nama_responden: '', jabatan: '' }
  await load()
  toast.add({ severity: 'success', summary: 'Responden ditambahkan', life: 2000 })
}

function delResponden(r) {
  confirm.require({
    message: `Hapus responden ${r.kode_responden}?`,
    header: 'Konfirmasi',
    icon: 'pi pi-exclamation-triangle',
    accept: async () => {
      await api.delete(`/cee/responden/${r.id}`)
      await load()
    },
  })
}

let saveTimer = null
async function onAnswer(pertanyaan, respId, ev) {
  let v = ev.target.value
  if (v === '') v = null
  else {
    v = parseInt(v)
    if (isNaN(v) || v < 1 || v > 4) {
      ev.target.value = ''
      return
    }
  }
  pertanyaan.jawaban[respId] = v
  await api.post('/cee/jawaban', {
    responden_id: respId,
    pertanyaan_id: pertanyaan.id,
    nilai: v,
  })
  clearTimeout(saveTimer)
  saveTimer = setTimeout(load, 350)
}

onMounted(load)
</script>

<template>
  <div v-if="form">
    <div class="toolbar">
      <span class="muted">{{ ctx.opd?.nama_pd }} — {{ ctx.tahun }}</span>
      <span class="muted">| {{ form.responden.length }} responden (R1..R{{ form.responden.length }})</span>
      <div class="spacer" />
      <Button label="Tambah Responden" icon="pi pi-plus" size="small" @click="showAdd = true" />
    </div>

    <div class="page-card" style="overflow-x: auto; padding: 0">
      <table class="grid-table">
        <thead>
          <tr>
            <th style="width: 34px">No</th>
            <th style="min-width: 320px; text-align: left">Pertanyaan / Sub-unsur</th>
            <th v-for="r in form.responden" :key="r.id" :title="r.nama_responden || ''" class="resp-col">
              {{ r.kode_responden }}
              <i class="pi pi-times del" @click="delResponden(r)" />
            </th>
            <th style="width: 60px">Modus</th>
            <th style="width: 140px">Simpulan</th>
          </tr>
        </thead>
        <tbody>
          <template v-for="kat in form.kategori" :key="kat.id">
            <tr class="kat-row">
              <td>{{ kat.kode }}</td>
              <td style="text-align: left; font-weight: 600">{{ kat.nama }}</td>
              <td :colspan="form.responden.length + 1"></td>
              <td>
                <span v-if="kat.simpulan" class="pill" :class="kat.simpulan === 'Memadai' ? 'pill-ok' : 'pill-bad'">
                  {{ kat.simpulan }}
                </span>
              </td>
            </tr>
            <tr v-for="(p, i) in kat.pertanyaan" :key="p.id">
              <td class="muted">{{ i + 1 }}</td>
              <td style="text-align: left">{{ p.pertanyaan }}</td>
              <td v-for="r in form.responden" :key="r.id" class="ans-cell">
                <input
                  class="ans-input"
                  type="number"
                  min="1"
                  max="4"
                  :value="p.jawaban[r.id] ?? ''"
                  @change="onAnswer(p, r.id, $event)"
                />
              </td>
              <td><strong>{{ p.modus ?? '–' }}</strong></td>
              <td>
                <span v-if="p.simpulan" class="pill" :class="p.simpulan === 'Memadai' ? 'pill-ok' : 'pill-bad'">
                  {{ p.simpulan }}
                </span>
              </td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
    <p class="muted" style="font-size: 0.8rem; margin-top: 10px">
      Skala jawaban 1–4 (1=Tidak Setuju, 2=Kurang Setuju, 3=Setuju, 4=Sangat Setuju). Simpulan
      pertanyaan <strong>Memadai</strong> bila modus 3/4, <strong>Kurang Memadai</strong> bila modus 1/2.
    </p>

    <Dialog v-model:visible="showAdd" header="Tambah Responden" modal style="width: 420px">
      <div style="display: flex; flex-direction: column; gap: 12px; padding-top: 6px">
        <span>
          <label class="muted" style="font-size: 0.82rem">Nama Responden</label>
          <InputText v-model="newResp.nama_responden" style="width: 100%" />
        </span>
        <span>
          <label class="muted" style="font-size: 0.82rem">Jabatan</label>
          <InputText v-model="newResp.jabatan" style="width: 100%" />
        </span>
      </div>
      <template #footer>
        <Button label="Batal" text @click="showAdd = false" />
        <Button label="Simpan" icon="pi pi-check" @click="addResponden" />
      </template>
    </Dialog>
  </div>
  <AppLoader v-else-if="loading" label="Memuat kuesioner…" />
</template>

<style scoped>
.grid-table { border-collapse: collapse; width: 100%; font-size: 0.84rem; }
.grid-table th, .grid-table td {
  border: 1px solid #e2e8f0; padding: 6px 8px; text-align: center; vertical-align: middle;
}
.grid-table thead th { background: #f8fafc; position: sticky; top: 0; font-weight: 600; }
.kat-row td { background: #eff6ff; }
.resp-col { white-space: nowrap; }
.resp-col .del { color: #cbd5e1; cursor: pointer; margin-left: 4px; font-size: 0.7rem; }
.resp-col .del:hover { color: #ef4444; }
.ans-cell { padding: 2px !important; }
.ans-input {
  width: 42px; text-align: center; border: 1px solid #e2e8f0; border-radius: 5px;
  padding: 4px 2px; font-size: 0.84rem;
}
.ans-input:focus { outline: 2px solid #93c5fd; border-color: #3b82f6; }
</style>
