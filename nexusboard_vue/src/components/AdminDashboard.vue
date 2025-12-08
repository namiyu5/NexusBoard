<template>
  <section class="w-full max-w-6xl mx-auto px-6 py-12">
    <h2 class="text-2xl font-bold mb-6">Admin Dashboard</h2>

    <div class="mb-6 flex justify-between items-center">
      <div class="text-sm text-mb-muted">Manage courses</div>
      <div>
        <button @click="refresh" class="btn mr-2 text-mb-muted">Refresh</button>
        <button @click="creating = true" class="btn bg-mb-primary text-[#071520]">New Course</button>
        <a href="/admin/" target="_blank" class="btn ml-2 text-mb-muted">Legacy Admin</a>
      </div>
    </div>

    <div class="grid grid-cols-3 gap-4 mb-6">
      <div class="card p-4 bg-mb-surface">
        <div class="text-xs muted">Total users</div>
        <div class="text-2xl font-semibold">{{ stats.totals?.users ?? '—' }}</div>
      </div>
      <div class="card p-4">
        <div class="text-xs muted">Total courses</div>
        <div class="text-2xl font-semibold">{{ stats.totals?.courses ?? '—' }}</div>
      </div>
      <div class="card p-4">
        <div class="text-xs muted">Total enrollments</div>
        <div class="text-2xl font-semibold">{{ stats.totals?.enrollments ?? '—' }}</div>
      </div>
    </div>

    <div v-if="creating" class="card mb-6">
      <h3 class="font-semibold mb-2 text-mb-muted">Create course</h3>
      <input v-model="newCourse.title" class="input mb-2" placeholder="Title" />
      <WysiwygEditor v-model="newCourse.excerpt" />
      <div class="grid grid-cols-2 gap-2 mb-2">
        <div>
          <label class="text-sm text-mb-muted">Difficulty</label>
          <select v-model="newCourse.difficulty" class="input">
            <option value="beginner">Beginner</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
        </div>
        <div>
          <label class="text-sm text-mb-muted">Duration (hours)</label>
          <input v-model.number="newCourse.duration_hours" type="number" min="1" class="input" />
        </div>
      </div>
      <div class="flex gap-2">
        <button @click="createCourse" class="btn btn-primary">Create</button>
        <button @click="cancelCreate" class="btn btn-ghost">Cancel</button>
      </div>
      <p v-if="createError" class="text-xs text-red-400 mt-2">{{ createError }}</p>
    </div>

    <div v-if="loading">Loading courses...</div>
    <div v-if="error" class="text-red-400">{{ error }}</div>

    <ul class="space-y-4">
      <li v-for="c in courses" :key="c.id" class="card">
        <div class="flex items-start justify-between">
          <div class="mt-1">
            <div class="font-semibold text-lg text-mb-muted">{{ c.title }} <span class="text-xs text-mb-muted">(#{{ c.id }})</span></div>
            <div class="text-sm text-mb-muted mt-1 line-clamp-3" v-html="c.excerpt"></div>
            <div class="text-xs text-mb-muted mt-2">
              Enrollments: {{ enrollCounts[c.id] ?? 0 }} | 
              Difficulty: {{ c.difficulty || 'beginner' }} | 
              Duration: {{ c.duration_hours || 1 }} hours
            </div>
          </div>
          <div class="flex flex-col items-end gap-2">
            <div class="flex gap-2">
              <button @click="togglePublish(c)" class="text-xs" :class="c.published ? 'text-mb-secondary' : 'text-mb-muted'">{{ c.published ? 'Published' : 'Unpublished' }}</button>
              <button @click="manageLessons(c)" class="text-xs text-mb-primary">Lessons</button>
              <button @click="toggleEdit(c)" class="text-xs text-mb-muted">Edit</button>
              <button @click="deleteCourse(c)" class="text-xs text-red-400">Delete</button>
            </div>
          </div>
        </div>

        <div v-if="editingId === c.id" class="mt-4">
          <input v-model="editForm.title" class="input mb-2" />
          <WysiwygEditor v-model="editForm.excerpt" />
          <div class="grid grid-cols-2 gap-2 mb-2">
            <div>
              <label class="text-sm text-mb-muted">Difficulty</label>
              <select v-model="editForm.difficulty" class="input">
                <option value="beginner">Beginner</option>
                <option value="intermediate">Intermediate</option>
                <option value="advanced">Advanced</option>
              </select>
            </div>
            <div>
              <label class="text-sm text-mb-muted">Duration (hours)</label>
              <input v-model.number="editForm.duration_hours" type="number" min="1" class="input" />
            </div>
          </div>
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

    <div class="mt-8">
      <h3 class="text-lg font-semibold mb-3">User Management</h3>
      <div v-if="usersLoading" class="text-sm">Loading users...</div>
      <div v-if="usersError" class="text-sm text-red-400">{{ usersError }}</div>
      <ul class="space-y-2">
        <li v-for="u in users" :key="u.id" class="p-2 card flex justify-between items-center">
          <div>
            <div class="font-semibold text-white">{{ u.username }}</div>
            <div class="text-xs muted">id: {{ u.id }}</div>
          </div>
          <div class="flex gap-2 items-center">
            <button @click="toggleStaff(u)" class="text-xs" :class="u.is_staff ? 'text-mb-secondary' : 'muted'">{{ u.is_staff ? 'Staff' : 'Make Staff' }}</button>
            <button @click="toggleActive(u)" class="text-xs" :class="u.is_active ? 'text-mb-secondary' : 'text-red-400'">{{ u.is_active ? 'Active' : 'Deactivate' }}</button>
          </div>
        </li>
      </ul>
    </div>

    <div class="mt-8">
      <h3 class="text-lg font-semibold mb-3">Manage Notes</h3>
      <div v-if="notesLoading" class="text-sm">Loading notes...</div>
      <div v-if="notesError" class="text-sm text-red-400">{{ notesError }}</div>
      <ul class="space-y-3">
        <li v-for="n in notes" :key="n.id" class="p-3 card">
          <div v-if="adminEditingNoteId === n.id">
            <input v-model="adminEditNoteTitle[n.id]" class="input mb-2" />
            <WysiwygEditor v-model="adminEditNoteContent[n.id]" />
            <div class="flex gap-2 mt-2">
              <button @click="saveAdminNoteEdit(n)" class="btn btn-primary">Save</button>
              <button @click="cancelAdminNoteEdit" class="btn btn-ghost">Cancel</button>
            </div>
            <div v-if="adminEditNoteError" class="text-xs text-red-400 mt-2">{{ adminEditNoteError }}</div>
          </div>
          <div v-else class="flex items-start justify-between">
            <div>
              <div class="font-semibold text-white">{{ n.title || 'Note' }} <span class="text-xs muted">by {{ n.author }}</span></div>
              <div class="text-xs muted mt-1 line-clamp-3" v-html="n.content"></div>
              <div class="text-xs text-mb-muted mt-1">{{ new Date(n.created_at).toLocaleString() }}</div>
            </div>
            <div class="flex flex-col items-end gap-2">
              <div class="flex gap-2">
                <button @click="startAdminEditNote(n)" class="text-xs text-mb-primary">Edit</button>
                <button @click="deleteAdminNote(n)" class="text-xs text-red-400">Delete</button>
              </div>
            </div>
          </div>
        </li>
      </ul>
    </div>

    <div v-if="selectedCourseId" class="mt-8">
      <h3 class="text-lg font-semibold mb-3">Manage Lessons for Course #{{ selectedCourseId }}</h3>
      <div class="card mb-4">
        <div class="flex gap-2 mb-3">
          <input v-model="lessonForm.title" class="input" placeholder="Lesson title" />
          <input v-model="lessonForm.order" type="number" class="input w-24" placeholder="Order" />
          <button @click="createLesson" class="btn btn-primary">Add lesson</button>
          <button @click="clearLessonSelection" class="btn btn-ghost">Close</button>
        </div>
        <div v-if="lessonError" class="text-xs text-red-400">{{ lessonError }}</div>
        <div v-if="lessonLoading">Loading lessons...</div>
        <ul class="space-y-3">
          <li v-for="ls in lessons" :key="ls.id" class="p-3 card">
            <div class="flex items-start justify-between">
              <div>
                <div class="font-semibold text-white">{{ ls.order }}. {{ ls.title }} <span class="text-xs muted">(#{{ ls.id }})</span></div>
                <div class="text-xs muted">{{ ls.duration_minutes ? ls.duration_minutes + ' min' : '' }}</div>
              </div>
              <div class="flex flex-col items-end gap-2">
                <div class="flex gap-2">
                  <button @click="moveLessonUp(ls)" class="text-xs muted">↑</button>
                  <button @click="moveLessonDown(ls)" class="text-xs muted">↓</button>
                </div>
                <button @click="startEditLesson(ls)" class="text-xs text-mb-primary">Edit</button>
                <button @click="deleteLesson(ls)" class="text-xs text-red-400">Delete</button>
              </div>
            </div>
            <div v-if="editingLessonId === ls.id" class="mt-3">
              <input v-model="editLessonForm.title" class="input mb-2" />
              <WysiwygEditor v-model="editLessonForm.content" />
              <div class="flex gap-2 items-center">
                <input v-model="editLessonForm.published" type="checkbox" /> <label class="text-sm mr-2">Published</label>
                <button @click="saveLessonEdit(ls)" class="btn btn-primary">Save</button>
                <button @click="cancelLessonEdit" class="btn btn-ghost">Cancel</button>
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
const notes = ref([])

const creating = ref(false)
const newCourse = ref({ title: '', excerpt: '', difficulty: 'beginner', duration_hours: 1 })
const createError = ref('')

const editingId = ref(null)
const editForm = ref({ title: '', excerpt: '', published: false, difficulty: 'beginner', duration_hours: 1 })
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

async function fetchNotes() {
  notesLoading.value = true
  notesError.value = ''
  try {
    const res = await axios.get('/api/notes/')
    notes.value = Array.isArray(res.data) ? res.data : (res.data && res.data.results) ? res.data.results : []
  } catch (err) {
    notes.value = []
    console.error('fetchNotes error', err)
    const status = err?.response?.status
    const detail = err?.response?.data?.detail || err?.response?.data || err?.message
    if (status === 401) {
      notesError.value = 'Unauthorized. Please log in.'
      // optionally, prompt login globally
      window.dispatchEvent(new CustomEvent('showLogin'))
    } else {
      notesError.value = `Failed to load notes${status ? ' (status ' + status + ')' : ''}: ${detail || 'network error'}`
    }
  } finally {
    notesLoading.value = false
  }
}

function refresh() { fetchCourses() }

function cancelCreate() { creating.value = false; newCourse.value = { title: '', excerpt: '', difficulty: 'beginner', duration_hours: 1 }; createError.value = '' }

async function createCourse() {
  createError.value = ''
  if (!newCourse.value.title) { createError.value = 'Title required'; return }
  try {
    const res = await axios.post('/api/courses/', {
      title: newCourse.value.title,
      excerpt: newCourse.value.excerpt,
      difficulty: newCourse.value.difficulty,
      duration_hours: newCourse.value.duration_hours
    })
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
    editForm.value = {
      title: c.title || '',
      excerpt: c.excerpt || '',
      published: !!c.published,
      difficulty: c.difficulty || 'beginner',
      duration_hours: c.duration_hours || 1
    }
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
    // Sort lessons by order for correct sequence
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

function cancelEdit() { editingId.value = null; editForm.value = { title: '', excerpt: '', published: false, difficulty: 'beginner', duration_hours: 1 }; editError.value = '' }

async function saveEdit(c) {
  editError.value = ''
  try {
    const res = await axios.patch(`/api/courses/${c.id}/`, {
      title: editForm.value.title,
      excerpt: editForm.value.excerpt,
      published: editForm.value.published,
      difficulty: editForm.value.difficulty,
      duration_hours: editForm.value.duration_hours
    })
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

async function togglePublish(c) {
  try {
    const res = await axios.patch(`/api/courses/${c.id}/`, { published: !c.published })
    if (res && res.data) {
      const idx = courses.value.findIndex(x => x.id === c.id)
      if (idx !== -1) courses.value.splice(idx, 1, res.data)
    }
  } catch (err) {
    alert('Failed to update publish state')
  }
}

// admin data
const stats = ref({})
const users = ref([])
const usersLoading = ref(false)
const usersError = ref('')
const notesLoading = ref(false)
const notesError = ref('')
const adminEditingNoteId = ref(null)
const adminEditNoteTitle = ref({})
const adminEditNoteContent = ref({})
const adminEditNoteError = ref('')

async function fetchAdminData() {
  try {
    const res = await axios.get('/api/admin/stats/')
    stats.value = res.data || {}
  } catch (err) {
    // ignore or surface to UI
    stats.value = {}
  }
}

async function fetchUsers() {
  usersLoading.value = true
  usersError.value = ''
  try {
    const res = await axios.get('/api/admin/users/')
    users.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    usersError.value = 'Failed to load users.'
  } finally {
    usersLoading.value = false
  }
}

async function toggleStaff(u) {
  try {
    const res = await axios.patch(`/api/admin/users/${u.id}/`, { is_staff: !u.is_staff })
    if (res && res.data) {
      u.is_staff = res.data.is_staff
    }
  } catch (err) {
    alert('Failed to update staff flag')
  }
}

async function toggleActive(u) {
  try {
    const res = await axios.patch(`/api/admin/users/${u.id}/`, { is_active: !u.is_active })
    if (res && res.data) {
      u.is_active = res.data.is_active
    }
  } catch (err) {
    alert('Failed to update active flag')
  }
}

function startAdminEditNote(n) {
  adminEditingNoteId.value = n.id
  adminEditNoteTitle.value[n.id] = n.title || ''
  adminEditNoteContent.value[n.id] = n.content || ''
  adminEditNoteError.value = ''
}

function cancelAdminNoteEdit() {
  adminEditingNoteId.value = null
  adminEditNoteError.value = ''
}

async function saveAdminNoteEdit(n) {
  adminEditNoteError.value = ''
  try {
    const res = await axios.patch(`/api/notes/${n.id}/`, { title: adminEditNoteTitle.value[n.id], content: adminEditNoteContent.value[n.id] })
    if (res && res.data) {
      const idx = notes.value.findIndex(x => x.id === n.id)
      if (idx !== -1) notes.value.splice(idx, 1, res.data)
      adminEditingNoteId.value = null
    }
  } catch (err) {
    adminEditNoteError.value = err?.response?.data || 'Save failed'
  }
}

async function deleteAdminNote(n) {
  if (!confirm('Delete note by ' + n.author + '?')) return
  try {
    await axios.delete(`/api/notes/${n.id}/`)
    notes.value = notes.value.filter(x => x.id !== n.id)
  } catch (err) {
    alert('Delete failed')
  }
}

onMounted(() => { fetchCourses(); fetchNotes(); fetchAdminData(); fetchUsers(); fetchEnrollments() })
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
