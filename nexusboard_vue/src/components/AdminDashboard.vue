<template>
  <section class="w-full max-w-6xl mx-auto px-6 py-12">
    <h2 class="text-2xl font-bold mb-6">Admin Dashboard</h2>

    <div class="mb-6 flex justify-between items-center">
      <div class="text-sm text-white/70">Manage courses</div>
      <div>
        <button @click="refresh" class="btn mr-2">Refresh</button>
        <button @click="creating = true" class="btn bg-yellow-400 text-indigo-900">New Course</button>
      </div>
    </div>

    <div v-if="creating" class="card mb-6">
      <h3 class="font-semibold mb-2">Create course</h3>
      <input v-model="newCourse.title" class="input mb-2" placeholder="Title" />
      <textarea v-model="newCourse.excerpt" class="input mb-2" placeholder="Excerpt"></textarea>
      <div class="flex gap-2">
        <button @click="createCourse" class="btn bg-indigo-500 text-white">Create</button>
        <button @click="cancelCreate" class="btn">Cancel</button>
      </div>
      <p v-if="createError" class="text-xs text-red-400 mt-2">{{ createError }}</p>
    </div>

    <div v-if="loading">Loading courses...</div>
    <div v-if="error" class="text-red-400">{{ error }}</div>

    <ul class="space-y-4">
      <li v-for="c in courses" :key="c.id" class="card">
        <div class="flex items-start justify-between">
          <div class="mt-3">
              <div class="text-xs text-white/60 mb-2">Recent notes from the community</div>
              <ul class="space-y-2">
          <li v-for="note in notes.slice(-3).reverse()" :key="note.id" class="flex items-start gap-3">
            <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-teal-400 flex items-center justify-center text-white font-semibold text-sm">
              {{ (note.title && note.title.length) ? note.title.charAt(0).toUpperCase() : 'N' }}
            </div>
            <div class="text-sm">
              <div class="font-semibold text-white truncate max-w-xs">{{ note.title }}</div>
              <div class="text-xs text-white/60 truncate max-w-xs">{{ note.content }}</div>
            </div>
          </li>
          <li v-if="!notes.length" class="text-xs text-white/60">No notes yet — be the first to share!</li>
            </ul>
          </div>
        </div>

        <div v-if="editingId === c.id" class="mt-4">
          <input v-model="editForm.title" class="input mb-2" />
          <textarea v-model="editForm.excerpt" class="input mb-2" rows="4"></textarea>
          <div class="flex gap-2 items-center">
            <label class="text-sm mr-2">Published</label>
            <input type="checkbox" v-model="editForm.published" />
            <button @click="saveEdit(c)" class="btn bg-indigo-500 text-white">Save</button>
            <button @click="cancelEdit" class="btn">Cancel</button>
          </div>
          <p v-if="editError" class="text-xs text-red-400 mt-2">{{ editError }}</p>
        </div>
      </li>
    </ul>

    <div v-if="selectedCourseId" class="mt-8">
      <h3 class="text-lg font-semibold mb-3">Manage Lessons for Course #{{ selectedCourseId }}</h3>
      <div class="card mb-4">
        <div class="flex gap-2 mb-3">
          <input v-model="lessonForm.title" class="input" placeholder="Lesson title" />
          <input v-model="lessonForm.order" type="number" class="input w-24" placeholder="Order" />
          <button @click="createLesson" class="btn bg-indigo-500 text-white">Add lesson</button>
          <button @click="clearLessonSelection" class="btn">Close</button>
        </div>
        <div v-if="lessonError" class="text-xs text-red-400">{{ lessonError }}</div>
        <div v-if="lessonLoading">Loading lessons...</div>
        <ul class="space-y-3">
          <li v-for="ls in lessons" :key="ls.id" class="p-3 bg-[rgba(255,255,255,0.02)] rounded">
            <div class="flex items-start justify-between">
              <div>
                <div class="font-semibold">{{ ls.order }}. {{ ls.title }} <span class="text-xs text-white/60">(#{{ ls.id }})</span></div>
                <div class="text-xs text-white/60">{{ ls.duration_minutes ? ls.duration_minutes + ' min' : '' }}</div>
              </div>
              <div class="flex flex-col items-end gap-2">
                <div class="flex gap-2">
                  <button @click="moveLessonUp(ls)" class="text-xs text-white/60">↑</button>
                  <button @click="moveLessonDown(ls)" class="text-xs text-white/60">↓</button>
                </div>
                <button @click="startEditLesson(ls)" class="text-xs text-indigo-300">Edit</button>
                <button @click="deleteLesson(ls)" class="text-xs text-red-400">Delete</button>
              </div>
            </div>
            <div v-if="editingLessonId === ls.id" class="mt-3">
              <input v-model="editLessonForm.title" class="input mb-2" />
              <textarea v-model="editLessonForm.content" class="input mb-2 h-28"></textarea>
              <div class="flex gap-2 items-center">
                <input v-model="editLessonForm.published" type="checkbox" /> <label class="text-sm mr-2">Published</label>
                <button @click="saveLessonEdit(ls)" class="btn bg-indigo-500 text-white">Save</button>
                <button @click="cancelLessonEdit" class="btn">Cancel</button>
              </div>
              <div v-if="editLessonError" class="text-xs text-red-400 mt-2">{{ editLessonError }}</div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import WysiwygEditor from './WysiwygEditor.vue'

const courses = ref([])
const loading = ref(false)
const error = ref('')
const enrollCounts = ref({})

const creating = ref(false)
const newCourse = ref({ title: '', excerpt: '' })
const createError = ref('')

const editingId = ref(null)
const editForm = ref({ title: '', excerpt: '', published: false })
const editError = ref('')

// lesson management
const selectedCourseId = ref(null)
const lessons = ref([])
const lessonLoading = ref(false)
const lessonError = ref('')
const lessonForm = ref({ title: '', order: 0, content: '' })
const editingLessonId = ref(null)
const editLessonForm = ref({ title: '', content: '', published: false })
const editLessonError = ref('')

async function fetchCourses() {
  loading.value = true
  error.value = ''
  try {
    const res = await axios.get('/api/courses/')
    courses.value = Array.isArray(res.data) ? res.data : (res.data && res.data.results) ? res.data.results : []
    // fetch enroll counts for each course (admins can view all enrollments)
    for (const c of courses.value) {
      try {
        const r = await axios.get(`/api/enrollments/?course=${c.id}`)
        const arr = Array.isArray(r.data) ? r.data : (r.data && r.data.results) ? r.data.results : []
        enrollCounts.value[c.id] = arr.length
      } catch (e) {
        enrollCounts.value[c.id] = 0
      }
    }
  } catch (err) {
    error.value = 'Failed to load courses.'
  } finally {
    loading.value = false
  }
}

function refresh() { fetchCourses() }

function cancelCreate() { creating.value = false; newCourse.value = { title: '', excerpt: '' }; createError.value = '' }

async function createCourse() {
  createError.value = ''
  if (!newCourse.value.title) { createError.value = 'Title required'; return }
  try {
    const res = await axios.post('/api/courses/', { title: newCourse.value.title, excerpt: newCourse.value.excerpt })
    if (res && (res.status === 201 || res.status === 200)) {
      courses.value.unshift(res.data)
      cancelCreate()
    }
  } catch (err) {
    createError.value = err?.response?.data?.detail || 'Create failed'
  }
}

function toggleEdit(c) {
  if (editingId.value === c.id) {
    editingId.value = null
  } else {
    editingId.value = c.id
    editForm.value = { title: c.title || '', excerpt: c.excerpt || '', published: !!c.published }
    editError.value = ''
  }
}

function manageLessons(c) {
  if (selectedCourseId.value === c.id) {
    clearLessonSelection()
    return
  }
  selectedCourseId.value = c.id
  fetchLessons(c.id)
}

function clearLessonSelection() {
  selectedCourseId.value = null
  lessons.value = []
  lessonForm.value = { title: '', order: 0, content: '' }
  lessonError.value = ''
  editingLessonId.value = null
}

async function fetchLessons(courseId) {
  lessonLoading.value = true
  lessonError.value = ''
  try {
    const res = await axios.get(`/api/lessons/?course=${courseId}`)
    lessons.value = Array.isArray(res.data) ? res.data : (res.data && res.data.results) ? res.data.results : []
    // sort by order to ensure ordering
    lessons.value.sort((a, b) => (a.order || 0) - (b.order || 0))
  } catch (err) {
    lessonError.value = 'Failed to load lessons.'
  } finally {
    lessonLoading.value = false
  }
}

async function createLesson() {
  lessonError.value = ''
  if (!lessonForm.value.title) { lessonError.value = 'Title required'; return }
  try {
    const payload = { title: lessonForm.value.title, order: lessonForm.value.order || 0, content: lessonForm.value.content, course: selectedCourseId.value }
    const res = await axios.post('/api/lessons/', payload)
    if (res && (res.status === 201 || res.status === 200)) {
      lessons.value.unshift(res.data)
      lessonForm.value = { title: '', order: 0, content: '' }
    }
  } catch (err) {
    lessonError.value = err?.response?.data?.detail || 'Create failed'
  }
}

function startEditLesson(ls) {
  editingLessonId.value = ls.id
  editLessonForm.value = { title: ls.title || '', content: ls.content || '', published: !!ls.published }
  editLessonError.value = ''
}

function cancelLessonEdit() { editingLessonId.value = null; editLessonForm.value = { title: '', content: '', published: false }; editLessonError.value = '' }

async function saveLessonEdit(ls) {
  editLessonError.value = ''
  try {
    const res = await axios.patch(`/api/lessons/${ls.id}/`, { title: editLessonForm.value.title, content: editLessonForm.value.content, published: editLessonForm.value.published })
    if (res && res.data) {
      const idx = lessons.value.findIndex(x => x.id === ls.id)
      if (idx !== -1) lessons.value.splice(idx, 1, res.data)
      cancelLessonEdit()
    }
  } catch (err) {
    editLessonError.value = err?.response?.data || 'Save failed'
  }
}

async function deleteLesson(ls) {
  if (!confirm('Delete lesson: ' + ls.title + ' ?')) return
  try {
    await axios.delete(`/api/lessons/${ls.id}/`)
    lessons.value = lessons.value.filter(x => x.id !== ls.id)
  } catch (err) {
    alert('Delete failed')
  }
}

async function moveLessonUp(ls) {
  // find index
  const idx = lessons.value.findIndex(x => x.id === ls.id)
  if (idx <= 0) return
  const prev = lessons.value[idx - 1]
  // swap orders
  try {
    const resA = await axios.patch(`/api/lessons/${ls.id}/`, { order: prev.order })
    const resB = await axios.patch(`/api/lessons/${prev.id}/`, { order: ls.order })
    // refresh list
    await fetchLessons(selectedCourseId.value)
  } catch (err) {
    alert('Reorder failed')
  }
}

async function moveLessonDown(ls) {
  const idx = lessons.value.findIndex(x => x.id === ls.id)
  if (idx === -1 || idx >= lessons.value.length - 1) return
  const next = lessons.value[idx + 1]
  try {
    await axios.patch(`/api/lessons/${ls.id}/`, { order: next.order })
    await axios.patch(`/api/lessons/${next.id}/`, { order: ls.order })
    await fetchLessons(selectedCourseId.value)
  } catch (err) {
    alert('Reorder failed')
  }
}

function cancelEdit() { editingId.value = null; editForm.value = { title: '', excerpt: '', published: false }; editError.value = '' }

async function saveEdit(c) {
  editError.value = ''
  try {
    const res = await axios.patch(`/api/courses/${c.id}/`, { title: editForm.value.title, excerpt: editForm.value.excerpt, published: editForm.value.published })
    if (res && res.data) {
      const idx = courses.value.findIndex(x => x.id === c.id)
      if (idx !== -1) courses.value.splice(idx, 1, res.data)
      cancelEdit()
    }
  } catch (err) {
    editError.value = err?.response?.data || 'Save failed'
  }
}

async function deleteCourse(c) {
  if (!confirm('Delete course: ' + c.title + ' ?')) return
  try {
    await axios.delete(`/api/courses/${c.id}/`)
    courses.value = courses.value.filter(x => x.id !== c.id)
  } catch (err) {
    alert('Delete failed')
  }
}

onMounted(() => { fetchCourses() })
// enrollments for admins
const enrollments = ref([])
const enrollLoading = ref(false)

async function fetchEnrollments() {
  enrollLoading.value = true
  try {
    const res = await axios.get('/api/enrollments/')
    enrollments.value = Array.isArray(res.data) ? res.data : (res.data && res.data.results) ? res.data.results : []
  } catch (err) {
    // ignore
  } finally {
    enrollLoading.value = false
  }
}

async function deleteEnrollment(en) {
  if (!confirm('Remove enrollment for ' + en.user + ' from course #' + en.course + ' ?')) return
  try {
    await axios.delete(`/api/enrollments/${en.id}/`)
    enrollments.value = enrollments.value.filter(x => x.id !== en.id)
    // refresh counts
    await fetchCourses()
  } catch (err) {
    alert('Failed to remove enrollment')
  }
}
</script>
