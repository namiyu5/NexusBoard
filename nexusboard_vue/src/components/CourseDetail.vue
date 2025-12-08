<template>
  <section class="w-full max-w-4xl mx-auto px-6 py-12">
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="course && !loading" class="relative">
      
      <div v-if="!isLoggedIn" class="absolute inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-40 p-6 rounded-lg">
          <div class="max-w-md text-center text-mb-muted">
            <h3 class="text-xl font-semibold mb-3 text-white">Please sign in to view this course</h3>
            <p class="text-sm text-mb-muted mb-4">Lessons and notes are available only for signed-in learners. Sign in or register to continue.</p>
            <div class="flex gap-3 justify-center">
              <button @click="goToLogin" class="btn bg-mb-primary text-[#071520]">Login</button>
              <button @click="goToRegister" class="btn bg-mb-secondary text-[#071520]">Register</button>
            </div>
          </div>
        </div>

      <div :class="selectedLesson ? 'min-h-screen flex flex-col md:flex-row' : 'grid md:grid-cols-4 gap-6'">
        <!-- Sidebar: lesson list -->
        <aside :class="selectedLesson ? 'w-full md:w-80 bg-mb-surface p-4 rounded-none md:rounded-l-lg h-[calc(100vh-4rem)] overflow-auto' : 'md:col-span-1 bg-mb-surface p-4 rounded-lg'">
          <div class="flex items-center justify-between mb-4">
            <div>
              <div class="text-sm text-mb-muted">Course</div>
              <div class="font-semibold text-white">{{ course.title }}</div>
            </div>
            <div>
              <div v-if="onEnroll && !enrolled" @click="onEnroll(course.id)" class="px-3 py-1 rounded bg-mb-primary text-[#071520] text-xs">Enroll</div>
              <div v-else class="text-xs text-mb-secondary">{{ enrolled ? 'Enrolled' : '' }}</div>
            </div>
          </div>

                <div class="text-xs text-mb-muted mb-3">Lessons ({{ lessons.length }})</div>
                <div v-if="!enrolled">
                  <div class="text-sm text-mb-muted mb-2">You need to enroll to view lessons.</div>
                  <div class="flex gap-2">
                    <button v-if="onEnroll" @click="handleEnroll" class="btn bg-mb-primary text-[#071520]">Enroll</button>
                    <button v-else @click="goToLogin" class="btn bg-mb-primary text-[#071520]">Login</button>
                  </div>
                </div>
                <div v-else>
                  <div v-if="previewMode && !showLessons.value" class="mb-3">
                    <div class="text-sm text-mb-muted mb-2">You're enrolled — preview</div>
                    <div class="font-semibold text-white text-lg">{{ course.title }}</div>
                    <div class="text-sm text-mb-muted mt-2 mb-3"><div v-html="processEmbeds(course.excerpt || course.description)"></div></div>
                    <div class="text-xs text-mb-muted mb-2">Lessons</div>
                    <ul class="text-sm space-y-1 mb-3 max-h-40 overflow-auto pr-2">
                      <li v-for="lesson in lessons" :key="lesson.id" class="text-white/80">{{ lesson.order }}. {{ lesson.title }}</li>
                      <li v-if="!lessons.length" class="text-xs text-white/60">No lessons yet.</li>
                    </ul>
                    <div class="flex gap-2">
                      <button @click="startLearning" class="btn bg-mb-primary text-[#071520]">Start</button>
                    </div>
                  </div>
                  <div v-else-if="!showLessons.value" class="text-sm text-mb-muted mb-2">You're enrolled. Click to start learning.</div>
                    <div v-else-if="!showLessons.value" class="flex gap-2">
                      <button @click="startLearning" class="btn bg-mb-secondary text-[#071520]">Start learning</button>
                    </div>
                  <ul v-if="showLessons.value" class="space-y-2 overflow-y-auto max-h-[60vh] pr-2">
                    <li v-for="lesson in lessons" :key="lesson.id" @click="selectLesson(lesson)" class="p-3 rounded cursor-pointer" :class="{'bg-white/5': selectedLesson && selectedLesson.id === lesson.id}">
                      <div class="flex items-center justify-between">
                        <div>
                          <div class="font-medium text-white text-sm">{{ lesson.order }}. {{ lesson.title }}</div>
                          <div class="text-xs text-white/60">{{ lesson.duration_minutes ? lesson.duration_minutes + ' min' : '' }}</div>
                        </div>
                        <div class="text-xs text-white/50">{{ lesson.published ? '●' : '' }}</div>
                      </div>
                    </li>
                    <li v-if="!lessons.length" class="text-xs text-white/60">No lessons yet.</li>
                  </ul>
                </div>
        </aside>

        <!-- Main: lesson content -->
        <div :class="selectedLesson ? 'flex-1 bg-mb-surface p-6 h-[calc(100vh-4rem)] overflow-auto rounded-none md:rounded-r-lg' : 'md:col-span-3 bg-mb-surface p-6 rounded-lg'">
          <div class="flex items-center justify-between mb-3">
            <div>
              <h2 class="text-2xl font-bold">{{ selectedLesson ? (selectedLesson.title) : course.title }}</h2>
              <div class="text-xs text-mb-muted mt-1">
                <template v-if="selectedLesson">{{ 'Lesson ' + selectedLesson.order + ' of ' + lessons.length }}</template>
                <template v-else><div v-html="processEmbeds(course.excerpt || course.description)"></div></template>
              </div>
            </div>
            <div class="w-40">
              <div class="text-xs text-mb-muted">Progress</div>
              <div class="w-full bg-white/5 rounded h-2 mt-1">
                <div :style="{ width: progressPercent + '%' }" class="h-2 rounded bg-mb-primary"></div>
              </div>
              <div class="text-xs text-right text-white/60 mt-1">{{ progressPercent }}%</div>
            </div>
          </div>

          <div v-if="selectedLesson" class="space-y-4">
            <div v-if="selectedLesson.video_url" class="w-full bg-black rounded overflow-hidden">
              <iframe :src="selectedLesson.video_url" class="w-full h-64" frameborder="0" allowfullscreen></iframe>
            </div>

            <div class="text-sm text-mb-muted bg-[rgba(255,255,255,0.02)] p-4 rounded"><div v-html="processEmbeds(selectedLesson.content)"></div></div>

            <!-- Navigation controls -->
            <div :class="selectedLesson ? 'mt-4 flex items-center justify-between gap-4 fixed left-0 right-0 bottom-6 mx-auto max-w-4xl px-4 z-50' : 'mt-4 flex items-center justify-between gap-4'">
              <button @click="goToPrev" :disabled="!hasPrev" class="btn w-full md:w-40" :class="!hasPrev ? 'opacity-50 cursor-not-allowed' : ''">Previous</button>
              <div class="flex-1 text-center text-xs text-mb-muted">{{ selectedLesson ? ('Lesson ' + selectedLesson.order + ' of ' + lessons.length) : '' }}</div>
              <button @click="goToNext" :disabled="!hasNext" class="btn w-full md:w-40 bg-mb-primary" :class="!hasNext ? 'opacity-50 cursor-not-allowed' : ''">{{ hasNext ? 'Next' : 'Finish course' }}</button>
            </div>

            <!-- Notes list -->
            <div>
              <div class="text-sm text-mb-muted mb-2">Notes</div>
              <ul class="space-y-2">
                <li v-for="note in notesMap[selectedLesson.id] || []" :key="note.id" class="bg-[rgba(255,255,255,0.03)] p-3 rounded">
                  <div v-if="editingNoteId === note.id">
                    <input v-model="editNoteTitle[note.id]" type="text" class="input mb-2" />
                    <WysiwygEditor v-model="editNoteContent[note.id]" />
                    <div class="flex gap-2">
                      <button @click="saveEdit(note)" class="btn bg-indigo-500 text-white">Save</button>
                      <button @click="cancelEdit(note)" class="btn">Cancel</button>
                    </div>
                    <div v-if="noteErrors[note.id]" class="text-xs text-red-400 mt-2">{{ noteErrors[note.id] }}</div>
                  </div>
                  <div v-else>
                    <div class="text-sm font-semibold text-mb-muted">{{ note.title || 'Note' }}</div>
                    <div class="text-xs text-mb-muted"><div v-html="processEmbeds(note.content)"></div></div>
                    <div class="text-xs text-white/50 mt-1">{{ new Date(note.created_at).toLocaleString() }}</div>
                    <div class="mt-2 flex items-center gap-2">
                      <button v-if="canEditNote(note)" @click="editNote(note)" class="text-xs text-mb-primary hover:underline">Edit</button>
                      <button v-if="canEditNote(note)" @click="deleteNote(note)" class="text-xs text-red-400 hover:underline">Delete</button>
                    </div>
                  </div>
                </li>
                <li v-if="!(notesMap[selectedLesson.id] && notesMap[selectedLesson.id].length)" class="text-xs text-white/60">No notes yet — be the first to add one.</li>
              </ul>
            </div>

            <!-- Add note form -->
              <div class="mt-3">
              <div class="text-sm text-white/60 mb-2">Add a note</div>
              <input v-model="newNoteTitle[selectedLesson.id]" type="text" placeholder="Title (optional)" class="input mb-2" />
              <WysiwygEditor v-model="newNoteContent[selectedLesson.id]" />
              <div class="flex items-center gap-2">
                <label class="text-sm mr-2 flex items-center gap-2"><input type="checkbox" v-model="newNoteIsPublic[selectedLesson.id]" /> <span>Public</span></label>
                <button @click="submitNote(selectedLesson)" class="btn bg-indigo-500 text-white">Save note</button>
                <div v-if="noteErrors[selectedLesson.id]" class="text-xs text-red-400">{{ noteErrors[selectedLesson.id] }}</div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import WysiwygEditor from './WysiwygEditor.vue'
