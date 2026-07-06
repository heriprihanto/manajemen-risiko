<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import InputText from 'primevue/inputtext'
import Password from 'primevue/password'
import Button from 'primevue/button'
import Message from 'primevue/message'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function submit() {
  error.value = ''
  if (!username.value || !password.value) {
    error.value = 'Username dan password wajib diisi'
    return
  }
  loading.value = true
  try {
    await auth.login(username.value.trim(), password.value)
    const redirect = route.query.redirect || '/dashboard'
    router.push(redirect)
  } catch (e) {
    error.value = e.response?.data?.detail || 'Gagal login, coba lagi'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-wrap">
    <form class="login-card" @submit.prevent="submit">
      <div class="login-brand">
        <i class="pi pi-shield" />
        <div>
          <h1>Manajemen Risiko</h1>
          <p>Pemerintah Kota Tegal — SPIP</p>
        </div>
      </div>

      <Message v-if="error" severity="error" :closable="false">{{ error }}</Message>

      <label>Username</label>
      <InputText v-model="username" placeholder="Username" autofocus fluid />

      <label>Password</label>
      <Password
        v-model="password"
        placeholder="Password"
        :feedback="false"
        toggleMask
        fluid
        inputStyle="width:100%"
      />

      <Button
        type="submit"
        :loading="loading"
        label="Masuk"
        icon="pi pi-sign-in"
        class="login-btn"
      />
    </form>
  </div>
</template>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #0f172a, #1e293b);
  padding: 1rem;
}
.login-card {
  width: 100%;
  max-width: 380px;
  background: #fff;
  border-radius: 14px;
  padding: 2rem;
  box-shadow: 0 20px 45px rgba(0, 0, 0, 0.35);
  display: flex;
  flex-direction: column;
  gap: 0.55rem;
}
.login-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}
.login-brand .pi {
  font-size: 2rem;
  color: #2563eb;
}
.login-brand h1 {
  font-size: 1.15rem;
  margin: 0;
}
.login-brand p {
  margin: 0;
  font-size: 0.8rem;
  color: #64748b;
}
.login-card label {
  font-size: 0.82rem;
  font-weight: 600;
  color: #334155;
  margin-top: 0.35rem;
}
.login-btn {
  margin-top: 1.25rem;
}
</style>
