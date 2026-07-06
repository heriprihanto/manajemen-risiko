import { defineStore } from 'pinia'
import api from '@/api'

const STORAGE_KEY = 'mr_context'

function loadSaved() {
  try {
    return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}
  } catch {
    return {}
  }
}

export const useContextStore = defineStore('context', {
  state: () => {
    const saved = loadSaved()
    return {
      opdList: [],
      opdId: saved.opdId || null,
      tahun: saved.tahun || new Date().getFullYear(),
      loaded: false,
    }
  },
  getters: {
    opd: (s) => s.opdList.find((o) => o.id_sub_pd === s.opdId) || null,
    ready: (s) => !!s.opdId && !!s.tahun,
  },
  actions: {
    async loadOpd(allowedOpds = []) {
      const { data } = await api.get('/master/opd')
      // Pengguna OPD (bukan Admin) hanya boleh melihat OPD miliknya.
      this.opdList = allowedOpds.length
        ? data.filter((o) => allowedOpds.includes(o.id_sub_pd))
        : data
      const ids = this.opdList.map((o) => o.id_sub_pd)
      if (!this.opdId || !ids.includes(this.opdId)) {
        this.opdId = ids[0] || null
      }
      this.loaded = true
      this.persist()
    },
    setOpd(id) {
      this.opdId = id
      this.persist()
    },
    setTahun(t) {
      this.tahun = t
      this.persist()
    },
    persist() {
      localStorage.setItem(
        STORAGE_KEY,
        JSON.stringify({ opdId: this.opdId, tahun: this.tahun }),
      )
    },
    get params() {
      return { opd_id: this.opdId, tahun: this.tahun }
    },
  },
})