import { useRoute } from 'vue-router'

// accept an optional `courseId` prop so this component can be used
// directly from App.vue or via a router route with params
const props = defineProps({
  courseId: {
    type: [String, Number],
    default: null,
  },
  // optional callback passed from parent to trigger enroll action
  onEnroll: {
    type: Function,
    default: null,
  },
})

const route = useRoute()
const id = props.courseId ?? route.params.id
const course = ref(null)
const lessons = ref([])
const loading = ref(true)
const error = ref(null)

const isLoggedIn = ref(!!localStorage.getItem('access_token'))
const showLessons = ref(false)

const notesMap = ref({})
const newNoteTitle = ref({})
const newNoteContent = ref({})
const newNoteIsPublic = ref({})
const noteErrors = ref({})
// tracks whether posting a note for a lesson failed because of auth
const noteRequiresLogin = ref({})

// editing state for notes
const editingNoteId = ref(null)
const editNoteTitle = ref({})
const editNoteContent = ref({})
const editNoteIsPublic = ref({})

// auth change handler (module scope so it can be removed cleanly)
function onAuthChange() {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

const selectedLesson = ref(null)
const enrolled = ref(false)
const previewMode = ref(false)

function selectLesson(lesson) {
  showLessons.value = true
  selectedLesson.value = lesson
  // ensure notes loaded
  loadNotes(lesson.id)
}

// navigation helpers
const hasPrev = computed(() => {
  if (!selectedLesson.value || !lessons.value.length) return false
  const idx = lessons.value.findIndex(l => l.id === selectedLesson.value.id)
  return idx > 0
})
const hasNext = computed(() => {
  if (!selectedLesson.value || !lessons.value.length) return false
  const idx = lessons.value.findIndex(l => l.id === selectedLesson.value.id)
  return idx !== -1 && idx < lessons.value.length - 1
})
const progressPercent = computed(() => {
  if (!selectedLesson.value || !lessons.value.length) return 0
  const idx = lessons.value.findIndex(l => l.id === selectedLesson.value.id)
  if (idx === -1) return 0
  return Math.round(((idx + 1) / lessons.value.length) * 100)
})

function goToPrev() {
  if (!hasPrev.value) return
  const idx = lessons.value.findIndex(l => l.id === selectedLesson.value.id)
  const prev = lessons.value[idx - 1]
  if (prev) selectLesson(prev)
}

function goToNext() {
  if (!hasNext.value) return
  const idx = lessons.value.findIndex(l => l.id === selectedLesson.value.id)
  const next = lessons.value[idx + 1]
  if (next) selectLesson(next)
}

async function handleEnroll() {
  if (typeof props.onEnroll === 'function') {
    try {
      await props.onEnroll(course.value.id)
    } catch (e) {
      // parent may redirect to login — ignore here
    }
  }
  enrolled.value = true
  showLessons.value = false
}

function startLearning() {
  if (lessons.value && lessons.value.length) {
    const first = lessons.value[0]
    selectLesson(first)
    // expose a small payload so parent/app can navigate to this course/lesson
    try {
      const payload = { courseId: course.value.id, lessonId: first.id }
      window.__startLearningPayload = payload
      try { localStorage.setItem('lastStart', JSON.stringify(payload)) } catch (e) { /* ignore */ }
      window.dispatchEvent(new CustomEvent('startLearning', { detail: payload }))
    } catch (e) {
      // ignore in non-browser or if dispatch fails
    }
  }
}

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
    // determine if current user is enrolled in this course
    try {
      const meRes = await axios.get('/api/me/').catch(() => null)
      const me = meRes && meRes.data ? meRes.data : null
      if (me) {
        const enr = await axios.get(`/api/enrollments/?course=${id}`)
        const arr = Array.isArray(enr.data) ? enr.data : (enr.data && enr.data.results) ? enr.data.results : []
        if (arr && arr.length) {
          const found = arr.find(e => e.user === me.id || e.user === me.username || (e.user && typeof e.user === 'object' && (e.user.id === me.id || e.user.username === me.username)))
          if (found) enrolled.value = true
        }
      }
    } catch (e) {
      // ignore
    }
    // don't auto-select a lesson; only reveal lessons when user starts learning
  } catch (err) {
    error.value = 'Failed to load course.'
    console.error(err)
  } finally {
    loading.value = false
  }
  // load notes for each lesson
  for (const lesson of lessons.value) {
    loadNotes(lesson.id)
    // initialize note input containers
    newNoteTitle.value[lesson.id] = ''
    newNoteContent.value[lesson.id] = ''
    noteErrors.value[lesson.id] = ''
  }
  // restore last-start payload if present and matches this course
  try {
    const last = JSON.parse(localStorage.getItem('lastStart') || 'null')
    if (last && last.courseId && Number(last.courseId) === Number(course.value.id)) {
      showLessons.value = true
      const lid = last.lessonId
      const found = lessons.value.find(l => Number(l.id) === Number(lid)) || lessons.value[0]
      if (found) selectLesson(found)
    }
    else if (enrolled.value && lessons.value.length) {
      // if user is enrolled and no last-start, select first lesson to begin
      selectLesson(lessons.value[0])
      showLessons.value = true
    }
  } catch (e) {
    // ignore parse errors
  }
  // update auth state when other parts of the app change it
  window.addEventListener('authChanged', onAuthChange)
  // listen for optimistic enrollment events from the parent/app
  window.addEventListener('enrolled', onEnrolled)
})

