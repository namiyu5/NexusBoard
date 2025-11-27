<template>
  <section class="w-full py-12 bg-gradient-to-r from-indigo-900 to-purple-800 rounded-tl-2xl rounded-tr-2xl">
    <div class="max-w-7xl mx-auto px-6 text-center">
      <h3 class="text-2xl font-bold">Ready to get started?</h3>
      <p class="text-white/80 mt-2">Create an account and start learning today.</p>
      <div class="mt-6">
        <button @click="$emit('navigate','/signup')" class="px-6 py-3 rounded-md bg-gradient-to-r from-teal-400 to-indigo-500 text-black font-semibold">Create Account</button>
      </div>
    </div>
  </section>
</template>

<script setup>
// emits: navigate
</script>

<style scoped></style>
