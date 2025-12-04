<template>
  <section class="w-full max-w-4xl mx-auto px-6 py-12">
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="text-red-500">{{ error }}</div>

    <div v-if="course && !loading" class="relative">
      
      <div v-if="!isLoggedIn" class="absolute inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-40 p-6 rounded-lg">
        <div class="max-w-md text-center text-white">
          <h3 class="text-xl font-semibold mb-3">Please sign in to view this course</h3>
          <p class="text-sm text-white/70 mb-4">Lessons and notes are available only for signed-in learners. Sign in or register to continue.</p>
          <div class="flex gap-3 justify-center">
            <button @click="goToLogin" class="btn bg-indigo-500 text-white">Login</button>
            <button @click="goToRegister" class="btn bg-yellow-400 text-black">Register</button>
          </div>
        </div>
      </div>

      <div class="grid md:grid-cols-4 gap-6">
        <!-- Sidebar: lesson list -->
        <aside class="md:col-span-1 bg-[rgba(255,255,255,0.02)] p-4 rounded-lg">
          <div class="flex items-center justify-between mb-4">
            <div>
              <div class="text-sm text-white/60">Course</div>
              <div class="font-semibold text-white">{{ course.title }}</div>
            </div>
            <div>
              <div v-if="onEnroll && !enrolled" @click="onEnroll(course.id)" class="px-3 py-1 rounded bg-teal-400 text-black text-xs">Enroll</div>
              <div v-else class="text-xs text-green-300">{{ enrolled ? 'Enrolled' : '' }}</div>
            </div>
          </div>

                <div class="text-xs text-white/60 mb-3">Lessons ({{ lessons.length }})</div>
                <div v-if="!enrolled">
                  <div class="text-sm text-white/70 mb-2">You need to enroll to view lessons.</div>
                  <div class="flex gap-2">
                    <button v-if="onEnroll" @click="handleEnroll" class="btn bg-teal-400">Enroll</button>
                    <button v-else @click="goToLogin" class="btn bg-indigo-500 text-white">Login</button>
                  </div>
                </div>
                <div v-else>
                  <div v-if="!showLessons.value" class="text-sm text-white/70 mb-2">You're enrolled. Click to start learning.</div>
                  <div v-if="!showLessons.value" class="flex gap-2">
                    <button @click="startLearning" class="btn bg-yellow-400 text-black">Start learning</button>
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
        <div class="md:col-span-3 bg-[rgba(255,255,255,0.01)] p-6 rounded-lg">
          <h2 class="text-2xl font-bold mb-2">{{ selectedLesson ? (selectedLesson.title) : course.title }}</h2>
          <div class="text-xs text-white/60 mb-4">{{ selectedLesson ? ('Lesson ' + selectedLesson.order + ' of ' + lessons.length) : course.excerpt || course.description }}</div>

          <div v-if="selectedLesson" class="space-y-4">
            <div v-if="selectedLesson.video_url" class="w-full bg-black rounded overflow-hidden">
              <iframe :src="selectedLesson.video_url" class="w-full h-64" frameborder="0" allowfullscreen></iframe>
            </div>

            <div class="text-sm text-white/80 bg-[rgba(255,255,255,0.02)] p-4 rounded">{{ selectedLesson.content }}</div>

            <!-- Notes list -->
            <div>
              <div class="text-sm text-white/60 mb-2">Notes</div>
              <ul class="space-y-2">
                <li v-for="note in notesMap[selectedLesson.id] || []" :key="note.id" class="bg-[rgba(255,255,255,0.03)] p-3 rounded">
                  <div v-if="editingNoteId === note.id">
                    <input v-model="editNoteTitle[note.id]" type="text" class="input mb-2" />
                    <textarea v-model="editNoteContent[note.id]" class="input h-24 mb-2"></textarea>
                    <div class="flex gap-2">
                      <button @click="saveEdit(note)" class="btn bg-indigo-500 text-white">Save</button>
                      <button @click="cancelEdit(note)" class="btn">Cancel</button>
                    </div>
                    <div v-if="noteErrors[note.id]" class="text-xs text-red-400 mt-2">{{ noteErrors[note.id] }}</div>
                  </div>
                  <div v-else>
                    <div class="text-sm font-semibold">{{ note.title || 'Note' }}</div>
                    <div class="text-xs text-white/60">{{ note.content }}</div>
                    <div class="text-xs text-white/50 mt-1">{{ new Date(note.created_at).toLocaleString() }}</div>
                    <div class="mt-2 flex items-center gap-2">
                      <button v-if="canEditNote(note)" @click="editNote(note)" class="text-xs text-indigo-300 hover:underline">Edit</button>
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
              <textarea v-model="newNoteContent[selectedLesson.id]" placeholder="Write a short note about this lesson..." class="input h-24 mb-2"></textarea>
              <div class="flex items-center gap-2">
                <button @click="submitNote(selectedLesson && selectedLesson.value ? selectedLesson.value : selectedLesson)" class="btn bg-indigo-500 text-white">Save note</button>
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
import { ref, onMounted, onUnmounted } from 'vue'
import axios from 'axios'
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
const noteErrors = ref({})
// tracks whether posting a note for a lesson failed because of auth
const noteRequiresLogin = ref({})

// editing state for notes
const editingNoteId = ref(null)
const editNoteTitle = ref({})
const editNoteContent = ref({})

// auth change handler (module scope so it can be removed cleanly)
function onAuthChange() {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

const selectedLesson = ref(null)
const enrolled = ref(false)

function selectLesson(lesson) {
  showLessons.value = true
  selectedLesson.value = lesson
  // ensure notes loaded
  loadNotes(lesson.id)
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
  } catch (e) {
    // ignore parse errors
  }
  // update auth state when other parts of the app change it
  window.addEventListener('authChanged', onAuthChange)
})

// cleanup listener when component is destroyed
onUnmounted(() => {
  window.removeEventListener('authChanged', onAuthChange)
})

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
  if (!content) {
    noteErrors.value[lesson.id] = 'Please enter note content.'
    return
  }
  try {
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await axios.post('/api/notes/', { lesson: lesson.id, title, content }, { headers })
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
  if (!content) {
    noteErrors.value[note.id] = 'Please provide note content.'
    return
  }
  try {
    const headers = {}
    const token = localStorage.getItem('access_token')
    if (token) headers['Authorization'] = `Bearer ${token}`
    const res = await axios.patch(`/api/notes/${note.id}/`, { title, content }, { headers })
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
</script>
