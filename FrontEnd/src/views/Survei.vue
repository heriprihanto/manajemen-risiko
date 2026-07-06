<script setup>
import { computed, onMounted, ref } from 'vue'
import { onAuthStateChanged } from 'firebase/auth'
import Select from 'primevue/select'
import InputText from 'primevue/inputtext'
import Button from 'primevue/button'
import { useToast } from 'primevue/usetoast'
import api from '@/api'
import { auth, signInWithGoogle, signOut } from '@/firebase'

const toast = useToast()

const user = ref(null)
const authReady = ref(false)
const info = ref(null)
const opdList = ref([])
const kuesioner = ref([])

const opdId = ref(null)
const nama = ref('')
const jabatan = ref('')
const answers = ref({}) // pertanyaan_id -> nilai
const submitting = ref(false)
const status = ref(null) // hasil /survei/status

const skala = [
  { nilai: 1, label: 'Tidak Setuju' },
  { nilai: 2, label: 'Kurang Setuju' },
  { nilai: 3, label: 'Setuju' },
  { nilai: 4, label: 'Sangat Setuju' },
]

const alreadySubmitted = computed(() => !!status.value?.submitted)
const totalQuestions = computed(() =>
  kuesioner.value.reduce((n, k) => n + k.pertanyaan.length, 0),
)
const answeredCount = computed(() => Object.keys(answers.value).length)
const allAnswered = computed(
  () => totalQuestions.value > 0 && answeredCount.value === totalQuestions.value,
)
const opdOptions = computed(() =>
  opdList.value.map((o) => ({ label: o.nama_pd, value: o.id_sub_pd })),
)

async function token() {
  return auth.currentUser ? await auth.currentUser.getIdToken() : null
}
function authHeader(t) {
  return { headers: { Authorization: `Bearer ${t}` } }
}

async function loadPublic() {
  const [a, b, c] = await Promise.all([
    api.get('/survei/info'),
    api.get('/survei/opd'),
    api.get('/survei/kuesioner'),
  ])
  info.value = a.data
  opdList.value = b.data
  kuesioner.value = c.data
}

async function checkStatus() {
  if (!user.value || !info.value) return
  const t = await token()
  const { data } = await api.get('/survei/status', {
    params: { tahun: info.value.tahun },
    ...authHeader(t),
  })
  status.value = data
  if (data.submitted) {
    // tampilkan jawaban tersimpan (read-only)
    answers.value = { ...data.jawaban }
    nama.value = data.nama_responden || ''
    jabatan.value = data.jabatan || ''
    opdId.value = data.opd_id
  }
}

async function doLogin() {
  try {
    await signInWithGoogle()
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Gagal masuk', detail: e.message, life: 4000 })
  }
}
async function doLogout() {
  await signOut()
  opdId.value = null
  answers.value = {}
  nama.value = ''
  jabatan.value = ''
  status.value = null
}

async function submit() {
  if (!opdId.value) {
    toast.add({ severity: 'warn', summary: 'Pilih OPD terlebih dahulu', life: 3000 })
    return
  }
  if (!nama.value.trim()) {
    toast.add({ severity: 'warn', summary: 'Nama responden wajib diisi', life: 3000 })
    return
  }
  if (!allAnswered.value) {
    toast.add({
      severity: 'warn',
      summary: 'Lengkapi semua pertanyaan',
      detail: `${answeredCount.value}/${totalQuestions.value} terjawab`,
      life: 3000,
    })
    return
  }
  submitting.value = true
  try {
    const t = await token()
    await api.post(
      '/survei/submit',
      {
        opd_id: opdId.value,
        tahun: info.value.tahun,
        nama_responden: nama.value.trim(),
        jabatan: jabatan.value,
        jawaban: answers.value,
      },
      authHeader(t),
    )
    await checkStatus() // kunci & tampilkan ringkasan
    toast.add({ severity: 'success', summary: 'Kuesioner terkirim', detail: 'Terima kasih atas partisipasi Anda.', life: 5000 })
    window.scrollTo({ top: 0, behavior: 'smooth' })
  } catch (e) {
    const msg = e.response?.data?.detail || e.message
    if (e.response?.status === 409) await checkStatus()
    toast.add({ severity: 'error', summary: 'Gagal mengirim', detail: msg, life: 6000 })
  } finally {
    submitting.value = false
  }
}

function fmtDate(iso) {
  if (!iso) return ''
  try {
    return new Date(iso).toLocaleString('id-ID', { dateStyle: 'long', timeStyle: 'short' })
  } catch {
    return iso
  }
}

onMounted(() => {
  loadPublic()
  onAuthStateChanged(auth, async (u) => {
    user.value = u
      ? { uid: u.uid, name: u.displayName, email: u.email, photo: u.photoURL }
      : null
    authReady.value = true
    status.value = null
    // Pra-isi nama responden dari akun Google (dapat diubah oleh responden).
    if (u && !nama.value) nama.value = u.displayName || ''
    if (u) await checkStatus()
  })
})
</script>

