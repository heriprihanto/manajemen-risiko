<script setup>
import { computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Select from 'primevue/select'
import Button from 'primevue/button'
import Toast from 'primevue/toast'
import ConfirmDialog from 'primevue/confirmdialog'
import { useContextStore } from '@/stores/context'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const ctx = useContextStore()
const auth = useAuthStore()

function logout() {
  auth.logout()
  ctx.$reset()
  router.push({ name: 'login' })
}

const navGroups = [
  {
    label: 'Umum',
    items: [
      ['dashboard', 'Dashboard', 'pi-home'],
      ['laporan', 'Cetak Laporan', 'pi-print'],
    ],
  },
  {
    label: 'Lingkungan Pengendalian (CEE)',
    items: [
      ['form1a', 'Form 1.a Kuesioner', 'pi-list-check'],
      ['survei-hasil', 'Rincian Hasil Survei', 'pi-users'],
      ['form1b', 'Form 1.b Reviu Dokumen', 'pi-file-edit'],
      ['form1c', 'Form 1.c Simpulan CEE', 'pi-check-square'],
      ['form6', 'Form 6 RTP atas CEE', 'pi-wrench'],
    ],
  },
  {
    label: 'Penetapan Konteks',
    items: [
      ['form2a', 'Form 2.a Konteks Pemda', 'pi-building'],
      ['form2b', 'Form 2.b Strategis OPD', 'pi-sitemap'],
      ['form2c', 'Form 2.c Operasional OPD', 'pi-cog'],
    ],
  },
  {
    label: 'Penilaian Risiko',
    items: [
      ['form3', 'Form 3 Identifikasi', 'pi-flag'],
      ['form4', 'Form 4 Analisis', 'pi-chart-bar'],
      ['matriks', 'Matriks Risiko', 'pi-th-large'],
      ['form5', 'Form 5 Prioritas', 'pi-star'],
      ['form7', 'Form 7 RTP Risiko', 'pi-shield'],
    ],
  },
  {
    label: 'Komunikasi & Pemantauan',
    items: [
      ['form8', 'Form 8 Info & Komunikasi', 'pi-megaphone'],
      ['form9', 'Form 9 Rencana Pemantauan', 'pi-eye'],
      ['form10', 'Form 10 Monitoring Event', 'pi-history'],
    ],
  },
]

const opdOptions = computed(() =>
  ctx.opdList.map((o) => ({ label: o.nama_pd || o.nama_pd_singkat, value: o.id_sub_pd })),
)
const tahunOptions = computed(() => {
  const y = new Date().getFullYear()
  return [y + 1, y, y - 1, y - 2].map((t) => ({ label: String(t), value: t }))
})
const pageTitle = computed(() => route.meta.title || 'Manajemen Risiko')
const isPublic = computed(() => !!route.meta.public)

// Pemetaan modul -> bagian (section) pada halaman Laporan/Cetak.
// Modul di sini dicetak lewat laporan berformat resmi; sisanya (matriks,
// dashboard) dicetak apa adanya dari layar via window.print().
const laporanKey = {
  form1a: 'f1a', form1b: 'f1b', form1c: 'f1c', form6: 'f6',
  form2a: 'f2a', form2b: 'f2b', form2c: 'f2c',
  form3: 'f3', form4: 'f4', form5: 'f5', form7: 'f7',
  form8: 'f8', form9: 'f9', form10: 'f10',
}
// Tampilkan tombol Cetak di setiap modul kecuali halaman laporan itu sendiri.
const showCetak = computed(() => route.name !== 'laporan')
function cetak() {
  const key = laporanKey[route.name]
  if (key) router.push({ name: 'laporan', query: { form: key, print: 1 } })
  else window.print()
}
// OPD hanya bisa dipilih bebas oleh Admin / pengguna dengan >1 OPD.
const opdLocked = computed(() => !auth.isAdmin && ctx.opdList.length <= 1)

onMounted(() => {
  if (!isPublic.value) ctx.loadOpd(auth.allowedOpds)
})
</script>

<template>
  <!-- Halaman publik (survei) tampil tanpa shell admin -->
  <template v-if="isPublic">
    <router-view />
    <Toast position="top-right" />
  </template>

  <div v-else class="app-shell">
    <aside class="sidebar">
      <div class="brand">
        Manajemen Risiko
        <small>Pemerintah Kota Tegal — SPIP</small>
      </div>
      <template v-for="g in navGroups" :key="g.label">
        <div class="nav-group-label">{{ g.label }}</div>
        <router-link
          v-for="it in g.items"
          :key="it[0]"
          :to="{ name: it[0] }"
          custom
          v-slot="{ navigate, isActive }"
        >
          <div class="nav-item" :class="{ active: isActive }" @click="navigate">
            <i class="pi" :class="it[2]" />
            <span>{{ it[1] }}</span>
          </div>
        </router-link>
      </template>
      <a class="nav-item" href="/survei" target="_blank" style="margin-top: auto; border-top: 1px solid #1e293b">
        <i class="pi pi-external-link" />
        <span>Buka Survei Publik</span>
      </a>
    </aside>

    <div class="main">
      <header class="topbar">
        <div class="page-title">{{ pageTitle }}</div>
        <div class="ctx">
          <i class="pi pi-building muted" />
          <Select
            :modelValue="ctx.opdId"
            @update:modelValue="ctx.setOpd"
            :options="opdOptions"
            optionLabel="label"
            optionValue="value"
            filter
            placeholder="Pilih OPD"
            :disabled="opdLocked"
            style="width: 320px"
          />
          <Select
            :modelValue="ctx.tahun"
            @update:modelValue="ctx.setTahun"
            :options="tahunOptions"
            optionLabel="label"
            optionValue="value"
            style="width: 110px"
          />
          <div class="user-box">
            <i class="pi pi-user" />
            <span class="user-name">{{ auth.displayName }}</span>
            <small class="user-role">{{ auth.isAdmin ? 'Admin' : 'OPD' }}</small>
          </div>
          <Button
            v-if="showCetak"
            label="Cetak"
            icon="pi pi-print"
            size="small"
            severity="secondary"
            outlined
            v-tooltip.bottom="'Cetak modul ini'"
            @click="cetak"
          />
          <Button
            icon="pi pi-sign-out"
            severity="secondary"
            text
            rounded
            v-tooltip.bottom="'Keluar'"
            @click="logout"
          />
        </div>
      </header>
      <main class="content">
        <router-view v-if="ctx.loaded" :key="route.name + '-' + ctx.opdId + '-' + ctx.tahun" />
        <div v-else class="muted">Memuat data OPD…</div>
      </main>
    </div>
    <Toast position="top-right" />
    <ConfirmDialog />
  </div>
</template>

<style scoped>
.user-box {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  padding-left: 0.75rem;
  margin-left: 0.25rem;
  border-left: 1px solid #e2e8f0;
}
.user-box .pi-user {
  color: #64748b;
}
.user-name {
  font-weight: 600;
  font-size: 0.85rem;
  max-width: 160px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.user-role {
  color: #64748b;
  font-size: 0.72rem;
  background: #f1f5f9;
  padding: 0.05rem 0.4rem;
  border-radius: 6px;
}
</style>
