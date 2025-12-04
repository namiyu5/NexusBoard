<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full bg-white p-8 rounded-lg shadow">
      <h2 class="text-2xl font-semibold text-gray-800 mb-4">Create an account</h2>
      <form @submit.prevent="submitSignup" class="space-y-4">
        <input v-model="username" placeholder="Username" required class="w-full px-4 py-2 border rounded-md" />
        <input v-model="email" placeholder="Email" type="email" required class="w-full px-4 py-2 border rounded-md" />
        <input type="password" v-model="password" placeholder="Password" required class="w-full px-4 py-2 border rounded-md" />
        <button type="submit" class="w-full py-2 bg-indigo-600 text-white rounded-md">Sign up</button>
        <p v-if="error" class="text-sm text-red-600">{{ error }}</p>
        <p v-if="success" class="text-sm text-green-600">{{ success }}</p>
      </form>
      <p class="mt-4 text-sm text-gray-600">Already have an account? <router-link to="/login" class="text-indigo-600">Sign in</router-link></p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { setAuthTokens } from '../api.js'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
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

async function submitSignup() {
  error.value = ''
  try {
    const res = await axios.post('/api/auth/signup/', {
      username: username.value,
      email: email.value,
      password: password.value
    })
    if (res && (res.status === 201 || res.status === 200)) {
      // After successful signup, auto-login by requesting tokens
      try {
        const tokenRes = await axios.post('/api/token/', {
          username: username.value,
          password: password.value,
        })
        if (tokenRes && tokenRes.data && tokenRes.data.access) {
          setAuthTokens(tokenRes.data.access, tokenRes.data.refresh)
          localStorage.setItem('username', username.value)
          success.value = 'Account created and signed in.'
          setTimeout(() => router.push('/'), 700)
          return
        }
      } catch (e) {
        // If token obtain failed, fall back to redirecting to login
        console.warn('Auto-login after signup failed', e)
      }
      // fallback: notify user that account was created and send to login
      success.value = 'Account created. Please sign in.'
      setTimeout(() => router.push('/login'), 900)
    } else {
      error.value = 'Unexpected server response'
    }
  } catch (err) {
    error.value = err?.response?.data?.detail || 'Signup failed'
  }
}
</script>

<style scoped>
/* layout handled by Tailwind */
</style>

