<template>
  <section class="w-full py-12">
    <div class="max-w-7xl mx-auto px-6 grid grid-cols-1 md:grid-cols-2 gap-8 items-center">
      <div class="flex flex-col gap-6">
        <h1 class="text-4xl md:text-5xl font-extrabold">Your Learning Hub, Reimagined.</h1>
        <p class="text-lg text-white/80">Access courses, track progress, and learn smarter.</p>
        <div class="flex gap-4 mt-4">
          <button @click="$emit('navigate','/signup')" class="px-6 py-3 rounded-md bg-gradient-to-r from-indigo-500 to-pink-500 text-black font-semibold hover:scale-[1.02] transition">Get Started</button>
          <button @click="$emit('navigate','/login')" class="px-6 py-3 rounded-md bg-white/8 hover:bg-white/12">Login</button>
        </div>
      </div>
      <div class="hidden md:flex items-center justify-center">
        <div class="w-full max-w-md h-64 bg-white/5 rounded-xl flex items-center justify-center"> <!-- placeholder image -->
          <span class="text-white/60">[Illustration]</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
// emits: navigate
</script>

<style scoped></style>
