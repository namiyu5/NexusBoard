<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">Sign in to your account</h2>
      <form @submit.prevent="submitLogin" class="space-y-4">
        <input v-model="username" placeholder="Username" required class="w-full px-4 py-2 border rounded-md" />
        <input type="password" v-model="password" placeholder="Password" required class="w-full px-4 py-2 border rounded-md" />
        <button type="submit" class="w-full py-2 bg-indigo-600 text-white rounded-md">Sign in</button>
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
      </form>
      <p class="mt-4 text-sm text-gray-600">Don't have an account? <router-link to="/signup" class="text-indigo-600">Sign up</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

async function submitLogin() {
  error.value = ''
  try {
    const res = await axios.post('/api/auth/login/', {
      username: username.value,
      password: password.value
    })
    if (res && res.data) {
      localStorage.setItem('access_token', res.data.access || res.data.token)
      if (res.data.refresh) localStorage.setItem('refresh_token', res.data.refresh)
      router.push('/dashboard')
    } else {
      error.value = 'Unexpected server response'
    }
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Invalid credentials'
  }
}
</script>

<style scoped>
/* Tailwind handles styling */
</style>
