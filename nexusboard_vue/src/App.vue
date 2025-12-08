<template>
  <div class="flex flex-col min-h-screen bg-mb-bg text-white font-sans">
    <!-- Toast Notifications -->
    <Toast ref="toast" />

    <!-- Navbar -->
    <header class="w-full py-4 border-b border-white/6">
      <div class="max-w-6xl mx-auto px-4 flex items-center justify-between">
              <div class="text-2xl font-bold text-mb-muted">NexusBoard<img :src="logo" alt="NexusBoard Logo" class="inline-block ml-2 w-8 h-8"></div>
              <nav class="space-x-6">
          <button @click="view='home'" class="nav-btn text-mb-muted hover:text-white">Home</button>
          <button @click="view='courses'" class="nav-btn text-mb-muted hover:text-white">Courses</button>
          <button @click="view='notes'" class="nav-btn text-mb-muted hover:text-white">Notes</button>
          <button @click="view='dashboard'" class="nav-btn text-mb-muted hover:text-white">Dashboard</button>
          <button v-if="isAdmin" @click="view='admin'" class="nav-btn text-mb-muted hover:text-white">Admin</button>
          <template v-if="isLoggedIn">
            <span class="text-sm text-mb-muted mr-3">Logged in as {{ usernameDisplay }}</span>
            <button @click="logout" class="nav-btn text-mb-primary">Logout</button>
          </template>
          <template v-else>
            <button @click="goToLogin" class="nav-btn text-mb-primary">Login</button>
            <button @click="goToRegister" class="nav-btn text-mb-muted">Register</button>
          </template>
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
          placeholder="•••••••••••"
          class="input" />

    <div class="w-full flex justify-end">
      <a href="#" class="text-xs font-bold text-indigo-300 hover:underline">Forgot password?</a>
    </div>

    <button @click="submitLogin"
            class="btn w-full bg-gradient-to-r from-teal-400 to-indigo-500 text-black">
      Login
    </button>

    <p class="text-xs text-center text-white/70">
      Don't have an account?
      <button @click="view='register'" class="font-bold text-indigo-300 hover:underline">
        Sign Up for FREE
      </button>
    </p>
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
  </div>