<template>
  <div class="survei-page">
    <header class="survei-top">
      <div class="brand">
        <i class="pi pi-shield" />
        <div>
          <div class="t">Survei Penilaian Lingkungan Pengendalian (CEE)</div>
          <div class="s">{{ info?.instansi || 'Pemerintah Kota Tegal' }} — Tahun {{ info?.tahun || '' }}</div>
        </div>
      </div>
      <div v-if="user" class="userbox">
        <img v-if="user.photo" :src="user.photo" referrerpolicy="no-referrer" />
        <span>{{ user.name || user.email }}</span>
        <Button icon="pi pi-sign-out" text rounded size="small" @click="doLogout" v-tooltip.bottom="'Keluar'" />
      </div>
    </header>

    <main class="survei-body">
      <!-- Belum login -->
      <div v-if="authReady && !user" class="login-card">
        <i class="pi pi-user-edit" style="font-size: 2.4rem; color: #3b82f6" />
        <h2>Masuk untuk Mengisi Survei</h2>
        <p class="muted">
          Survei ini ditujukan bagi pegawai di lingkungan Pemerintah Kota Tegal. Silakan masuk
          menggunakan akun Google Anda untuk mulai mengisi kuesioner.
          <br /><strong>Setiap akun hanya dapat mengisi survei satu kali dalam satu tahun.</strong>
        </p>
        <Button label="Masuk dengan Google" icon="pi pi-google" @click="doLogin" />
      </div>

      <!-- Sudah login & sudah mengisi: terkunci -->
      <div v-else-if="user && info && alreadySubmitted" class="form-wrap">
        <div class="done-card">
          <i class="pi pi-check-circle" style="font-size: 2.6rem; color: #16a34a" />
          <h2>Terima kasih, survei Anda sudah tercatat</h2>
          <p class="muted">
            Setiap akun hanya dapat mengisi survei <strong>satu kali dalam satu tahun</strong>.
            Berikut ringkasan jawaban Anda untuk Tahun {{ info.tahun }}.
          </p>
          <div class="summary">
            <div><span class="muted">Nama Responden</span><b>{{ status.nama_responden || '-' }}</b></div>
            <div><span class="muted">OPD</span><b>{{ status.opd_nama }}</b></div>
            <div><span class="muted">Jabatan</span><b>{{ status.jabatan || '-' }}</b></div>
            <div><span class="muted">Kode Responden</span><b>{{ status.kode_responden }}</b></div>
            <div><span class="muted">Waktu Pengisian</span><b>{{ fmtDate(status.submitted_at) }}</b></div>
          </div>
        </div>

        <!-- Jawaban read-only -->
        <div v-for="kat in kuesioner" :key="kat.id" class="card">
          <div class="kat-head">{{ kat.kode }}. {{ kat.nama }}</div>
          <div v-for="(p, i) in kat.pertanyaan" :key="p.id" class="q">
            <div class="q-text"><span class="q-no">{{ i + 1 }}.</span> {{ p.pertanyaan }}</div>
            <div class="q-opts">
              <span v-for="s in skala" :key="s.nilai" class="opt ro" :class="{ on: answers[p.id] === s.nilai }">
                <b>{{ s.nilai }}</b><span>{{ s.label }}</span>
              </span>
            </div>
          </div>
        </div>
      </div>

      <!-- Sudah login, belum mengisi: form -->
      <div v-else-if="user && info" class="form-wrap">
        <div class="card identity">
          <div style="flex: 1 1 100%">
            <label class="lbl">Nama Responden</label>
            <InputText v-model="nama" placeholder="Nama lengkap Anda" style="width: 100%" />
          </div>
          <div style="flex: 1">
            <label class="lbl">Organisasi Perangkat Daerah (OPD)</label>
            <Select
              v-model="opdId"
              :options="opdOptions"
              optionLabel="label"
              optionValue="value"
              filter
              placeholder="Pilih OPD Anda"
              style="width: 100%"
            />
          </div>
          <div style="flex: 1">
            <label class="lbl">Jabatan</label>
            <InputText v-model="jabatan" placeholder="cth: Kepala Subbagian" style="width: 100%" />
          </div>
        </div>

        <template v-if="opdId">
          <div class="progress">
            <div class="bar"><div :style="{ width: (answeredCount / totalQuestions) * 100 + '%' }" /></div>
            <span class="muted">{{ answeredCount }} / {{ totalQuestions }} terjawab</span>
          </div>

          <div v-for="kat in kuesioner" :key="kat.id" class="card">
            <div class="kat-head">{{ kat.kode }}. {{ kat.nama }}</div>
            <div v-for="(p, i) in kat.pertanyaan" :key="p.id" class="q">
              <div class="q-text"><span class="q-no">{{ i + 1 }}.</span> {{ p.pertanyaan }}</div>
              <div class="q-opts">
                <label v-for="s in skala" :key="s.nilai" class="opt" :class="{ on: answers[p.id] === s.nilai }">
                  <input type="radio" :name="'q' + p.id" :value="s.nilai" v-model="answers[p.id]" />
                  <b>{{ s.nilai }}</b><span>{{ s.label }}</span>
                </label>
              </div>
            </div>
          </div>

          <div class="submit-bar">
            <span class="muted" v-if="!allAnswered">Lengkapi semua pertanyaan untuk mengirim.</span>
            <span class="muted" v-else style="color: #16a34a"><i class="pi pi-check" /> Semua pertanyaan terjawab</span>
            <Button label="Kirim Jawaban" icon="pi pi-send" :loading="submitting" :disabled="!allAnswered" @click="submit" />
          </div>
          <p class="muted" style="text-align: center; font-size: 0.8rem; margin-top: 4px">
            Pastikan OPD &amp; jawaban sudah benar — jawaban hanya dapat dikirim satu kali per tahun.
          </p>
        </template>
        <div v-else class="muted" style="text-align: center; padding: 30px">
          Pilih OPD Anda untuk menampilkan pertanyaan.
        </div>
      </div>

      <div v-else class="muted" style="text-align: center; padding: 40px">Memuat…</div>
    </main>
  </div>
