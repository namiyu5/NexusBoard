<template>
  <section class="w-full py-12 bg-mb-surface rounded-tl-2xl rounded-tr-2xl">
    <div class="max-w-7xl mx-auto px-6 text-center">
      <h3 class="text-2xl font-bold text-white">Ready to get started?</h3>
      <p class="muted mt-2">Create an account and start learning today.</p>
      <div class="mt-6">
        <button @click="$emit('navigate','/signup')" class="btn btn-primary">Create Account</button>
      </div>
    </div>
  </section>
</template>

<script setup>
// emits: navigate
</script>

<style scoped></style>