</section>


     
      <section v-if="view==='home'" class="w-full starry-bg">
        <div class="max-w-6xl mx-auto px-6 py-12 space-y-10 starry-content">
          <!-- Hero -->
          <div class="grid md:grid-cols-2 gap-8 items-center">
            <div class="space-y-6">
              <h1 class="text-4xl md:text-6xl font-extrabold leading-tight text-mb-highlight">
                NexusBoard<br>
                For Learners,<br>
                By Learners
              </h1>
              <p class="text-lg text-mb-muted max-w-2xl">
                NexusBoard is a community-first learning hub: find practical courses, publish brief notes,
                and collaborate with peers. Designed for fast progress and real-world skills.
              </p>

              <div class="flex gap-4 items-center">
                <button @click="view='courses'" class="cta-btn btn btn-primary">Browse Courses</button>
                <button @click="view='register'" class="cta-btn btn btn-secondary">Join Free</button>
                <button @click="view='login'" class="btn-ghost">Sign in</button>
              </div>

              <div class="mt-4 flex gap-6 flex-wrap text-sm text-mb-muted">
                <div class="flex items-center gap-3">
                  <div class="text-2xl font-bold text-mb-muted">{{ courses.length }}</div>
                  <div>
                    <div class="text-xs">Courses</div>
                    <div class="text-xs text-white/60">Community-created</div>
                  </div>
                </div>

                <div class="flex items-center gap-3">
                  <div class="text-2xl font-bold text-mb-muted">{{ notes.length }}</div>
                  <div>
                    <div class="text-xs">Notes</div>
                    <div class="text-xs text-white/60">Shared insights</div>
                  </div>
                </div>

                <div class="flex items-center gap-3">
                  <div class="text-2xl font-bold text-mb-muted">{{ Math.max(1200, enrolledCourses.length * 37) }}</div>
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

                <p class="text-sm text-white/70">{{ featuredCourse.description }}</p>

                <div class="mt-4 grid grid-cols-2 gap-3">
                  <button @click="openCourse(featuredCourse.id)" class="btn btn-primary">Start Learning</button>
                  <button @click="enroll(featuredCourse.id)" class="btn btn-secondary">Enroll</button>
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

         
          <div class="space-y-6">
            <div class="flex items-center justify-between">
              <h2 class="text-2xl font-bold text-white">Featured courses</h2>
              <div class="text-sm text-white/60">Handpicked for fast learning</div>
            </div>

            <div class="overflow-x-auto pb-2 -mx-6 px-6">
              <div class="flex gap-4 min-w-max">
                <article v-for="course in courses" :key="course.id" class="min-w-[280px] bg-gradient-to-tr from-[rgba(255,255,255,0.02)] to-[rgba(255,255,255,0.01)] rounded-2xl p-5 shadow-sm hover:shadow-lg transition">
                  <div class="flex items-start justify-between gap-3">
                    <div class="flex-1 pr-3">
                      <h3 class="text-lg font-semibold text-white truncate">{{ course.title }}</h3>
                      <p class="text-xs text-white/60 mt-2 line-clamp-3">{{ course.description }}</p>
                      <div class="mt-3 flex items-center gap-3 text-xs text-white/60">
                        <div class="px-2 py-1 bg-white/5 rounded-full">{{ course.lessons ? course.lessons.length : '—' }} lessons</div>
                        <div class="px-2 py-1 bg-white/5 rounded-full">{{ course.duration || 'Self-paced' }}</div>
                        <div class="px-2 py-1 rounded-full text-xs" :class="course.level ? 'bg-white/3' : ''">{{ course.level || 'Level: N/A' }}</div>
                      </div>
                    </div>
                    <div class="flex flex-col items-end gap-3">
                      <div v-if="enrolledCourses.includes(course.id)" class="text-xs text-green-300 font-semibold">Enrolled</div>
                      <div class="text-xs text-white/50">{{ course.level || '' }}</div>
                    </div>
                  </div>
                  <div class="mt-4 flex gap-3 items-center">
                    <button @click="openCourse(course.id)" class="btn btn-ghost text-mb-muted" aria-label="View course {{ course.title }}">View course</button>
                    <button @click="enroll(course.id)" class="btn btn-primary" :class="{'opacity-60 cursor-not-allowed': enrolledCourses.includes(course.id)}" :disabled="enrolledCourses.includes(course.id)">
                      {{ enrolledCourses.includes(course.id) ? 'Go to course' : 'Start learning' }}
                    </button>
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
             class="input"
             aria-label="Note title" />
      <textarea v-model="newNoteContent"
                placeholder="Write your note here..."
                class="input h-32"
                aria-label="Note content"></textarea>
      <button @click="createNote"
              class="btn w-full"
              aria-label="Save note">
        Save Note
      </button>
    </div>
  </div>

  <!-- Notes List -->
  <div v-if="notes.length === 0" class="text-center text-white/60 py-8">
    <p>No notes yet. Create your first note above!</p>
  </div>
  <ul v-else class="space-y-4">
    <li v-for="note in notes" :key="note.id" class="card">
      <div v-if="editingNoteId !== note.id" class="flex justify-between items-start">
        <div class="flex-1">
          <h3 class="text-lg font-semibold">{{ note.title }}</h3>
          <p class="text-sm text-white/70 mt-2">{{ note.content }}</p>
          <p class="text-xs text-white/50 mt-3">
            Created: {{ new Date(note.created_at).toLocaleDateString() }}
          </p>
        </div>
        <div class="flex gap-2 ml-4">
          <button @click="startEditNote(note)"
                  class="px-3 py-1 rounded bg-blue-500/30 text-blue-300 text-sm hover:bg-blue-500/50 transition"
                  aria-label="Edit note">
            Edit
          </button>
          <button @click="deleteNote(note.id)"
                  class="px-3 py-1 rounded bg-red-500/30 text-red-300 text-sm hover:bg-red-500/50 transition"
                  aria-label="Delete note">
            Delete
          </button>
        </div>
      </div>
      <div v-else class="flex flex-col gap-3">
        <input v-model="editingNote.title" type="text"
               placeholder="Note title"
               class="input"
               aria-label="Edit note title" />
        <textarea v-model="editingNote.content"
                  placeholder="Note content"
                  class="input h-32"
                  aria-label="Edit note content"></textarea>
        <div class="flex gap-2">
          <button @click="saveEditNote(note.id)"
                  class="btn flex-1"
                  aria-label="Save changes">
            Save Changes
          </button>
          <button @click="cancelEditNote"
                  class="px-4 py-2 rounded-md bg-gray-500 text-white font-semibold hover:bg-gray-600 transition"
                  aria-label="Cancel editing">
            Cancel
          </button>
        </div>
      </div>
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
      <section v-if="view==='course'" class="w-full max-w-6xl mx-auto px-6 py-12">
        <CourseDetail :courseId="currentCourseId" :onEnroll="enroll" />
      </section>

      <section v-if="view==='admin'" class="w-full max-w-6xl mx-auto px-6 py-12">
        <AdminDashboard />
      </section>

      <section v-if="view==='login' || view==='register'" class="w-full max-w-md">
        <!-- Insert your login/register forms here -->
      </section>
    </main>

    <!-- Footer -->
    <footer class="w-full py-8 border-t border-white/10">
      <div class="max-w-7xl mx-auto px-6 flex items-center justify-between text-sm text-mb-muted">
        <div>© {{ new Date().getFullYear() }} NexusBoard Community — Built for learners, by learners</div>
        <div class="flex items-center gap-4">
          <nav class="flex gap-3 items-center" aria-label="Footer social links">
            <a href="https://github.com/namiyu5" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="GitHub">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M12 .5C5.73.5.75 5.48.75 11.75c0 4.92 3.19 9.09 7.61 10.56.56.10.77-.24.77-.54 0-.26-.01-1.12-.02-2.03-3.09.67-3.74-1.49-3.74-1.49-.51-1.29-1.25-1.64-1.25-1.64-1.02-.7.08-.69.08-.69 1.13.08 1.73 1.16 1.73 1.16 1.01 1.73 2.65 1.23 3.3.94.10-.73.39-1.23.71-1.51-2.47-.28-5.07-1.24-5.07-5.51 0-1.22.44-2.22 1.16-3-.12-.28-.5-1.4.11-2.92 0 0 .95-.3 3.12 1.16.90-.25 1.86-.37 2.82-.37.96 0 1.92.12 2.82.37 2.16-1.46 3.11-1.16 3.11-1.16.62 1.52.24 2.64.12 2.92.72.78 1.15 1.78 1.15 3 0 4.28-2.6 5.23-5.08 5.5.4.35.77 1.04.77 2.10 0 1.52-.01 2.74-.01 3.11 0 .30.21.65.78.54C19.06 20.84 22.25 16.67 22.25 11.75 22.25 5.48 17.27.5 11 .5z"/>
              </svg>
            </a>
            <a href="https://www.instagram.com" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="Instagram">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M7 2C4.24 2 2 4.24 2 7v10c0 2.76 2.24 5 5 5h10c2.76 0 5-2.24 5-5V7c0-2.76-2.24-5-5-5H7zm0 2h10c1.66 0 3 1.34 3 3v10c0 1.66-1.34 3-3 3H7c-1.66 0-3-1.34-3-3V7c0-1.66 1.34-3 3-3zm5 2.5A4.5 4.5 0 1 0 16.5 11 4.5 4.5 0 0 0 12 6.5zm0 2A2.5 2.5 0 1 1 9.5 11 2.5 2.5 0 0 1 12 8.5zM18.5 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
              </svg>
            </a>
            <a href="https://www.facebook.com" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="Facebook">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
                <path d="M22 12a10 10 0 1 0-11.5 9.95v-7.05H8.9V12h1.6V9.8c0-1.58.94-2.46 2.38-2.46.69 0 1.42.12 1.42.12v1.56h-.8c-.79 0-1.04.49-1.04.99V12h1.77l-.28 2.9h-1.49v7.05A10 10 0 0 0 22 12z"/>
              </svg>
            </a>
            <a href="#" target="_blank" rel="noopener" class="text-mb-muted hover:text-mb-primary" aria-label="X">
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
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import axios from 'axios'
import { setAuthTokens, clearAuth, verifyAuth } from './api.js'
import logo from './assets/favicon.ico'
import CourseDetail from './components/CourseDetail.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import Toast from './components/Toast.vue'

