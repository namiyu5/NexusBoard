<template>
  <section class="w-full max-w-6xl mx-auto px-6 py-12">
    <h2 class="text-3xl font-bold mb-8 text-center">Available Courses</h2>
    <div v-if="loading" class="text-center">Loading...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>
    <div class="grid md:grid-cols-3 gap-8" v-if="!loading && !error">
      <div v-for="course in courses" :key="course.id" class="bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition">
        <h3 class="text-xl font-semibold mb-2">{{ course.title }}</h3>
        <p class="text-sm text-white/70 mb-4">{{ course.excerpt || course.description || '' }}</p>
        <div class="flex justify-between items-center">
          <span class="text-xs text-white/50">Lessons: {{ course.lessons ? course.lessons.length : '—' }}</span>
          <router-link :to="`/courses/${course.id}`" class="px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300">View</router-link>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const courses = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get('/api/courses/')
    courses.value = Array.isArray(res.data) ? res.data : (res.data.results || [])
  } catch (err) {
    error.value = 'Failed to load courses.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>
