<template>
  <div class="flex flex-col min-h-screen bg-gradient-to-br from-neutral-900 via-slate-900 to-zinc-900 text-white">
    <!-- Navbar -->
    <header class="w-full py-4 border-b border-white/10">
      <div class="max-w-6xl mx-auto px-4 flex items-center justify-between">
        <div class="text-2xl font-bold">NexusBoard</div>
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
           placeholder="••••••••"
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


      <!-- Home -->
      <section v-if="view==='home'" class="text-center max-w-2xl">
        <h1 class="text-4xl md:text-6xl font-extrabold text-yellow-300">Learn. Share. Grow.</h1>
        <p class="mt-6 text-lg text-white/80">
          NexusBoard is your free community‑powered platform for courses, notes, and collaboration.
        </p>
        <div class="mt-8 flex gap-4 justify-center">
          <button @click="view='courses'" class="cta-btn bg-yellow-400 text-indigo-900">Browse Courses</button>
          <button @click="view='register'" class="cta-btn bg-indigo-500 text-white">Join Free</button>
        </div>
      </section>

      <!-- Courses -->
    <!-- Courses Page -->
<section v-if="view==='courses'" class="w-full max-w-6xl mx-auto px-6 py-12">
  <h2 class="text-3xl font-bold mb-8 text-center">Available Courses</h2>

  <!-- Courses Grid -->
  <div class="grid md:grid-cols-3 gap-8">
    <!-- Mock Course Card -->
    <div v-for="course in mockCourses" :key="course.id"
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
import { ref, onMounted } from 'vue'
import axios from 'axios'

const view = ref('home')
const username = ref('')
const courses = ref([])
const notes = ref([])
const enrolledCourses = ref([])

const API_BASE = 'http://127.0.0.1:8000'

// Fetch courses and notes from backend
onMounted(async () => {
  try {
    const courseRes = await axios.get(`${API_BASE}/api/courses/`)
    courses.value = courseRes.data
    const notesRes = await axios.get(`${API_BASE}/api/notes/`)
    notes.value = notesRes.data
  } catch (err) {
    console.error('Error fetching data', err)
  }
})

function openCourse(id) {
  view.value = 'dashboard'
  enrolledCourses.value.push(id)
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
const mockCourses = ref([
  { id: 1, title: 'Intro to Web Development', description: 'Learn HTML, CSS, and JavaScript basics.', duration: '6 weeks' },
  { id: 2, title: 'Python for Beginners', description: 'Start coding with Python and build simple apps.', duration: '8 weeks' },
  { id: 3, title: 'UI/UX Design Fundamentals', description: 'Design clean, user‑friendly interfaces.', duration: '4 weeks' },
  { id: 4, title: 'Data Science Essentials', description: 'Explore data analysis, visualization, and machine learning basics.', duration: '10 weeks' },
  { id: 5, title: 'Cybersecurity Basics', description: 'Understand online safety, encryption, and ethical hacking.', duration: '5 weeks' },
  { id: 6, title: 'Django & REST APIs', description: 'Build powerful backends with Django and REST framework.', duration: '7 weeks' },
])

function enroll(courseId) {
  console.log('Enrolled in course:', courseId)
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