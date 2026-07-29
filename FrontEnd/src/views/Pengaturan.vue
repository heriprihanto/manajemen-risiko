<script setup>
import { computed, onMounted, ref } from 'vue'
import DatePicker from 'primevue/datepicker'
import InputNumber from 'primevue/inputnumber'
import InputText from 'primevue/inputtext'
import ToggleSwitch from 'primevue/toggleswitch'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { useToast } from 'primevue/usetoast'
import api from '@/api'
import AppLoader from '@/components/AppLoader.vue'
import { useContextStore } from '@/stores/context'

const toast = useToast()
const ctx = useContextStore()

const loading = ref(true)
const saving = ref(false)
const form = ref({
  tahun_default: null,
  survei_mulai: null,
  survei_selesai: null,
  survei_aktif: true,
  survei_pesan_tutup: '',
})
const status = ref(null) // status jadwal dari server
const updated = ref({ at: null, by: null })

// Kolom tanggal dikirim/diterima sebagai 'YYYY-MM-DD'; DatePicker memakai Date.
const toDate = (s) => (s ? new Date(`${s}T00:00:00`) : null)
const toIso = (d) => {
  if (!d) return null
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
}
const fmt = (s) =>
  s ? new Date(`${s}T00:00:00`).toLocaleDateString('id-ID', { dateStyle: 'long' }) : '—'

const rentangSalah = computed(() => {
  const { survei_mulai: a, survei_selesai: b } = form.value
  return !!(a && b && a > b)
})

async function load() {
  loading.value = true
  const { data } = await api.get('/pengaturan')
  form.value = {
    tahun_default: data.tahun_default,
    survei_mulai: toDate(data.survei_mulai),
    survei_selesai: toDate(data.survei_selesai),
    survei_aktif: !!data.survei_aktif,
    survei_pesan_tutup: data.survei_pesan_tutup || '',
  }
  status.value = data.survei_status
  updated.value = { at: data.updated_at, by: data.updated_by }
  loading.value = false
}

async function save() {
  if (rentangSalah.value) return
  saving.value = true
  try {
    const { data } = await api.put('/pengaturan', {
      tahun_default: form.value.tahun_default,
      survei_mulai: toIso(form.value.survei_mulai),
      survei_selesai: toIso(form.value.survei_selesai),
      survei_aktif: form.value.survei_aktif,
      survei_pesan_tutup: form.value.survei_pesan_tutup,
    })
    status.value = data.survei_status
    updated.value = { at: data.updated_at, by: data.updated_by }
    // Sesi ini ikut pindah tahun bila admin belum memilih tahun sendiri.
    if (data.tahun_default) ctx.applyTahunDefault(data.tahun_default)
    toast.add({ severity: 'success', summary: 'Pengaturan tersimpan', life: 2000 })
  } catch (e) {
    toast.add({
      severity: 'error',
      summary: 'Gagal menyimpan',
      detail: e.response?.data?.detail || 'Coba lagi',
      life: 4000,
    })
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<template>
  <AppLoader v-if="loading" label="Memuat pengaturan…" />

  <template v-else>
    <div class="page-card" style="margin-bottom: 16px">
      <h3 class="sec-title">Tahun Penilaian</h3>
      <p class="muted sec-desc">
        Tahun yang dipakai sebagai awalan saat pengguna membuka aplikasi dan sebagai tahun
        survei CEE. Pengguna tetap dapat memilih tahun lain lewat pemilih tahun di kanan atas.
      </p>
      <label class="lbl">Tahun Default</label>
      <InputNumber
        v-model="form.tahun_default"
        :useGrouping="false"
        :min="2000"
        :max="2100"
        showButtons
        placeholder="cth: 2026"
        style="width: 180px"
      />
    </div>

    <div class="page-card">
      <h3 class="sec-title">Jadwal Survei CEE</h3>
      <p class="muted sec-desc">
        Rentang tanggal saat responden boleh mengisi survei publik. Tanggal bersifat
        <strong>inklusif</strong> — dikosongkan berarti tanpa batas pada sisi tersebut.
      </p>

      <Message
        v-if="status"
        :severity="status.dibuka ? 'success' : 'warn'"
        :closable="false"
        class="status-msg"
      >
        <template v-if="status.dibuka">
          Survei <strong>sedang dibuka</strong> hari ini.
        </template>
        <template v-else>
          Survei <strong>tertutup</strong> — {{ status.alasan }}
        </template>
      </Message>

      <div class="grid-2" style="gap: 14px; margin-top: 14px">
        <div>
          <label class="lbl">Tanggal Mulai</label>
          <DatePicker
            v-model="form.survei_mulai"
            dateFormat="dd-mm-yy"
            showIcon
            showButtonBar
            placeholder="Tanpa batas awal"
            fluid
          />
        </div>
        <div>
          <label class="lbl">Tanggal Selesai</label>
          <DatePicker
            v-model="form.survei_selesai"
            dateFormat="dd-mm-yy"
            showIcon
            showButtonBar
            placeholder="Tanpa batas akhir"
            :minDate="form.survei_mulai || undefined"
            fluid
          />
        </div>
      </div>

      <Message v-if="rentangSalah" severity="error" :closable="false" style="margin-top: 12px">
        Tanggal mulai tidak boleh melewati tanggal selesai.
      </Message>

      <div class="switch-row">
        <ToggleSwitch v-model="form.survei_aktif" inputId="survei-aktif" />
        <label for="survei-aktif">
          <strong>Survei aktif</strong>
          <small class="muted">
            Matikan untuk menutup survei sewaktu-waktu tanpa mengubah tanggal.
          </small>
        </label>
      </div>

      <div style="margin-top: 14px">
        <label class="lbl">Pesan saat survei tertutup</label>
        <InputText
          v-model="form.survei_pesan_tutup"
          placeholder="cth: Survei akan dibuka kembali pada Januari 2027"
          style="width: 100%"
        />
        <small class="muted">
          Ditampilkan di halaman survei publik. Dikosongkan = memakai pesan bawaan.
        </small>
      </div>

      <p class="muted preview">
        Rentang aktif: <strong>{{ fmt(status?.mulai) }}</strong> s/d
        <strong>{{ fmt(status?.selesai) }}</strong>
      </p>
    </div>

    <div class="save-bar">
      <span v-if="updated.at" class="muted">
        Terakhir diubah {{ new Date(updated.at).toLocaleString('id-ID') }}
        <template v-if="updated.by">oleh {{ updated.by }}</template>
      </span>
      <div class="spacer" />
      <Button
        label="Simpan Pengaturan"
        icon="pi pi-check"
        :loading="saving"
        :disabled="rentangSalah"
        @click="save"
      />
    </div>
  </template>
</template>

<style scoped>
.sec-title { margin: 0 0 4px; font-size: 1rem; }
.sec-desc { margin: 0 0 14px; font-size: 0.84rem; line-height: 1.5; }
.lbl { display: block; font-size: 0.82rem; font-weight: 600; color: #334155; margin-bottom: 4px; }
.status-msg { margin: 0; }
.switch-row {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-top: 16px;
}
.switch-row label { font-size: 0.86rem; cursor: pointer; }
.switch-row small { display: block; font-size: 0.78rem; margin-top: 2px; }
.preview { margin: 14px 0 0; font-size: 0.84rem; }
.save-bar { display: flex; align-items: center; gap: 12px; margin-top: 16px; flex-wrap: wrap; }
</style>
