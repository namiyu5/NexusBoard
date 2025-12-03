<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-br from-neutral-900 via-slate-900 to-zinc-900 text-white">
    <!-- Navbar -->
    <header class="w-full py-4 border-b border-white/10">
      <div class="max-w-6xl mx-auto px-4 flex items-center justify-between">
              <div class="text-2xl font-bold">NexusBoard<img :src="logo" alt="NexusBoard Logo" class="inline-block ml-2 w-8 h-8"></div>
              <nav class="space-x-6">
          <button @click="view='home'" class="nav-btn">Home</button>
          <button @click="view='courses'" class="nav-btn">Courses</button>
          <button @click="view='notes'" class="nav-btn">Notes</button>
          <button @click="view='dashboard'" class="nav-btn">Dashboard</button>
          <button @click="view='login'" class="nav-btn">Login</button>
          <button @click="view='register'" class="nav-btn">Register</button>
        </nav>
      </div>
    </header>

    <!-- Main content -->
    <main class="flex-1 flex flex-col items-center justify-center px-6 py-12">
      <section v-if="view==='login'" class="w-full max-w-md">
  <div class="flex flex-col items-center mb-6">
    <h2 class="font-extrabold text-3xl md:text-4xl text-center text-yellow-300 drop-shadow-lg">
      Welcome Back
    </h2>
    <p class="text-sm md:text-lg text-center text-white/70 mt-2">
      Continue with your username and password
    </p>
  </div>

  <div class="flex flex-col gap-4">
    <input v-model="username" type="text"
           placeholder="Username"
           class="input" />
    <input v-model="password" type="password"
           placeholder="•••••••••••
           "
           class="input" />

    <div class="w-full flex justify-end">
      <a href="#" class="text-xs font-bold text-indigo-300 hover:underline">Forgot password?</a>
    </div>

    <button @click="submitLogin"
            class="btn w-full bg-gradient-to-r from-teal-400 to-indigo-500 text-black">
      Login
    </button>

    <p class="text-xs text-center text-white/70">
      Don’t have an account?
      <button @click="view='register'" class="font-bold text-indigo-300 hover:underline">
        Sign Up for FREE
      </button>
    </p>

    <p v-if="error" class="text-sm text-red-400 text-center">{{ error }}</p>
  </div>
</section>
<section v-if="view==='register'" class="w-full max-w-md">
  <div class="flex flex-col items-center mb-6">
    <h2 class="font-extrabold text-3xl md:text-4xl text-center text-yellow-300 drop-shadow-lg">
      Create Account
    </h2>
    <p class="text-sm md:text-lg text-center text-white/70 mt-2">
      Sign up to get started
    </p>
  </div>

  <div class="flex flex-col gap-4">
    <input v-model="regUsername" type="text"
           placeholder="Username"
           class="input" />
    <input v-model="regEmail" type="email"
           placeholder="you@example.com"
           class="input" />
    <input v-model="regPassword" type="password"
           placeholder="••••••••"
           class="input" />

    <button @click="submitRegister"
            class="btn w-full bg-gradient-to-r from-green-400 to-indigo-500 text-black">
      Create Account
    </button>

    <p class="text-xs text-center text-white/70">
      Already have an account?
      <button @click="view='login'" class="font-bold text-indigo-300 hover:underline">
        Sign in
      </button>
    </p>

    <p v-if="regError" class="text-sm text-red-400 text-center">{{ regError }}</p>
  </div>