// cleanup listener when component is destroyed
onUnmounted(() => {
  window.removeEventListener('authChanged', onAuthChange)
  window.removeEventListener('enrolled', onEnrolled)
})

function onEnrolled(e) {
  try {
    const cid = e?.detail?.courseId
    if (!cid || !course.value) return
    if (Number(cid) === Number(course.value.id)) {
      enrolled.value = true
      previewMode.value = true
      showLessons.value = false
      // ensure lessons and notes are loaded so the preview shows titles
      for (const lesson of lessons.value) {
        loadNotes(lesson.id)
      }
    }
  } catch (err) {
    // ignore
  }
}

async function loadNotes(lessonId) {
  try {
    const res = await axios.get(`/api/notes/?lesson=${lessonId}`)
    notesMap.value[lessonId] = Array.isArray(res.data) ? res.data : (res.data.results || [])
  } catch (err) {
    notesMap.value[lessonId] = []
  }
}

async function submitNote(lesson) {
  noteErrors.value[lesson.id] = ''
  const title = (newNoteTitle.value[lesson.id] || '').trim()
  const content = (newNoteContent.value[lesson.id] || '').trim()
  const is_public = !!newNoteIsPublic.value[lesson.id]
  if (!content) {
    noteErrors.value[lesson.id] = 'Please enter note content.'
    return
  }
  try {
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await axios.post('/api/notes/', { lesson: lesson.id, title, content, is_public }, { headers })
    if (res.status === 201 || res.status === 200) {
      // prepend new note into map
      notesMap.value[lesson.id] = [res.data].concat(notesMap.value[lesson.id] || [])
      newNoteTitle.value[lesson.id] = ''
      newNoteContent.value[lesson.id] = ''
    } else {
      noteErrors.value[lesson.id] = 'Failed to save note.'
    }
  } catch (err) {
    const status = err?.response?.status
    if (status === 401 || status === 403) {
      noteRequiresLogin.value[lesson.id] = true
      noteErrors.value[lesson.id] = 'You must be logged in to add notes.'
    } else {
      noteErrors.value[lesson.id] = err?.response?.data?.detail || 'Error saving note.'
    }
  }
}

