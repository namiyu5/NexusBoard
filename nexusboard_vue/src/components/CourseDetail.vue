<template>
  <section class="w-full mx-auto">
    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center min-h-screen">
      <div class="text-center">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-500 mx-auto mb-4"></div>
        <p class="text-white/60">Loading course...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="error" class="max-w-2xl mx-auto px-6 py-12">
      <div class="bg-red-500/10 border border-red-500/30 rounded-lg p-6 text-center">
        <div class="text-4xl mb-3">⚠️</div>
        <p class="text-red-400 font-semibold mb-2">Error Loading Course</p>
        <p class="text-red-300/80 text-sm">{{ error }}</p>
      </div>
    </div>

    <div v-if="course && !loading" class="relative">
      <!-- Login Overlay -->
      <div v-if="!isLoggedIn" class="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50">
        <div class="max-w-md mx-4 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-white/10 rounded-2xl p-8 text-center">
          <div class="text-5xl mb-4">🔒</div>
          <h3 class="text-2xl font-bold mb-3 text-white">Sign In Required</h3>
          <p class="text-white/70 mb-6">Access exclusive course content, track your progress, and take notes by signing in to your account.</p>
          <div class="flex gap-3 justify-center">
            <button @click="goToLogin" class="btn bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-6 py-3">Login</button>
            <button @click="goToRegister" class="btn bg-white/10 text-white px-6 py-3 hover:bg-white/20">Register</button>
          </div>
        </div>
      </div>

      <!-- Course Overview (when no lesson selected) -->
      <div v-if="!selectedLesson" class="max-w-6xl mx-auto px-6 py-12">
        <!-- Back Button -->
        <button @click="$emit('back')" class="mb-6 text-white/60 hover:text-white flex items-center gap-2 transition">
          <span>←</span> Back to Courses
        </button>

        <!-- Course Header -->
        <div class="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border border-white/10 rounded-2xl p-8 mb-8">
          <div class="flex flex-col md:flex-row gap-8">
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-4">
                <span :class="['px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider', 
                  course.difficulty === 'beginner' ? 'bg-green-500/30 text-green-300' :
                  course.difficulty === 'intermediate' ? 'bg-yellow-500/30 text-yellow-300' :
                  'bg-red-500/30 text-red-300']">
                  {{ course.difficulty || 'Beginner' }}
                </span>
                <span v-if="enrolled" class="px-3 py-1 rounded-full text-xs font-bold bg-teal-500/30 text-teal-300">
                  ✓ Enrolled
                </span>
              </div>
              <h1 class="text-4xl font-bold text-white mb-4">{{ course.title }}</h1>
              <div class="text-white/70 text-lg leading-relaxed mb-6" v-html="processEmbeds(course.excerpt || course.description)"></div>
              
              <!-- Course Stats -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div class="bg-white/5 rounded-lg p-4">
                  <div class="text-2xl font-bold text-indigo-400">{{ lessons.length }}</div>
                  <div class="text-xs text-white/60 mt-1">Lessons</div>
                </div>
                <div class="bg-white/5 rounded-lg p-4">
                  <div class="text-2xl font-bold text-teal-400">{{ course.duration_hours || 'N/A' }}</div>
                  <div class="text-xs text-white/60 mt-1">Hours</div>
                </div>
                <div class="bg-white/5 rounded-lg p-4">
                  <div class="text-2xl font-bold text-purple-400">{{ progressPercent }}%</div>
                  <div class="text-xs text-white/60 mt-1">Progress</div>
                </div>
                <div class="bg-white/5 rounded-lg p-4">
                  <div class="text-2xl font-bold text-orange-400">{{ totalNotes }}</div>
                  <div class="text-xs text-white/60 mt-1">Your Notes</div>
                </div>
              </div>

              <!-- Action Buttons -->
              <div class="flex gap-3">
                <button v-if="!enrolled && onEnroll" @click="handleEnroll" 
                        class="btn bg-gradient-to-r from-teal-400 to-indigo-500 text-white px-8 py-3 text-lg font-semibold">
                  Enroll Now
                </button>
                <button v-else @click="startLearning" 
                        class="btn bg-gradient-to-r from-indigo-500 to-purple-500 text-white px-8 py-3 text-lg font-semibold">
                  {{ progressPercent > 0 ? 'Continue Learning' : 'Start Course' }}
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Course Curriculum -->
        <div class="bg-mb-surface border border-white/10 rounded-2xl p-8">
          <h2 class="text-2xl font-bold text-white mb-6">📚 Course Curriculum</h2>
          
          <div v-if="!enrolled" class="text-center py-12 bg-white/5 rounded-lg border border-white/10">
            <div class="text-4xl mb-3">🔒</div>
            <p class="text-white/60 mb-4">Enroll in this course to access all lessons</p>
            <button v-if="onEnroll" @click="handleEnroll" class="btn bg-indigo-500 text-white">
              Enroll Now
            </button>
          </div>

          <div v-else class="space-y-3">
            <div v-for="(lesson, index) in lessons" :key="lesson.id" 
                 @click="selectLesson(lesson)"
                 class="group bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg p-4 cursor-pointer transition-all duration-200">
              <div class="flex items-start gap-4">
                <div class="flex-shrink-0 w-12 h-12 rounded-full bg-gradient-to-br from-indigo-500/30 to-purple-500/30 flex items-center justify-center font-bold text-white">
                  {{ lesson.order }}
                </div>
                <div class="flex-1">
                  <h3 class="font-semibold text-white group-hover:text-indigo-300 transition mb-1">
                    {{ lesson.title }}
                  </h3>
                  <div class="flex items-center gap-4 text-sm text-white/60">
                    <span v-if="lesson.duration_minutes">⏱️ {{ lesson.duration_minutes }} min</span>
                    <span v-if="lesson.video_url">🎥 Video</span>
                    <span v-if="notesMap[lesson.id]?.length">📝 {{ notesMap[lesson.id].length }} notes</span>
                  </div>
                </div>
                <div class="flex-shrink-0">
                  <span class="text-indigo-400 group-hover:translate-x-1 transition-transform inline-block">→</span>
                </div>
              </div>
            </div>
            
            <div v-if="!lessons.length" class="text-center py-12 text-white/60">
              <div class="text-4xl mb-3">📭</div>
              <p>No lessons available yet. Check back soon!</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Lesson View (when lesson selected) -->
      <div v-else class="min-h-screen flex flex-col md:flex-row">
        <!-- Sidebar: lesson list -->
        <aside class="w-full md:w-80 bg-mb-surface border-r border-white/10 p-4 h-screen overflow-auto">
          <button @click="selectedLesson = null" class="mb-4 text-white/60 hover:text-white flex items-center gap-2 transition w-full">
            <span>←</span> Course Overview
          </button>

          <div class="mb-4 pb-4 border-b border-white/10">
            <div class="text-xs text-white/60 mb-1">Course</div>
            <div class="font-semibold text-white text-sm">{{ course.title }}</div>
          </div>

          <!-- Progress Bar -->
          <div class="mb-4 pb-4 border-b border-white/10">
            <div class="flex items-center justify-between text-xs text-white/60 mb-2">
              <span>Progress</span>
              <span class="font-semibold text-white">{{ progressPercent }}%</span>
            </div>
            <div class="w-full bg-white/10 rounded-full h-2">
              <div :style="{ width: progressPercent + '%' }" class="h-2 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all duration-300"></div>
            </div>
          </div>

          <!-- Lessons List -->
          <div class="text-xs text-white/60 mb-3 uppercase tracking-wider">Lessons ({{ lessons.length }})</div>
          <ul class="space-y-2">
            <li v-for="lesson in lessons" :key="lesson.id" 
                @click="selectLesson(lesson)" 
                :class="['p-3 rounded-lg cursor-pointer transition-all duration-200', 
                  selectedLesson.id === lesson.id 
                    ? 'bg-gradient-to-r from-indigo-500/30 to-purple-500/30 border border-indigo-500/50' 
                    : 'bg-white/5 hover:bg-white/10']">
              <div class="flex items-center gap-3">
                <div :class="['flex-shrink-0 w-6 h-6 rounded-full flex items-center justify-center text-xs font-bold',
                  selectedLesson.id === lesson.id ? 'bg-indigo-500 text-white' : 'bg-white/10 text-white/60']">
                  {{ lesson.order }}
                </div>
                <div class="flex-1 min-w-0">
                  <div class="font-medium text-white text-sm truncate">{{ lesson.title }}</div>
                  <div class="text-xs text-white/50">{{ lesson.duration_minutes ? lesson.duration_minutes + ' min' : 'N/A' }}</div>
                </div>
              </div>
            </li>
          </ul>
        </aside>

        <!-- Main: lesson content -->
        <div class="flex-1 bg-mb-bg overflow-auto">
          <div class="max-w-4xl mx-auto px-6 py-8">
            <!-- Lesson Header -->
            <div class="mb-6">
              <div class="flex items-center gap-2 text-sm text-white/60 mb-2">
                <span>Lesson {{ selectedLesson.order }} of {{ lessons.length }}</span>
                <span>•</span>
                <span>{{ selectedLesson.duration_minutes ? selectedLesson.duration_minutes + ' minutes' : '' }}</span>
              </div>
              <h2 class="text-3xl font-bold text-white mb-2">{{ selectedLesson.title }}</h2>
            </div>

            <!-- Video Player -->
            <div v-if="selectedLesson.video_url" class="mb-6 bg-black rounded-xl overflow-hidden shadow-2xl">
              <div class="relative" style="padding-bottom: 56.25%;">
                <iframe :src="getEmbedUrl(selectedLesson.video_url)" 
                        class="absolute inset-0 w-full h-full" 
                        frameborder="0" 
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                        allowfullscreen></iframe>
              </div>
            </div>

            <!-- Lesson Content -->
            <div class="bg-white/5 border border-white/10 rounded-xl p-6 mb-6">
              <div class="prose prose-invert max-w-none text-white/80 leading-relaxed" v-html="processEmbeds(selectedLesson.content)"></div>
            </div>

            <!-- Lesson Content -->
            <div class="bg-white/5 border border-white/10 rounded-xl p-6 mb-6">
              <div class="prose prose-invert max-w-none text-white/80 leading-relaxed" v-html="processEmbeds(selectedLesson.content)"></div>
            </div>

            <!-- Navigation controls -->
            <div class="flex items-center justify-between gap-4 mb-8 bg-white/5 border border-white/10 rounded-xl p-4">
              <button @click="goToPrev" :disabled="!hasPrev" 
                      :class="['btn flex-1 md:flex-none md:px-8', !hasPrev ? 'opacity-30 cursor-not-allowed' : 'hover:bg-white/10']">
                <span class="mr-2">←</span> Previous
              </button>
              <div class="hidden md:block text-center text-sm text-white/60">
                Lesson {{ selectedLesson.order }} of {{ lessons.length }}
              </div>
              <button @click="goToNext" :disabled="!hasNext" 
                      :class="['btn flex-1 md:flex-none md:px-8', 
                        !hasNext ? 'opacity-30 cursor-not-allowed' : 'bg-gradient-to-r from-indigo-500 to-purple-500 text-white hover:shadow-lg']">
                {{ hasNext ? 'Next' : 'Complete' }} <span class="ml-2">→</span>
              </button>
            </div>

            <!-- Notes Section -->
            <div class="bg-mb-surface border border-white/10 rounded-xl p-6">
              <h3 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
                <span>📝</span> Lesson Notes
              </h3>

              <!-- Existing Notes -->
              <div v-if="(notesMap[selectedLesson.id] || []).length > 0" class="mb-6 space-y-3">
                <div v-for="note in notesMap[selectedLesson.id]" :key="note.id" 
                     class="bg-white/5 border border-white/10 rounded-lg p-4 hover:border-indigo-500/30 transition">
                  <div v-if="editingNoteId === note.id">
                    <!-- Edit Mode -->
                    <input v-model="editNoteTitle[note.id]" 
                           type="text" 
                           placeholder="Note title"
                           class="input mb-3" />
                    <WysiwygEditor v-model="editNoteContent[note.id]" />
                    <label class="flex items-center gap-2 text-sm text-white/70 mt-3 bg-white/5 px-3 py-2 rounded">
                      <input type="checkbox" v-model="editNoteIsPublic[note.id]" class="rounded" />
                      <span>Make this note public</span>
                    </label>
                    <div class="flex gap-2 mt-3">
                      <button @click="saveEdit(note)" class="btn bg-green-500 text-white flex-1">
                        ✓ Save
                      </button>
                      <button @click="cancelEdit(note)" class="btn bg-white/10 text-white flex-1">
                        ✕ Cancel
                      </button>
                    </div>
                    <div v-if="noteErrors[note.id]" class="text-xs text-red-400 mt-2">{{ noteErrors[note.id] }}</div>
                  </div>
                  <div v-else>
                    <!-- View Mode -->
                    <div class="flex items-start justify-between mb-2">
                      <h4 class="font-semibold text-white">{{ note.title || 'Untitled Note' }}</h4>
                      <div class="flex items-center gap-2">
                        <button v-if="canEditNote(note)" @click="editNote(note)" 
                                class="text-xs text-indigo-400 hover:text-indigo-300 transition">
                          ✏️ Edit
                        </button>
                        <button v-if="canEditNote(note)" @click="deleteNote(note)" 
                                class="text-xs text-red-400 hover:text-red-300 transition">
                          🗑️ Delete
                        </button>
                      </div>
                    </div>
                    <div class="text-sm text-white/70 mb-2 prose prose-invert prose-sm max-w-none" v-html="processEmbeds(note.content)"></div>
                    <div class="flex items-center gap-3 text-xs text-white/50">
                      <span>{{ new Date(note.created_at).toLocaleDateString() }}</span>
                      <span v-if="note.is_public" class="px-2 py-0.5 rounded bg-teal-500/30 text-teal-300">Public</span>
                    </div>
                  </div>
                </div>
              </div>

              <div v-else class="mb-6 text-center py-8 bg-white/5 rounded-lg border border-dashed border-white/20">
                <div class="text-3xl mb-2">📝</div>
                <p class="text-white/60 text-sm">No notes yet. Be the first to add one!</p>
              </div>

              <!-- Add Note Form -->
              <div class="bg-gradient-to-br from-indigo-500/10 to-purple-500/10 border border-indigo-500/30 rounded-lg p-4">
                <h4 class="text-sm font-semibold text-white mb-3">Add Your Note</h4>
                <input v-model="newNoteTitle[selectedLesson.id]" 
                       type="text" 
                       placeholder="Note title (optional)" 
                       class="input mb-3" />
                <WysiwygEditor v-model="newNoteContent[selectedLesson.id]" />
                <div class="flex items-center gap-3 mt-3">
                  <label class="flex items-center gap-2 text-sm text-white/70 cursor-pointer hover:text-white transition">
                    <input type="checkbox" v-model="newNoteIsPublic[selectedLesson.id]" class="rounded" />
                    <span>Make this note public</span>
                  </label>
                  <button @click="submitNote(selectedLesson)" 
                          class="btn bg-gradient-to-r from-indigo-500 to-purple-500 text-white ml-auto px-6">
                    Save Note
                  </button>
                </div>
                <div v-if="noteErrors[selectedLesson.id]" class="text-xs text-red-400 mt-2">{{ noteErrors[selectedLesson.id] }}</div>
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