</section>


      <!-- Home: polished UX-focused landing -->
      <section v-if="view==='home'" class="w-full max-w-6xl mx-auto px-6 py-12 space-y-10">
        <!-- Hero -->
        <div class="grid md:grid-cols-2 gap-8 items-center">
          <div class="space-y-6">
        <h1 class="text-4xl md:text-6xl font-extrabold leading-tight text-yellow-300">
          NexusBoard<br>
          For Learners,<br>
          By Learners
        </h1>
        <p class="text-lg text-white/80 max-w-2xl">
          NexusBoard is a community-first learning hub: find practical courses, publish brief notes,
          and collaborate with peers. Designed for fast progress and real-world skills.
        </p>

        <div class="flex gap-4 items-center">
          <button @click="view='courses'" class="cta-btn bg-yellow-400 text-indigo-900 shadow">
            Browse Courses
          </button>
          <button @click="view='register'" class="cta-btn bg-indigo-500 text-white shadow">
            Join Free
          </button>
          <button @click="view='login'" class="px-4 py-2 rounded-md text-sm text-white/80 border border-white/10 hover:bg-white/5">
            Sign in
          </button>
        </div>

        <div class="mt-4 flex gap-6 flex-wrap text-sm text-white/70">
          <div class="flex items-center gap-3">
            <div class="text-2xl font-bold text-white">{{ courses.length }}</div>
            <div>
          <div class="text-xs">Courses</div>
          <div class="text-xs text-white/60">Community-created</div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <div class="text-2xl font-bold text-white">{{ notes.length }}</div>
            <div>
          <div class="text-xs">Notes</div>
          <div class="text-xs text-white/60">Shared insights</div>
            </div>
          </div>

          <div class="flex items-center gap-3">
            <div class="text-2xl font-bold text-white">{{ Math.max(1200, enrolledCourses.length * 37) }}</div>
            <div>
          <div class="text-xs">Active learners</div>
          <div class="text-xs text-white/60">Engaged recently</div>
            </div>
          </div>
        </div>
          </div>

          <!-- Visual / Illustration block -->
          <div class="bg-[linear-gradient(135deg,#0f172a_0%,#04263a_100%)] rounded-2xl p-6 shadow-xl">
        <div class="flex flex-col gap-4">
          <div class="flex items-center justify-between">
            <div>
          <div class="text-sm text-white/60">Featured course</div>
          <div class="text-lg font-bold text-white">{{ featuredCourse.title }}</div>
            </div>
            <div class="text-xs text-white/60">6 weeks</div>
          </div>

          <p class="text-sm text-white/70">
            {{ featuredCourse.description }}
          </p>

          <div class="mt-4 grid grid-cols-2 gap-3">
            <button @click="openCourse(featuredCourse.id)" class="btn bg-teal-400 text-black">Start Learning</button>
            <button @click="enroll(featuredCourse.id)" class="btn bg-indigo-500 text-white">Enroll</button>
          </div>

          <div class="mt-5">
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
          </div>
        </div>

        <!-- Quick categories + featured carousel -->
        <div class="space-y-6">
          <div class="flex items-center justify-between">
        <h2 class="text-2xl font-bold text-white">Featured courses</h2>
        <div class="text-sm text-white/60">Handpicked for fast learning</div>
          </div>

          <div class="overflow-x-auto pb-2 -mx-6 px-6">
        <div class="flex gap-4 min-w-max">
          <article v-for="course in courses" :key="course.id" class="min-w-[260px] bg-[rgba(255,255,255,0.03)] rounded-xl p-5 shadow-sm">
            <div class="flex items-start justify-between gap-3">
          <div>
            <h3 class="text-lg font-semibold text-white">{{ course.title }}</h3>
            <p class="text-xs text-white/60 mt-1">{{ course.description }}</p>
          </div>
          <div class="text-xs text-white/50">{{ course.duration }}</div>
            </div>
            <div class="mt-4 flex gap-3">
          <button @click="openCourse(course.id)" class="px-3 py-2 rounded-md bg-yellow-400 text-indigo-900 text-sm font-semibold">Preview</button>
          <button @click="enroll(course.id)" class="px-3 py-2 rounded-md bg-teal-400 text-black text-sm font-semibold">Enroll</button>
            </div>
          </article>
        </div>
          </div>

          <!-- Categories -->
          <div class="flex flex-wrap gap-3">
        <button @click="view='courses'" class="px-4 py-2 rounded-full bg-white/5 text-sm text-white/90">Web Development</button>
        <button @click="view='courses'" class="px-4 py-2 rounded-full bg-white/5 text-sm text-white/90">Python</button>
        <button @click="view='courses'" class="px-4 py-2 rounded-full bg-white/5 text-sm text-white/90">Design</button>
        <button @click="view='courses'" class="px-4 py-2 rounded-full bg-white/5 text-sm text-white/90">Data Science</button>
        <button @click="view='courses'" class="px-4 py-2 rounded-full bg-white/5 text-sm text-white/90">Security</button>
          </div>
        </div>

        <!-- Social proof & testimonials -->
        <div class="grid md:grid-cols-3 gap-6">
          <div class="card">
        <div class="text-sm text-white/60">Why learners love NexusBoard</div>
        <div class="mt-3 font-semibold text-white">Short, practical lessons — built by the community.</div>
        <p class="text-xs text-white/60 mt-2">Real projects, quick wins, and helpful peers — join study groups and share notes that stick.</p>
          </div>

          <div class="card">
        <div class="text-xs text-white/60">Testimonials</div>
        <div class="mt-3 space-y-3">
          <div class="text-sm">
            <div class="font-semibold text-white">"Great for building practical skills quickly."</div>
            <div class="text-xs text-white/60">— Alex, Frontend dev</div>
          </div>
          <div class="text-sm">
            <div class="font-semibold text-white">"Notes are concise and super helpful."</div>
            <div class="text-xs text-white/60">— Priya, Data scientist</div>
          </div>
        </div>
          </div>

          <div class="card">
        <div class="text-xs text-white/60">Get started</div>
        <div class="mt-3 font-semibold text-white">Create your first note or enroll in a course</div>
        <div class="mt-4 flex gap-3">
          <button @click="view='notes'" class="btn bg-indigo-500 text-white">Write a note</button>
          <button @click="view='courses'" class="btn bg-yellow-400 text-indigo-900">Find a course</button>
        </div>
          </div>
        </div>
      </section>

      <!-- Courses -->
    <!-- Courses Page -->
