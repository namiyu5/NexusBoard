<template>
  <header class="w-full bg-transparent py-6">
    <div class="max-w-7xl mx-auto px-6 flex items-center justify-between">
      <div class="flex items-center gap-4">
        <div class="w-10 h-10 bg-gradient-to-r from-indigo-500 to-pink-500 rounded-lg flex items-center justify-center font-extrabold">NB</div>
        <div class="text-lg font-bold">NexusBoard</div>
      </div>

      <nav class="hidden md:flex items-center gap-6 text-sm text-white/80">
        <component :is="linkTag" :to="'/'" :href="'/'" class="hover:text-white">Home</component>
        <component :is="linkTag" :to="'/about'" :href="'/about'" class="hover:text-white">About</component>
        <component :is="linkTag" :to="'/courses'" :href="'/courses'" class="hover:text-white">Courses</component>

        <div class="ml-6 flex items-center gap-3">
          <template v-if="!loggedIn">
            <component :is="linkTag" :to="'/login'" :href="'/login'" class="px-4 py-2 rounded-md bg-white/8 hover:bg-white/12">Login</component>
            <component :is="linkTag" :to="'/signup'" :href="'/signup'" class="ml-2 px-4 py-2 rounded-md bg-gradient-to-r from-indigo-500 to-pink-500 text-black font-semibold">Sign up</component>
          </template>
          <template v-else>
            <component :is="linkTag" :to="'/dashboard'" :href="'/dashboard'" class="px-3 py-2 rounded-md bg-white/6 hover:bg-white/10">Dashboard</component>
            <component v-if="isAdmin" :is="linkTag" :to="'/admin-dashboard'" :href="'/admin-dashboard'" class="px-3 py-2 rounded-md bg-white/6 hover:bg-white/10">Admin Panel</component>
            <button @click="$emit('logout')" class="ml-2 px-3 py-2 rounded-md bg-red-600 text-white">Logout</button>
          </template>
        </div>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { defineProps, computed } from 'vue'
const props = defineProps({
  loggedIn: { type: Boolean, default: false },
  isAdmin: { type: Boolean, default: false },
})

// Choose router-link if a router is present; otherwise use a plain anchor
const hasRouter = typeof window !== 'undefined' && (window.router || window.__VUE_ROUTER__)
const linkTag = computed(() => (hasRouter ? 'router-link' : 'a'))
</script>

<style scoped></style>
