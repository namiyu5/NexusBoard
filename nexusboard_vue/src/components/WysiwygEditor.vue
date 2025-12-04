<template>
  <div>
    <div :id="containerId" class="ck-container"></div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref, watch } from 'vue'
const props = defineProps({ modelValue: { type: String, default: '' } })
const emit = defineEmits(['update:modelValue'])

const containerId = `ck_${Math.random().toString(36).slice(2, 9)}`
let editor = null

onMounted(async () => {
  if (!window.ClassicEditor) {
    // load CKEditor 5 from CDN
    const s = document.createElement('script')
    s.src = 'https://cdn.ckeditor.com/ckeditor5/39.0.1/classic/ckeditor.js'
    s.defer = true
    document.head.appendChild(s)
    await new Promise((resolve) => { s.onload = resolve; s.onerror = resolve })
  }
  try {
    // eslint-disable-next-line no-undef
    editor = await window.ClassicEditor.create(document.getElementById(containerId))
    editor.setData(props.modelValue || '')
    editor.model.document.on('change:data', () => {
      const data = editor.getData()
      emit('update:modelValue', data)
    })
  } catch (e) {
    console.error('CKEditor init failed', e)
  }
})

onUnmounted(() => {
  if (editor) {
    editor.destroy().catch(() => {})
    editor = null
  }
})

watch(() => props.modelValue, (v) => {
  if (editor && typeof v === 'string' && editor.getData() !== v) {
    editor.setData(v || '')
  }
})
</script>

<style scoped>
.ck-container {
  min-height: 160px;
}
</style>