<section v-if="view==='courses'" class="w-full max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-bold mb-8 text-center">Available Courses</h2>

  <!-- Courses Grid -->
  <div class="grid md:grid-cols-3 gap-8">
    <div v-for="course in courses" :key="course.id"
         class="bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition">
      <h3 class="text-xl font-semibold mb-2">{{ course.title }}</h3>
      <p class="text-sm text-white/70 mb-4">{{ course.description }}</p>
      <div class="flex justify-between items-center">
        <span class="text-xs text-white/50">Duration: {{ course.duration }}</span>
        <button @click="enroll(course.id)"
                class="px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300">
          Enroll
        </button>
      </div>
    </div>
  </div>
</section>


      <!-- Notes -->
      <!-- Notes Section -->
<section v-if="view==='notes'" class="w-full max-w-4xl">
  <h2 class="text-3xl font-bold mb-8">My Notes</h2>

  <!-- Create Note Form -->
  <div class="card mb-8">
    <h3 class="text-lg font-semibold mb-4">Create a new note</h3>
    <div class="flex flex-col gap-3">
      <input v-model="newNoteTitle" type="text"
             placeholder="Note title"
             class="input" />
      <textarea v-model="newNoteContent"
                placeholder="Write your note here..."
                class="input h-32"></textarea>
      <button @click="createNote"
              class="btn w-full">
        Save Note
      </button>
      <p v-if="noteError" class="text-sm text-red-400 text-center">{{ noteError }}</p>
    </div>
  </div>

  <!-- Notes List -->
  <ul class="space-y-4">
    <li v-for="note in notes" :key="note.id" class="card">
      <h3 class="text-lg font-semibold">{{ note.title }}</h3>
      <p class="text-sm text-white/70">{{ note.content }}</p>
    </li>
  </ul>