function onAuthChange() {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

const selectedLesson = ref(null)
const enrolled = ref(false)
const previewMode = ref(false)

function selectLesson(lesson) {
  showLessons.value = true
  selectedLesson.value = lesson
  // Load notes for the selected lesson
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

const totalNotes = computed(() => {
  return Object.values(notesMap.value).reduce((total, notes) => total + notes.length, 0)
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
    // Load lessons: use nested data if available, otherwise fetch separately
    if (course.value.lessons && Array.isArray(course.value.lessons)) {
      lessons.value = course.value.lessons
    } else {
      const lres = await axios.get(`/api/lessons/?course=${id}`)
      lessons.value = Array.isArray(lres.data) ? lres.data : (lres.data.results || [])
    }
    // Check enrollment status
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
      // ignore enrollment check errors
    }
    // Only reveal lessons when user starts learning
  } catch (err) {
    error.value = 'Failed to load course.'
    console.error(err)
  } finally {
    loading.value = false
  }
  // Load notes for each lesson
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
  editNoteIsPublic.value[note.id] = false
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

function getEmbedUrl(url) {
  if (!url) return ''
  
  // If already an embed URL, return as-is
  if (url.includes('/embed/')) return url
  
  // Convert YouTube watch URLs to embed format
  if (url.includes('youtube.com/watch')) {
    const match = url.match(/[?&]v=([A-Za-z0-9_-]{11})/)
    if (match) return `https://www.youtube.com/embed/${match[1]}`
  }
  
  // Convert youtu.be short URLs to embed format
  if (url.includes('youtu.be/')) {
    const match = url.match(/youtu\.be\/([A-Za-z0-9_-]{11})/)
    if (match) return `https://www.youtube.com/embed/${match[1]}`
  }
  
  // Return original URL for other video platforms
  return url
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