const view = ref('home')
const toast = ref(null)
const username = ref(localStorage.getItem('username') || '')
const courses = ref([])
const notes = ref([])
const enrolledCourses = ref([])
const isLoggedIn = ref(!!localStorage.getItem('access_token'))
const isAdmin = ref(false)
const usernameDisplay = ref(localStorage.getItem('username') || '')
const currentCourseId = ref(null)

function refreshAuthState() {
  isLoggedIn.value = !!localStorage.getItem('access_token')
  usernameDisplay.value = localStorage.getItem('username') || ''
}

const featuredCourse = computed(() => (courses.value && courses.value.length) ? courses.value[0] : { id: null, title: '', description: '', duration: '' })

// API base URL — update VITE_API_BASE in .env.local if needed for development
const API_BASE = import.meta.env.VITE_API_BASE || ''

let pollHandle = null
const POLL_INTERVAL_MS = 8000

function onShowLogin() { if (!isLoggedIn.value) view.value = 'login' }
function onShowRegister() { if (!isLoggedIn.value) view.value = 'register' }

async function fetchData() {
  try {
    const [courseRes, notesRes] = await Promise.all([
      axios.get(`${API_BASE}/api/courses/`),
      axios.get(`${API_BASE}/api/notes/`).catch(() => ({ data: [] })),
    ])
    // Handle both paginated DRF responses and plain arrays
    const courseData = Array.isArray(courseRes.data) ? courseRes.data : (courseRes.data && courseRes.data.results) ? courseRes.data.results : []
    const notesData = Array.isArray(notesRes.data) ? notesRes.data : (notesRes.data && notesRes.data.results) ? notesRes.data.results : []
    courses.value = courseData
    notes.value = notesData
  } catch (err) {
    console.error('Error fetching data', err)
  }
}

