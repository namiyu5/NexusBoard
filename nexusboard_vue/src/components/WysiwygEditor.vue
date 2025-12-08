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
    // Compute theme colors from root CSS variables so editor matches theme
    const docStyle = getComputedStyle(document.documentElement)
    const bgVar = (docStyle.getPropertyValue('--mb-editor-bg') || '#0b0f14').trim()
    const fgVar = (docStyle.getPropertyValue('--mb-editor-fg') || '#e6eef8').trim()
    const contentStyle = `
      body { background: ${bgVar} !important; color: ${fgVar} !important; }
      p, h1, h2, h3, li, span { color: ${fgVar} !important; }
    `
    editor = await window.ClassicEditor.create(document.getElementById(containerId), { contentStyle })
    editor.setData(props.modelValue || '')
    editor.model.document.on('change:data', () => {
      const data = editor.getData()
      emit('update:modelValue', data)
    })
    // Ensure the editable element uses the dark theme (fixes cases where CSS isn't applied)
    try {
      const editableEl = editor.ui && typeof editor.ui.getEditableElement === 'function'
        ? editor.ui.getEditableElement()
        : document.querySelector(`#${containerId} .ck-editor__editable`)
      if (editableEl) {
        editableEl.style.background = bgVar || '#0b0f14'
        editableEl.style.color = fgVar || '#e6eef8'
        editableEl.style.padding = editableEl.style.padding || '0.6rem'
      }
      // Style toolbar if present
      const toolbar = document.querySelector(`#${containerId} .ck-toolbar`) || document.querySelector(`#${containerId} .ck-editor__top`)
      if (toolbar) toolbar.style.background = 'rgba(255,255,255,0.02)'

      // Observe mutations to the editable element and reapply styles if CKEditor resets them
      if (editableEl && window.MutationObserver) {
        const mo = new MutationObserver(() => {
          try {
            editableEl.style.background = bgVar || '#0b0f14'
            editableEl.style.color = fgVar || '#e6eef8'
          } catch (e) {}
        })
        mo.observe(editableEl, { attributes: true, attributeFilter: ['style', 'class'] })
        // store on editor instance so we can disconnect later
        editor.__mbMutationObserver = mo
      }
    } catch (e) {
      // non-fatal
    }
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
/* Force CKEditor editable area to dark background and readable white text */
.ck-container .ck-editor__editable,
.ck-container .ck-editor__editable_inline,
.ck-container .ck-content,
.ck-container .ck-editor__main {
  background: var(--mb-editor-bg, #0b0f14) !important;
  color: var(--mb-editor-fg, #ffffff) !important;
}
.ck-container .ck-content p,
.ck-container .ck-content h1,
.ck-container .ck-content h2,
.ck-container .ck-content h3,
.ck-container .ck-content li,
.ck-container .ck-content span {
  color: #ffffff !important;
}
.ck-container .ck-toolbar {
  background: rgba(255,255,255,0.02) !important;
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  white-space: nowrap;
}
.ck-container .ck-editor__top {
  border-bottom: 1px solid rgba(255,255,255,0.04) !important;
}
.ck-container .ck-placeholder {
  color: rgba(255,255,255,0.45) !important;
}

/* Responsive sizing for CKEditor editable area */
.ck-container {
  width: 100%;
  max-width: 100%;
  box-sizing: border-box;
  padding: 0.25rem;
}
.ck-container .ck-editor__editable {
  padding: 0.75rem !important;
  line-height: 1.6 !important;
}

@media (max-width: 640px) {
  .ck-container { min-height: 120px; }
  .ck-container .ck-editor__editable { font-size: 0.95rem !important; padding: 0.5rem !important; }
}

@media (min-width: 641px) and (max-width: 1024px) {
  .ck-container { min-height: 180px; }
  .ck-container .ck-editor__editable { font-size: 1rem !important; padding: 0.65rem !important; }
}

@media (min-width: 1025px) {
  .ck-container { min-height: 300px; }
  .ck-container .ck-editor__editable { font-size: 1.02rem !important; padding: 0.85rem !important; }
}

/* Respect reduced motion preferences */
@media (prefers-reduced-motion: reduce) {
  .ck-container .ck-content,
  .ck-container .ck-editor__editable {
    transition: none !important;
    animation: none !important;
  }
}

/* Ensure content elements inherit readable color */
.ck-container .ck-content p,
.ck-container .ck-content h1,
.ck-container .ck-content h2,
.ck-container .ck-content h3,
.ck-container .ck-content li,
.ck-container .ck-content span {
  color: var(--mb-editor-fg, #ffffff) !important;
}
</style>
