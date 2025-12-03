<template>
  <section class="w-full max-w-4xl mx-auto px-6 py-12">
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="course && !loading">
      <h2 class="text-3xl font-bold mb-4">{{ course.title }}</h2>
      <p class="text-sm text-white/70 mb-4">{{ course.excerpt || course.description }}</p>
      <div class="space-y-4">
        <div v-for="lesson in lessons" :key="lesson.id" class="p-4 bg-[rgba(255,255,255,0.02)] rounded">
          <div class="flex justify-between">
            <div>
              <div class="font-semibold">{{ lesson.order }}. {{ lesson.title }}</div>
              <div class="text-xs text-white/60">{{ lesson.duration_minutes ? lesson.duration_minutes + ' min' : '' }}</div>
            </div>
            <div>
              <a :href="lesson.video_url" target="_blank" v-if="lesson.video_url" class="text-indigo-300">Watch</a>
            </div>
          </div>
          <p class="text-sm text-white/70 mt-2">{{ lesson.content }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()
const id = route.params.id
const course = ref(null)
const lessons = ref([])
const loading = ref(true)
const error = ref(null)

onMounted(async () => {
  try {
    const res = await axios.get(`/api/courses/${id}/`)
    course.value = res.data
    // If API returns nested lessons, use them; otherwise fetch lessons list filtered by course
    if (course.value.lessons && Array.isArray(course.value.lessons)) {
      lessons.value = course.value.lessons
    } else {
      const lres = await axios.get(`/api/lessons/?course=${id}`)
      lessons.value = Array.isArray(lres.data) ? lres.data : (lres.data.results || [])
    }
  } catch (err) {
    error.value = 'Failed to load course.'
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>