async function loadEnrollments() {
  // Load user's enrolled courses from server
  enrolledCourses.value = []
  if (!isLoggedIn.value) return
  try {
    const res = await axios.get('/api/enrollments/')
    const data = Array.isArray(res.data) ? res.data : (res.data && res.data.results) ? res.data.results : []
    enrolledCourses.value = data.map(en => {
      const c = en.course
      return c && typeof c === 'object' ? c.id : c
    }).filter(Boolean)
  } catch (err) {
    console.error('Failed to load enrollments', err)
  }
}

onMounted(() => {
  // Load initial data
  fetchData()
  // verify auth tokens and refresh if needed so UI shows correct login state
  verifyAuth().then(ok => {
    if (ok) {
      refreshAuthState()
      // load server-side enrollments when authenticated
      loadEnrollments().catch(() => {})
      loadUserInfo().catch(() => {})
    } else {
      refreshAuthState()
    }
  }).catch(() => refreshAuthState())
  // listen for auth changes from other components
  window.addEventListener('authChanged', refreshAuthState)
  // listen for requests from child components to show inline auth views
  window.addEventListener('showLogin', onShowLogin)
  window.addEventListener('showRegister', onShowRegister)
  // navigate to course/lesson when child signals startLearning
  window.addEventListener('startLearning', (ev) => {
    const d = ev?.detail || window.__startLearningPayload
    if (!d) return
    currentCourseId.value = d.courseId
    // ensure enrolledCourses contains courseId
    if (!enrolledCourses.value.includes(d.courseId)) enrolledCourses.value.push(d.courseId)
    // persist last-start payload so we can restore across reloads
    try { localStorage.setItem('lastStart', JSON.stringify(d)) } catch (e) { /* ignore */ }
    view.value = 'course'
  })
  // poll for changes so admin-created courses appear automatically
  pollHandle = setInterval(fetchData, POLL_INTERVAL_MS)
})

async function loadUserInfo() {
  try {
    const res = await axios.get('/api/me/')
    if (res && res.data) {
      const d = res.data
      isAdmin.value = !!d.is_staff
      // cache for quick checks
      try { localStorage.setItem('is_staff', isAdmin.value ? '1' : '0') } catch (e) {}
    }
  } catch (err) {
    isAdmin.value = false
  }
}

onUnmounted(() => {
  if (pollHandle) clearInterval(pollHandle)
  window.removeEventListener('authChanged', refreshAuthState)
  window.removeEventListener('showLogin', onShowLogin)
  window.removeEventListener('showRegister', onShowRegister)
})

function openCourse(id) {
  // open course detail — require login to view full content
  if (!isLoggedIn.value) {
    view.value = 'login'
    return
  }
  if (!enrolledCourses.value.includes(id)) enrolledCourses.value.push(id)
  currentCourseId.value = id
  view.value = 'course'
}
const newNoteTitle = ref('')
const newNoteContent = ref('')
const editingNoteId = ref(null)
const editingNote = ref({ title: '', content: '' })

// login/register form state used by the inline App.vue forms
const password = ref('')
const regUsername = ref('')
const regEmail = ref('')
const regPassword = ref('')

function startEditNote(note) {
  editingNoteId.value = note.id
  editingNote.value = {
    title: note.title,
    content: note.content,
  }
}

function cancelEditNote() {
  editingNoteId.value = null
  editingNote.value = { title: '', content: '' }
}

