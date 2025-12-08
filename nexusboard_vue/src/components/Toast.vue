<template>
  <div class="fixed top-4 right-4 z-50 pointer-events-none">
    <transition-group name="toast" tag="div" class="space-y-2">
      <div
        v-for="notification in notifications"
        :key="notification.id"
        :class="[
          'pointer-events-auto px-6 py-3 rounded-lg shadow-lg font-semibold max-w-sm animate-slide-in',
          notification.type === 'success' ? 'bg-green-500/90 text-white' : '',
          notification.type === 'error' ? 'bg-red-500/90 text-white' : '',
          notification.type === 'info' ? 'bg-blue-500/90 text-white' : '',
        ]"
      >
        <div class="flex items-center gap-3">
          <span v-if="notification.type === 'success'" class="text-xl">✓</span>
          <span v-else-if="notification.type === 'error'" class="text-xl">✕</span>
          <span v-else class="text-xl">ℹ</span>
          <span>{{ notification.message }}</span>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const notifications = ref([])
let notificationId = 0

/**
 * Show a toast notification
 * @param {string} message - The notification message
 * @param {string} type - Type: 'success', 'error', or 'info'
 * @param {number} duration - How long to show (ms), default 3000
 */
function showToast(message, type = 'info', duration = 3000) {
  const id = ++notificationId
  notifications.value.push({ id, message, type })

  setTimeout(() => {
    notifications.value = notifications.value.filter(n => n.id !== id)
  }, duration)
}

// Export functions for use in parent components
defineExpose({
  showToast,
})
</script>

<style scoped>
@keyframes slideIn {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

.animate-slide-in {
  animation: slideIn 0.3s ease-out;
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  transform: translateX(400px);
  opacity: 0;
}

.toast-leave-to {
  transform: translateX(400px);
  opacity: 0;
}
</style>
