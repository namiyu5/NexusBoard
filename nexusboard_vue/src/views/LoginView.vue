<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">Sign in to your account</h2>
      <form @submit.prevent="submitLogin" class="space-y-4">
        <input v-model="username" placeholder="Username" required class="w-full px-4 py-2 border rounded-md" />
        <input type="password" v-model="password" placeholder="Password" required class="w-full px-4 py-2 border rounded-md" />
        <button type="submit" class="w-full py-2 bg-indigo-600 text-white rounded-md">Sign in</button>
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
        <p v-if="success" class="text-sm text-green-600">{{ success }}</p>
      </form>
      <p class="mt-4 text-sm text-gray-600">Don't have an account? <router-link to="/signup" class="text-indigo-600">Sign up</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { setAuthTokens } from '../api.js'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const error = ref('')
const success = ref('')
const router = useRouter()

onMounted(() => {
  // If user already has an access token, redirect to home
  if (localStorage.getItem('access')) {
    router.push('/')
  }
})

async function submitLogin() {
  error.value = ''
  try {
    // Use SimpleJWT token obtain endpoint
    const res = await axios.post('/api/token/', {
      username: username.value,
      password: password.value,
    })
    if (res && res.data && res.data.access) {
      setAuthTokens(res.data.access, res.data.refresh)
      // store username so UI can display who is logged in
      localStorage.setItem('username', username.value)
      success.value = 'Signed in successfully.'
      // short delay so user sees the success message
      setTimeout(() => router.push('/'), 700)
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
