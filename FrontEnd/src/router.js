import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'login', component: () => import('@/views/Login.vue'), meta: { title: 'Login', public: true, guestOnly: true } },
  { path: '/survei', name: 'survei', component: () => import('@/views/Survei.vue'), meta: { title: 'Survei CEE', public: true } },
  { path: '/dashboard', name: 'dashboard', component: () => import('@/views/Dashboard.vue'), meta: { title: 'Dashboard' } },
  { path: '/laporan', name: 'laporan', component: () => import('@/views/Laporan.vue'), meta: { title: 'Cetak Laporan / Print Preview' } },

  { path: '/form1a', name: 'form1a', component: () => import('@/views/Form1a.vue'), meta: { title: 'Form 1.a — Kuesioner CEE (Persepsi)' } },
  { path: '/form1b', name: 'form1b', component: () => import('@/views/Form1b.vue'), meta: { title: 'Form 1.b — Reviu Dokumen CEE' } },
  { path: '/form1c', name: 'form1c', component: () => import('@/views/Form1c.vue'), meta: { title: 'Form 1.c — Simpulan CEE' } },
  { path: '/survei-hasil', name: 'survei-hasil', component: () => import('@/views/SurveiHasil.vue'), meta: { title: 'Rincian Hasil Survei CEE' } },
  { path: '/form6', name: 'form6', component: () => import('@/views/Form6.vue'), meta: { title: 'Form 6 — RTP atas CEE' } },

  { path: '/form2a', name: 'form2a', component: () => import('@/views/Form2a.vue'), meta: { title: 'Form 2.a — Konteks Strategis Pemda' } },
  { path: '/form2b', name: 'form2b', component: () => import('@/views/Form2b.vue'), meta: { title: 'Form 2.b — Konteks Strategis OPD' } },
  { path: '/form2c', name: 'form2c', component: () => import('@/views/Form2c.vue'), meta: { title: 'Form 2.c — Konteks Operasional OPD' } },

  { path: '/form3a', name: 'form3a', component: () => import('@/views/Form3.vue'), props: { jenis: 'strategis_pemda' }, meta: { title: 'Form 3.a — Identifikasi Risiko Strategis Pemda' } },
  { path: '/form3b', name: 'form3b', component: () => import('@/views/Form3.vue'), props: { jenis: 'strategis_opd' }, meta: { title: 'Form 3.b — Identifikasi Risiko Strategis OPD' } },
  { path: '/form3c', name: 'form3c', component: () => import('@/views/Form3.vue'), props: { jenis: 'operasional_opd' }, meta: { title: 'Form 3.c — Identifikasi Risiko Operasional OPD' } },
  { path: '/form4', name: 'form4', component: () => import('@/views/Form4.vue'), meta: { title: 'Form 4 — Analisis Risiko' } },
  { path: '/matriks', name: 'matriks', component: () => import('@/views/Matriks.vue'), meta: { title: 'Matriks Risiko' } },
  { path: '/form5', name: 'form5', component: () => import('@/views/Form5.vue'), meta: { title: 'Form 5 — Daftar Risiko Prioritas' } },
  { path: '/form7', name: 'form7', component: () => import('@/views/Form7.vue'), meta: { title: 'Form 7 — RTP atas Risiko' } },

  { path: '/form8', name: 'form8', component: () => import('@/views/Form8.vue'), meta: { title: 'Form 8 — Informasi & Komunikasi' } },
  { path: '/form9', name: 'form9', component: () => import('@/views/Form9.vue'), meta: { title: 'Form 9 — Rencana Pemantauan PI' } },
  { path: '/form10', name: 'form10', component: () => import('@/views/Form10.vue'), meta: { title: 'Form 10 — Monitoring Risk Event & RTP' } },

  { path: '/kelola-kuesioner', name: 'kelola-kuesioner', component: () => import('@/views/KelolaKuesioner.vue'), meta: { title: 'Kelola Kuesioner CEE', admin: true } },
  { path: '/pengaturan', name: 'pengaturan', component: () => import('@/views/Pengaturan.vue'), meta: { title: 'Pengaturan Aplikasi', admin: true } },
]

const router = createRouter({
  // BASE_URL = '/manajemen-risiko/' saat produksi, '/' saat dev (lihat vite.config).
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

// Guard autentikasi: rute non-publik butuh token; rute guest (login) dialihkan
// bila sudah login. Impor store di dalam guard agar Pinia sudah terpasang.
router.beforeEach(async (to) => {
  const { useAuthStore } = await import('@/stores/auth')
  const auth = useAuthStore()
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'dashboard' }
  }
  if (!to.meta.public && !auth.isAuthenticated) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.admin && !auth.isAdmin) {
    return { name: 'dashboard' }
  }
  return true
})

export default router