function canEditNote(note) {
  const username = localStorage.getItem('username') || ''
  return username && note.author && note.author === username
}

function editNote(note) {
  editingNoteId.value = note.id
  editNoteTitle.value[note.id] = note.title || ''
  editNoteContent.value[note.id] = note.content || ''
  editNoteIsPublic.value[note.id] = !!note.is_public
  noteErrors.value[note.id] = ''
}

function cancelEdit(note) {
  editingNoteId.value = null
  editNoteTitle.value[note.id] = ''
  editNoteContent.value[note.id] = ''
  noteErrors.value[note.id] = ''
}

async function saveEdit(note) {
  noteErrors.value[note.id] = ''
  const title = (editNoteTitle.value[note.id] || '').trim()
  const content = (editNoteContent.value[note.id] || '').trim()
  // allow editing public flag if UI exposes it (admins can change via AdminDashboard)
  const is_public = !!editNoteIsPublic?.value?.[note.id]
  if (!content) {
    noteErrors.value[note.id] = 'Please provide note content.'
    return
  }
  try {
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) headers['Authorization'] = `Bearer ${token}`
    const payload = { title, content }
    if (typeof is_public !== 'undefined') payload.is_public = is_public
    const res = await axios.patch(`/api/notes/${note.id}/`, payload, { headers })
    // update local map
    const arr = notesMap.value[selectedLesson.value.id] || []
    const idx = arr.findIndex(n => n.id === note.id)
    if (idx !== -1) arr.splice(idx, 1, res.data)
    notesMap.value[selectedLesson.value.id] = arr
    cancelEdit(note)
  } catch (err) {
    const status = err?.response?.status
    if (status === 401 || status === 403) {
      noteErrors.value[note.id] = 'You are not authorized to edit this note.'
    } else {
      noteErrors.value[note.id] = err?.response?.data?.detail || 'Error saving note.'
    }
  }
}

