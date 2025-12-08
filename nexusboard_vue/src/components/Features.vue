<template>
  <section class="w-full py-6">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-4 gap-6">
      <div v-for="item in items" :key="item.title" class="p-6 card hover:shadow-xl transition">
        <div class="text-3xl mb-3">{{ item.icon }}</div>
        <h4 class="font-semibold text-white">{{ item.title }}</h4>
        <p class="text-sm muted mt-2">{{ item.desc }}</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'
const items = ref([
  { icon: '📚', title: 'Course Access', desc: 'Users can browse and view courses.' },
  { icon: '🛠️', title: 'Admin Tools', desc: 'Admins can create and manage courses.' },
  { icon: '📈', title: 'Progress Tracking', desc: 'Students see completion progress.' },
  { icon: '🔒', title: 'Secure Login', desc: 'JWT-based authentication.' },
])
</script>

<style scoped></style>