async function saveEditNote(noteId) {
  if (!editingNote.value.title || !editingNote.value.content) {
    toast.value?.showToast('Please provide both a title and content.', 'error')
    return
  }

  try {
    const res = await axios.put(`/api/notes/${noteId}/`, {
      title: editingNote.value.title,
      content: editingNote.value.content,
    })
    
    if (res.status === 200) {
      const noteIndex = notes.value.findIndex(n => n.id === noteId)
      if (noteIndex !== -1) {
        notes.value[noteIndex] = res.data
      }
      editingNoteId.value = null
      editingNote.value = { title: '', content: '' }
      toast.value?.showToast('Note updated successfully!', 'success', 2000)
    } else {
      toast.value?.showToast('Failed to update note.', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error updating note.', 'error')
  }
}

async function deleteNote(noteId) {
  if (!confirm('Are you sure you want to delete this note?')) {
    return
  }

  try {
    const res = await axios.delete(`/api/notes/${noteId}/`)
    
    if (res.status === 204 || res.status === 200) {
      notes.value = notes.value.filter(n => n.id !== noteId)
      toast.value?.showToast('Note deleted successfully!', 'success', 2000)
    } else {
      toast.value?.showToast('Failed to delete note.', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error deleting note.', 'error')
  }
}

async function submitLogin() {
  try {
    const res = await axios.post('/api/token/', {
      username: username.value,
      password: password.value,
    })
    if (res && res.data && res.data.access) {
      setAuthTokens(res.data.access, res.data.refresh)
      localStorage.setItem('username', username.value)
      refreshAuthState()
      toast.value?.showToast('Signed in successfully!', 'success', 2000)
      setTimeout(() => {
        view.value = 'home'
      }, 2000)
    } else {
      toast.value?.showToast('Unexpected server response', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Invalid credentials', 'error')
  }
}

async function submitRegister() {
  try {
    const res = await axios.post(`${API_BASE}/api/auth/signup/`, {
      username: regUsername.value,
      email: regEmail.value,
      password: regPassword.value,
    })
    if (res && res.status === 201) {
      toast.value?.showToast('Account created. Please sign in.', 'success', 2000)
      username.value = regUsername.value
      setTimeout(() => {
        view.value = 'login'
      }, 2000)
    } else {
      toast.value?.showToast('Registration failed', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error during registration', 'error')
  }
}

async function createNote() {
  if (!newNoteTitle.value || !newNoteContent.value) {
    toast.value?.showToast('Please provide both a title and content.', 'error')
    return
  }
  try {
    const res = await axios.post('/api/notes/', {
      title: newNoteTitle.value,
      content: newNoteContent.value,
    })
    if (res.status === 201) {
      notes.value.push(res.data)
      newNoteTitle.value = ''
      newNoteContent.value = ''
      toast.value?.showToast('Note created successfully!', 'success', 2000)
    } else {
      toast.value?.showToast('Failed to save note.', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error saving note.', 'error')
  }
}

async function enroll(courseId) {
  if (!isLoggedIn.value) {
    view.value = 'login'
    return
  }
  // Optimistic UI: immediately mark as enrolled so button turns into 'Start learning'
  let addedOptimistically = false
  if (!enrolledCourses.value.includes(courseId)) {
    enrolledCourses.value.push(courseId)
    addedOptimistically = true
  }
  currentCourseId.value = courseId
  // navigate to course page immediately
  view.value = 'course'

  // notify any open course-detail component that enrollment occurred (optimistic)
  try {
    window.dispatchEvent(new CustomEvent('enrolled', { detail: { courseId } }))
  } catch (e) {
    /* ignore if window isn't available */
  }

  try {
    const res = await axios.post('/api/enrollments/', { course: courseId })
    if (!(res && (res.status === 201 || res.status === 200))) {
      // server didn't create enrollment; leave optimistic state (user will see server state on refresh)
    }
  } catch (err) {
    // On error (e.g., 401), revert optimistic update and prompt login
    if (err?.response?.status === 401) {
      // revert optimistic enrollment
      if (addedOptimistically) enrolledCourses.value = enrolledCourses.value.filter(id => id !== courseId)
      view.value = 'login'
      return
    }
    console.error('Enrollment failed', err)
  }
}

function logout() {
  clearAuth()
  refreshAuthState()
  view.value = 'home'
}

function goToLogin() { 
  if (isLoggedIn.value) { view.value = 'home'; return }
  view.value = 'login' 
}
function goToRegister() { 
  if (isLoggedIn.value) { view.value = 'home'; return }
  view.value = 'register' 
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
  @apply px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300 transition;
}

.btn-lg {
  @apply px-6 py-3 rounded-lg font-bold shadow-md hover:opacity-90 transition;
}

.cta-btn {
  @apply px-6 py-3 rounded-lg font-bold shadow-md transition;
}

.input {
  @apply bg-[rgba(255,255,255,0.05)] border border-white/10 p-3 rounded-md outline-none 
         text-lg text-white placeholder:text-white/40 focus:ring-2 focus:ring-indigo-400 transition;
}



</style> 