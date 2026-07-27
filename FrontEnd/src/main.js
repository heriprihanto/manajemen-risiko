import { createApp } from 'vue'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import Aura from '@primevue/themes/aura'
import { definePreset } from '@primevue/themes'
import ToastService from 'primevue/toastservice'
import ConfirmationService from 'primevue/confirmationservice'
import Tooltip from 'primevue/tooltip'

import 'primeicons/primeicons.css'
import './style.css'

import App from './App.vue'
import router from './router'

// Selaraskan warna primary PrimeVue (default Aura = emerald) dengan aksen
// biru pada shell aplikasi (lihat style.css --primary).
const AppPreset = definePreset(Aura, {
  semantic: {
    primary: {
      50: '#eff4ff', 100: '#dbe6fe', 200: '#bfd3fe', 300: '#93b4fd',
      400: '#608dfa', 500: '#3b82f6', 600: '#2563eb', 700: '#1d4ed8',
      800: '#1e40af', 900: '#1e3a8a', 950: '#172554',
    },
  },
})

const app = createApp(App)
app.use(createPinia())
app.use(router)
app.use(PrimeVue, {
  theme: { preset: AppPreset, options: { darkModeSelector: '.app-dark' } },
})
app.use(ToastService)
app.use(ConfirmationService)
app.directive('tooltip', Tooltip)
app.mount('#app')