async function deleteNote(note) {
  if (!confirm('Delete this note?')) return
  try {
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) headers['Authorization'] = `Bearer ${token}`
    await axios.delete(`/api/notes/${note.id}/`, { headers })
    const arr = notesMap.value[selectedLesson.value.id] || []
    notesMap.value[selectedLesson.value.id] = arr.filter(n => n.id !== note.id)
    if (editingNoteId.value === note.id) cancelEdit(note)
  } catch (err) {
    noteErrors.value[note.id] = err?.response?.data?.detail || 'Error deleting note.'
  }
}

function goToLogin() {
  // Notify parent app to show inline login view
  try { window.dispatchEvent(new Event('showLogin')) } catch (e) { /* ignore */ }
}

function goToRegister() {
  try { window.dispatchEvent(new Event('showRegister')) } catch (e) { /* ignore */ }
}

function processEmbeds(html) {
  if (!html) return ''
  try {
    return html.replace(/<oembed[^>]*url=["']([^"']+)["'][^>]*>(?:<\/oembed>)?/gi, (m, url) => {
      let embedSrc = url
      if (/youtube\.com\/watch/.test(url) || /youtu\.be\//.test(url)) {
        const ytMatch = url.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{6,})/)
        const vid = ytMatch ? ytMatch[1] : null
        if (vid) embedSrc = `https://www.youtube.com/embed/${vid}`
      }
      return `\n<div class="media-embed" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;">\n  <iframe src="${embedSrc}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe>\n</div>\n`
    })
  } catch (err) {
    console.error('processEmbeds error', err)
    return html
  }
}
</script>