</template>

<style scoped>
.survei-page { min-height: 100vh; background: #f1f5f9; }
.survei-top {
  background: #0f172a; color: #fff; padding: 14px 22px;
  display: flex; align-items: center; gap: 14px; position: sticky; top: 0; z-index: 10;
}
.survei-top .brand { display: flex; align-items: center; gap: 12px; flex: 1; }
.survei-top .brand i { font-size: 1.6rem; color: #60a5fa; }
.survei-top .brand .t { font-weight: 700; }
.survei-top .brand .s { font-size: 0.78rem; color: #94a3b8; }
.userbox { display: flex; align-items: center; gap: 8px; font-size: 0.85rem; }
.userbox img { width: 30px; height: 30px; border-radius: 50%; }

.survei-body { max-width: 880px; margin: 0 auto; padding: 24px 16px 60px; }
.login-card {
  background: #fff; border: 1px solid #e2e8f0; border-radius: 14px; padding: 40px;
  text-align: center; max-width: 480px; margin: 60px auto; display: flex;
  flex-direction: column; align-items: center; gap: 12px;
}
.login-card h2 { margin: 4px 0; }
.muted { color: #64748b; }

.done-card {
  background: #fff; border: 1px solid #bbf7d0; border-radius: 14px; padding: 28px;
  text-align: center; display: flex; flex-direction: column; align-items: center; gap: 8px; margin-bottom: 16px;
}
.done-card h2 { margin: 4px 0; }
.summary {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px;
  width: 100%; margin-top: 12px; text-align: left;
}
.summary > div { background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 10px 12px; }
.summary span { display: block; font-size: 0.74rem; }
.summary b { font-size: 0.9rem; }

.card { background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 18px; margin-bottom: 16px; }
.identity { display: flex; gap: 16px; flex-wrap: wrap; }
.lbl { font-size: 0.8rem; color: #64748b; display: block; margin-bottom: 4px; }

.progress { display: flex; align-items: center; gap: 12px; margin: 4px 0 14px; }
.progress .bar { flex: 1; height: 8px; background: #e2e8f0; border-radius: 999px; overflow: hidden; }
.progress .bar div { height: 100%; background: #3b82f6; transition: width 0.2s; }

.kat-head { font-weight: 700; color: #0f172a; padding-bottom: 8px; margin-bottom: 8px; border-bottom: 2px solid #eff6ff; }
.q { padding: 12px 0; border-bottom: 1px dashed #e2e8f0; }
.q:last-child { border-bottom: none; }
.q-text { font-size: 0.9rem; margin-bottom: 8px; }
.q-no { color: #94a3b8; font-weight: 600; margin-right: 4px; }
.q-opts { display: flex; gap: 8px; flex-wrap: wrap; }
.opt {
  display: flex; align-items: center; gap: 6px; border: 1px solid #e2e8f0; border-radius: 8px;
  padding: 6px 12px; cursor: pointer; font-size: 0.82rem; user-select: none;
}
.opt:hover { border-color: #93c5fd; background: #f8fafc; }
.opt.on { border-color: #3b82f6; background: #eff6ff; color: #1d4ed8; }
.opt.ro { cursor: default; opacity: 0.65; }
.opt.ro.on { opacity: 1; border-color: #16a34a; background: #dcfce7; color: #166534; }
.opt input { display: none; }
.opt b { font-size: 0.95rem; }

.submit-bar {
  display: flex; align-items: center; justify-content: space-between; gap: 14px;
  background: #fff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 14px 18px;
  position: sticky; bottom: 14px; box-shadow: 0 6px 18px rgba(15, 23, 42, 0.08);
}
</style>