</section>


      <!-- Dashboard -->
      <section v-if="view==='dashboard'" class="w-full max-w-4xl">
        <h2 class="text-3xl font-bold mb-8">Dashboard</h2>
        <p class="text-white/80">Welcome back, {{ username || 'Guest' }}!</p>
        <div class="mt-6 grid md:grid-cols-2 gap-6">
          <div class="card">📚 Courses enrolled: {{ enrolledCourses.length }}</div>
          <div class="card">📝 Notes created: {{ notes.length }}</div>
        </div>
      </section>

      <!-- Login/Register (reuse your existing forms) -->
      <section v-if="view==='login' || view==='register'" class="w-full max-w-md">
        <!-- Insert your login/register forms here -->
      </section>
    </main>

    <!-- Footer -->
    <footer class="w-full py-6 border-t border-white/10 text-center text-white/60 text-sm">
      © 2025 NexusBoard Community — Built for learners, by learners
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import logo from './assets/favicon.ico'

const view = ref('home')
const username = ref('')
const courses = ref([])
const notes = ref([])
const enrolledCourses = ref([])

const featuredCourse = computed(() => (courses.value && courses.value.length) ? courses.value[0] : { id: null, title: '', description: '', duration: '' })

// Use Vite env when available; otherwise default to a relative path
// - In dev: set `VITE_API_BASE` to the Django backend (e.g. http://127.0.0.1:8000)
// - In production (served from Django/Heroku): leave unset so API calls are relative to current origin
const API_BASE = import.meta.env.VITE_API_BASE ?? ''

let pollHandle = null
const POLL_INTERVAL_MS = 8000

async function fetchData() {
  try {
    const [courseRes, notesRes] = await Promise.all([
      axios.get(`${API_BASE}/api/courses/`),
      // notes API may not exist yet on the backend; handle failure gracefully
      axios.get(`${API_BASE}/api/notes/`).catch(() => ({ data: [] })),
    ])
    // only replace if data changed (simple equality by length)
    if (Array.isArray(courseRes.data)) courses.value = courseRes.data
    if (Array.isArray(notesRes.data)) notes.value = notesRes.data
  } catch (err) {
    console.error('Error fetching data', err)
  }
}

onMounted(() => {
  // initial fetch
  fetchData()
  // poll for changes so admin-created courses appear automatically
  pollHandle = setInterval(fetchData, POLL_INTERVAL_MS)
})

onUnmounted(() => {
  if (pollHandle) clearInterval(pollHandle)
})

function openCourse(id) {
  view.value = 'dashboard'
  if (!enrolledCourses.value.includes(id)) enrolledCourses.value.push(id)
}

const newNoteTitle = ref('')
const newNoteContent = ref('')
const noteError = ref('')

async function createNote() {
  noteError.value = ''
  if (!newNoteTitle.value || !newNoteContent.value) {
    noteError.value = 'Please provide both a title and content.'
    return
  }
  try {
    const res = await axios.post(`${API_BASE}/api/notes/`, {
      title: newNoteTitle.value,
      content: newNoteContent.value,
    }, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access_token')}`
      }
    })
    if (res.status === 201) {
      notes.value.push(res.data) // add new note to list
      newNoteTitle.value = ''
      newNoteContent.value = ''
    } else {
      noteError.value = 'Failed to save note.'
    }
  } catch (err) {
    noteError.value = err?.response?.data?.detail || 'Error saving note.'
  }
}

function enroll(courseId) {
  // Later: POST to backend to enroll user
}

</script>

<style scoped>
.nav-btn {
  @apply text-sm text-white/80 hover:text-white transition;
}
.card {
  @apply bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition;
}
.btn {
  @apply px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300;
}
.cta-btn {
  @apply px-6 py-3 rounded-lg font-bold shadow-md transition;
}
.input {
  @apply bg-transparent border border-white/10 p-3 rounded-md outline-none text-lg text-white placeholder:text-white/40;
}
.card {
  @apply bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition;
}
.btn {
  @apply px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300 transition;
}
.card {
  @apply bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition;
}
.btn {
  @apply px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300 transition;
}

.input {
  @apply bg-[rgba(255,255,255,0.05)] border border-white/10 p-3 rounded-md outline-none 
         text-lg text-white placeholder:text-white/40 focus:ring-2 focus:ring-indigo-400 transition;
}

.btn {
  @apply px-6 py-3 rounded-lg font-bold shadow-md hover:opacity-90 transition;
}



</style> 