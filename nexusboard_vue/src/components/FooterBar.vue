<template>
  <footer class="w-full py-8 border-t border-white/6">
    <div class="max-w-7xl mx-auto px-6 flex items-center justify-between text-sm text-mb-muted">
      <div>© {{ new Date().getFullYear() }} NexusBoard</div>
      <div class="flex items-center gap-4">
        <nav class="flex gap-3 items-center" aria-label="Footer social links">
          <a href="#" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="GitHub">
            <!-- GitHub SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M12 .5C5.73.5.75 5.48.75 11.75c0 4.92 3.19 9.09 7.61 10.56.56.1.77-.24.77-.54 0-.26-.01-1.12-.02-2.03-3.09.67-3.74-1.49-3.74-1.49-.51-1.29-1.25-1.64-1.25-1.64-1.02-.7.08-.69.08-.69 1.13.08 1.73 1.16 1.73 1.16 1.01 1.73 2.65 1.23 3.3.94.1-.73.39-1.23.71-1.51-2.47-.28-5.07-1.24-5.07-5.51 0-1.22.44-2.22 1.16-3-.12-.28-.5-1.4.11-2.92 0 0 .95-.3 3.12 1.16.9-.25 1.86-.37 2.82-.37.96 0 1.92.12 2.82.37 2.16-1.46 3.11-1.16 3.11-1.16.62 1.52.24 2.64.12 2.92.72.78 1.15 1.78 1.15 3 0 4.28-2.6 5.23-5.08 5.5.4.35.77 1.04.77 2.1 0 1.52-.01 2.74-.01 3.11 0 .3.21.65.78.54C19.06 20.84 22.25 16.67 22.25 11.75 22.25 5.48 17.27.5 11 .5z"/>
            </svg>
          </a>
          <a href="#" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="Instagram">
            <!-- Instagram SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M7 2C4.24 2 2 4.24 2 7v10c0 2.76 2.24 5 5 5h10c2.76 0 5-2.24 5-5V7c0-2.76-2.24-5-5-5H7zm0 2h10c1.66 0 3 1.34 3 3v10c0 1.66-1.34 3-3 3H7c-1.66 0-3-1.34-3-3V7c0-1.66 1.34-3 3-3zm5 2.5A4.5 4.5 0 1 0 16.5 11 4.5 4.5 0 0 0 12 6.5zm0 2A2.5 2.5 0 1 1 9.5 11 2.5 2.5 0 0 1 12 8.5zM18.5 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
            </svg>
          </a>
          <a href="#" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="Facebook">
            <!-- Facebook SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M22 12a10 10 0 1 0-11.5 9.95v-7.05H8.9V12h1.6V9.8c0-1.58.94-2.46 2.38-2.46.69 0 1.42.12 1.42.12v1.56h-.8c-.79 0-1.04.49-1.04.99V12h1.77l-.28 2.9h-1.49v7.05A10 10 0 0 0 22 12z"/>
            </svg>
          </a>
          <a href="#" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="X">
            <!-- X (Twitter) SVG -->
            <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
              <path d="M22.46 6c-.77.35-1.6.58-2.46.69a4.28 4.28 0 0 0 1.88-2.37 8.55 8.55 0 0 1-2.72 1.04 4.26 4.26 0 0 0-7.26 3.88A12.09 12.09 0 0 1 3.15 4.6a4.26 4.26 0 0 0 1.32 5.68c-.66-.02-1.28-.2-1.82-.5v.05c0 2.07 1.47 3.8 3.42 4.19-.36.1-.74.15-1.13.15-.28 0-.55-.03-.82-.07.55 1.73 2.15 2.99 4.05 3.02A8.56 8.56 0 0 1 2 19.54a12.07 12.07 0 0 0 6.54 1.92c7.85 0 12.15-6.5 12.15-12.14l-.01-.55A8.6 8.6 0 0 0 22.46 6z"/>
            </svg>
          </a>
        </nav>
        <div class="flex gap-4">
          <a href="#" class="hover:underline text-mb-muted">Privacy</a>
          <a href="#" class="hover:underline text-mb-muted">Terms</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup></script>

<style scoped></style>
