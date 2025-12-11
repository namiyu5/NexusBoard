<template>
  <div class="flex flex-col min-h-screen bg-mb-bg text-white font-sans">
    <!-- Toast Notifications -->
    <Toast ref="toast" />

    <!-- Skip to main content link (for keyboard navigation and screen readers) -->
    <a href="#main-content" class="sr-only focus:not-sr-only focus:absolute focus:top-0 focus:left-0 focus:bg-mb-primary focus:text-black focus:p-2 focus:z-50">
      Skip to main content
    </a>

    <!-- Navbar -->
    <header class="w-full py-4 border-b border-white/10 backdrop-blur-md bg-slate-900/50" role="banner">
      <div class="max-w-6xl mx-auto px-6 flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="text-2xl font-bold bg-gradient-to-r from-yellow-300 to-indigo-400 bg-clip-text text-transparent">
        NexusBoard
        </div>
        <img :src="logoUrl" alt="NexusBoard logo and home link" class="w-8 h-8 rounded-full" />
      </div>
      
      <nav class="flex items-center gap-8" aria-label="Main navigation">
        <button @click="view='home'" 
                :aria-current="view === 'home' ? 'page' : undefined"
                :class="['nav-btn', view === 'home' ? 'text-yellow-300 border-b-2 border-yellow-300' : 'text-white/70 hover:text-white']"
                aria-label="Home page">
        Home
        </button>
        <button @click="view='courses'" 
                :aria-current="view === 'courses' ? 'page' : undefined"
                :class="['nav-btn', view === 'courses' ? 'text-yellow-300 border-b-2 border-yellow-300' : 'text-white/70 hover:text-white']"
                aria-label="Browse courses">
        Courses
        </button>
        <button @click="view='notes'" 
                :aria-current="view === 'notes' ? 'page' : undefined"
                :class="['nav-btn', view === 'notes' ? 'text-yellow-300 border-b-2 border-yellow-300' : 'text-white/70 hover:text-white']"
                aria-label="View your notes">
        Notes
        </button>
        <button @click="view='dashboard'" 
                :aria-current="view === 'dashboard' ? 'page' : undefined"
                :class="['nav-btn', view === 'dashboard' ? 'text-yellow-300 border-b-2 border-yellow-300' : 'text-white/70 hover:text-white']"
                aria-label="View your dashboard">
        Dashboard
        </button>
        <button v-if="isAdmin" @click="view='admin'" 
                :aria-current="view === 'admin' ? 'page' : undefined"
                :class="['nav-btn', view === 'admin' ? 'text-yellow-300 border-b-2 border-yellow-300' : 'text-white/70 hover:text-white']"
                aria-label="Admin panel">
        Admin
        </button>
      </nav>

      <div class="flex items-center gap-4">
        <template v-if="isLoggedIn">
        <div class="hidden sm:flex items-center gap-3">
          <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-indigo-500 to-teal-400 flex items-center justify-center text-white font-semibold text-sm" :aria-label="`Profile avatar for ${usernameDisplay}`">
          {{ usernameDisplay.charAt(0).toUpperCase() }}
          </div>
          <div class="flex flex-col">
            <span class="text-xs text-white/50">You are logged in as</span>
            <span class="text-sm text-white/70">{{ usernameDisplay }}</span>
          </div>
        </div>
        <button @click="logout" 
          class="px-4 py-2 rounded-lg bg-red-500/20 text-red-300 text-sm font-medium hover:bg-red-500/30 transition"
          aria-label="Logout from your account">
          Logout
        </button>
        </template>
        <template v-else>
          <span class="text-xs text-white/50">You are not logged in</span>
        <button @click="goToLogin" 
                class="px-4 py-2 rounded-lg bg-indigo-500/30 text-indigo-300 text-sm font-medium hover:bg-indigo-500/50 transition"
                aria-label="Sign in to your account">
          Login
        </button>
        <button @click="goToRegister" 
                class="px-4 py-2 rounded-lg bg-gradient-to-r from-teal-400 to-indigo-500 text-black text-sm font-semibold hover:shadow-lg transition"
                aria-label="Create a new account">
          Sign Up
        </button>
        </template>
      </div>
      </div>
    </header>

    <!-- Main content -->
    <main id="main-content" role="main" :class="view==='home' ? 'flex-1 flex flex-col items-center justify-center' : 'flex-1 flex flex-col items-center justify-center px-6 py-12'">
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
    <div class="flex flex-col">
      <label for="login-username" class="text-sm font-medium text-white/80 mb-1">Username</label>
      <input id="login-username" v-model="username" type="text"
             placeholder="Enter your username"
             class="input"
             aria-label="Username for login" />
    </div>
    <div class="flex flex-col">
      <label for="login-password" class="text-sm font-medium text-white/80 mb-1">Password</label>
      <input id="login-password" v-model="password" type="password"
             placeholder="Enter your password"
             class="input"
             aria-label="Password for login" />
    </div>

    <div class="w-full flex justify-end">
      <a href="#" class="text-xs font-bold text-indigo-300 hover:underline" aria-label="Reset password">Forgot password?</a>
    </div>

    <button @click="submitLogin"
            class="btn w-full bg-gradient-to-r from-teal-400 to-indigo-500 text-black"
            aria-label="Sign in with your credentials">
      Login
    </button>

    <p class="text-xs text-center text-white/70">
      Don't have an account?
      <button @click="view='register'" class="font-bold text-indigo-300 hover:underline" aria-label="Navigate to sign up page">
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
    <div class="flex flex-col">
      <label for="reg-username" class="text-sm font-medium text-white/80 mb-1">Username</label>
      <input id="reg-username" v-model="regUsername" type="text"
             placeholder="Choose your username"
             class="input"
             aria-label="Username for new account" />
    </div>
    <div class="flex flex-col">
      <label for="reg-email" class="text-sm font-medium text-white/80 mb-1">Email</label>
      <input id="reg-email" v-model="regEmail" type="email"
             placeholder="you@example.com"
             class="input"
             aria-label="Email address for new account" />
    </div>
    <div class="flex flex-col">
      <label for="reg-password" class="text-sm font-medium text-white/80 mb-1">Password</label>
      <input id="reg-password" v-model="regPassword" type="password"
             placeholder="Create a password"
             class="input"
             aria-label="Password for new account" />
    </div>

    <button @click="submitRegister"
            class="btn w-full bg-gradient-to-r from-green-400 to-indigo-500 text-black"
            aria-label="Create your account">
      Create Account
    </button>

    <p class="text-xs text-center text-white/70">
      Already have an account?
      <button @click="view='login'" class="font-bold text-indigo-300 hover:underline" aria-label="Navigate to sign in page">
        Sign in
      </button>
    </p>
  </div>
</section>


     
      <section v-if="view==='home'" class="w-full min-h-[calc(100vh-80px)]" :style="heroBackgroundStyle">
        <div class="max-w-6xl mx-auto px-6 py-12 space-y-10 starry-content">
          <!-- Hero -->
          <div class="grid md:grid-cols-2 gap-8 items-center">
        <div class="space-y-6">
          <h1 class="text-4xl md:text-6xl font-extrabold leading-tight text-mb-highlight font-heading bg-gradient-to-r from-teal-400 to-indigo-500 bg-clip-text text-transparent">
        NexusBoard<br>
        For Learners,<br>
        By Learners
          </h1>
          <br>
          <p class="text-lg text-mb-muted max-w-2xl">
        Part of <span class="text-mb-highlight font-semibold">The Nexus Project</span> 
        <br>Connecting communities through learning. 
        NexusBoard bridges the gaps in education by providing accessible, practical courses and collaborative spaces where 
        every voice is heard. Together, we're building a constellation of knowledge where no one is left behind.
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

        
        <div class="bg-blue-400/20 rounded-2xl p-6 shadow-xl border-l-4 border-yellow-300 backdrop-blur-md">
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
            <div class="w-9 h-9 rounded-full bg-gradient-to-tr from-teal-400 to-indigo-500 flex items-center justify-center text-white font-semibold text-sm">
              {{ (note.title && note.title.length) ? note.title.charAt(0).toUpperCase() : 'N' }}
            </div>
            <div class="text-sm">
              <div class="font-semibold text-white truncate max-w-xs">{{ note.title }}</div>
              <div class="text-xs text-white/60 line-clamp-2 max-w-xs" v-html="processEmbeds(note.content)"></div>
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
<section v-if="view==='courses'" class="w-full max-w-6xl mx-auto px-6 py-12">
  <!-- Header -->
  <div class="mb-10">
    <h2 class="text-4xl font-bold mb-2">📚 Courses</h2>
    <p class="text-white/60">Expand your skills with our curated selection of courses</p>
  </div>

  <!-- Quick Stats -->
  <div class="grid grid-cols-3 gap-4 mb-8">
    <div class="card p-4 bg-gradient-to-br from-indigo-500/20 to-purple-500/20">
      <div class="text-3xl font-bold text-indigo-400">{{ courses.length }}</div>
      <div class="text-xs text-white/60 mt-1">Total Courses</div>
    </div>
    <div class="card p-4 bg-gradient-to-br from-teal-500/20 to-green-500/20">
      <div class="text-3xl font-bold text-teal-400">{{ enrolledCourses.length }}</div>
      <div class="text-xs text-white/60 mt-1">Your Courses</div>
    </div>
    <div class="card p-4 bg-gradient-to-br from-orange-500/20 to-red-500/20">
      <div class="text-3xl font-bold text-orange-400">{{ Math.max(0, courses.length - enrolledCourses.length) }}</div>
      <div class="text-xs text-white/60 mt-1">Available to Explore</div>
    </div>
  </div>

  <!-- Search/Filter Bar -->
  <div class="mb-8 flex gap-3">
    <input v-model="courseSearchQuery" 
           type="text" 
           placeholder="Search courses by title or topic..."
           class="flex-1 px-4 py-2 rounded-md bg-white/10 border border-white/20 text-white placeholder-white/40 focus:outline-none focus:border-indigo-500"
           aria-label="Search courses" />
    <select v-model="courseDifficultyFilter"
            class="px-4 py-2 rounded-md bg-white/10 border border-white/20 text-white focus:outline-none focus:border-indigo-500"
            aria-label="Filter by difficulty">
      <option value="">All Levels</option>
      <option value="beginner">Beginner</option>
      <option value="intermediate">Intermediate</option>
      <option value="advanced">Advanced</option>
    </select>
  </div>

  <!-- Courses Grid -->
  <div v-if="filteredCourses.length === 0" class="text-center py-16">
    <div class="text-4xl mb-3">🔍</div>
    <p class="text-white/60">No courses match your search criteria. Try adjusting your filters.</p>
  </div>

  <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div v-for="course in filteredCourses" :key="course.id"
         class="card group hover:shadow-xl hover:shadow-indigo-500/20 transition">
      <!-- Course Header -->
      <div class="flex items-start justify-between mb-3">
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-white group-hover:text-indigo-300 transition">{{ course.title }}</h3>
          <div class="flex items-center gap-2 mt-2 flex-wrap">
            <span :class="['px-2 py-1 rounded-full text-xs font-medium', 
              course.difficulty === 'beginner' ? 'bg-green-500/30 text-green-300' :
              course.difficulty === 'intermediate' ? 'bg-yellow-500/30 text-yellow-300' :
              'bg-red-500/30 text-red-300']">
              {{ course.difficulty ? course.difficulty.charAt(0).toUpperCase() + course.difficulty.slice(1) : 'Beginner' }}
            </span>
            <span v-if="course.duration_hours" class="px-2 py-1 rounded-full text-xs bg-indigo-500/30 text-indigo-300">⏱️ {{ course.duration_hours }}h</span>
          </div>
        </div>
      </div>

      <!-- Description -->
      <p class="text-sm text-white/70 mb-4 line-clamp-2">{{ course.description }}</p>

      <!-- Course Metadata -->
      <div class="mb-4 pb-4 border-b border-white/10 text-xs text-white/50">
        <div class="flex justify-between mb-2">
          <span>Lessons</span>
          <span class="font-semibold text-white">{{ course.lessons ? course.lessons.length : 0 }}</span>
        </div>
        <div class="flex justify-between" v-if="enrolledCourses.includes(course.id)">
          <span>Status</span>
          <span class="text-green-300 font-semibold">✓ Enrolled</span>
        </div>
      </div>

      <!-- Buttons -->
      <div class="flex gap-2">
        <button @click="openCourse(course.id)" 
                class="flex-1 px-3 py-2 rounded-md bg-indigo-500/30 text-indigo-300 text-sm hover:bg-indigo-500/50 transition font-medium"
                :aria-label="`View ${course.title}`">
          View Details
        </button>
        <button @click="enroll(course.id)"
                :class="['flex-1 px-3 py-2 rounded-md text-sm font-medium transition', enrolledCourses.includes(course.id) ? 'bg-green-500/30 text-green-300 cursor-not-allowed' : 'bg-teal-500/30 text-teal-300 hover:bg-teal-500/50']"
                :disabled="enrolledCourses.includes(course.id)"
                :aria-label="enrolledCourses.includes(course.id) ? `Continue ${course.title}` : `Enroll in ${course.title}`">
          {{ enrolledCourses.includes(course.id) ? '▶ Continue' : '+ Enroll' }}
        </button>
      </div>
    </div>
  </div>
</section>


      <!-- Notes Section -->
<section v-if="view==='notes'" class="w-full max-w-6xl">
  <div class="mb-8">
    <h2 class="text-4xl font-bold mb-2">Study Notes</h2>
    <p class="text-white/60">Organize and manage your course notes in one place</p>
  </div>

  <!-- Quick Stats -->
  <div class="grid grid-cols-3 gap-4 mb-8">
    <div class="card p-4 bg-gradient-to-br from-indigo-500/20 to-purple-500/20">
      <div class="text-3xl font-bold text-indigo-400">{{ notes.length }}</div>
      <div class="text-xs text-white/60 mt-1">Total Notes</div>
    </div>
    <div class="card p-4 bg-gradient-to-br from-teal-500/20 to-green-500/20">
      <div class="text-3xl font-bold text-teal-400">{{ notes.filter(n => n.is_public).length }}</div>
      <div class="text-xs text-white/60 mt-1">Public Notes</div>
    </div>
    <div class="card p-4 bg-gradient-to-br from-orange-500/20 to-red-500/20">
      <div class="text-3xl font-bold text-orange-400">{{ enrolledCourses.length }}</div>
      <div class="text-xs text-white/60 mt-1">Courses Enrolled</div>
    </div>
  </div>

  <!-- Create Note Form -->
  <div class="card mb-8 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border-l-4 border-indigo-500">
    <div class="flex items-center gap-3 mb-4">
      <div class="w-10 h-10 rounded-full bg-indigo-500/20 flex items-center justify-center">
        <span class="text-lg">📝</span>
      </div>
      <h3 class="text-lg font-semibold">Create a Study Note</h3>
    </div>
    <input v-model="newNoteTitle" type="text"
           placeholder="Note title (e.g., 'Key Concepts - Module 1')"
           class="input mb-3"
           aria-label="Note title" />
    <select v-model="selectedLessonId"
            class="input mb-3"
            aria-label="Select lesson for this note">
      <option disabled value="">Select a lesson to attach this note</option>
      <option v-for="lesson in lessonOptions" :key="lesson.id" :value="lesson.id">
        {{ lesson.course }} — {{ lesson.title }}
      </option>
    </select>
    <WysiwygEditor v-model="newNoteContent" />
    <div class="flex gap-2">
      <button @click="createNote"
              class="btn bg-gradient-to-r from-indigo-500 to-purple-500 text-white flex-1"
              aria-label="Save note">
        Save Note
      </button>
      <label class="flex items-center gap-2 px-4 py-2 rounded-md bg-white/10 hover:bg-white/20 cursor-pointer transition">
        <input type="checkbox" v-model="newNoteIsPublic" class="rounded" />
        <span class="text-sm text-white/70">Make Public</span>
      </label>
    </div>
  </div>

  <!-- Notes View Tabs -->
  <div class="mb-6 flex gap-2 border-b border-white/10">
    <button @click="notesFilter = 'all'"
            :class="['px-4 py-2 text-sm font-medium transition', notesFilter === 'all' ? 'text-indigo-400 border-b-2 border-indigo-400' : 'text-white/60 hover:text-white']">
      All Notes
    </button>
    <button @click="notesFilter = 'public'"
            :class="['px-4 py-2 text-sm font-medium transition', notesFilter === 'public' ? 'text-teal-400 border-b-2 border-teal-400' : 'text-white/60 hover:text-white']">
      Public
    </button>
    <button @click="notesFilter = 'private'"
            :class="['px-4 py-2 text-sm font-medium transition', notesFilter === 'private' ? 'text-orange-400 border-b-2 border-orange-400' : 'text-white/60 hover:text-white']">
      Private
    </button>
  </div>

  <!-- Notes List -->
  <div v-if="filteredNotes.length === 0" class="text-center py-12">
    <div class="text-4xl mb-3">📚</div>
    <p class="text-white/60">{{ notesFilter === 'all' ? 'No notes yet. Start by creating your first study note!' : `No ${notesFilter} notes yet.` }}</p>
  </div>

  <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <div v-for="note in filteredNotes" :key="note.id" class="card">
      <div v-if="editingNoteId !== note.id">
        <!-- View Mode -->
        <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <h3 class="text-lg font-semibold text-white">{{ note.title }}</h3>
            <div class="flex items-center gap-2 mt-2">
              <span :class="['px-2 py-1 rounded text-xs font-medium', note.is_public ? 'bg-teal-500/30 text-teal-300' : 'bg-orange-500/30 text-orange-300']">
                {{ note.is_public ? '🔓 Public' : '🔒 Private' }}
              </span>
              <span class="text-xs text-white/50">{{ new Date(note.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) }}</span>
              <span v-if="lessonTitleMap[note.lesson]" class="text-xs text-white/50">· {{ lessonTitleMap[note.lesson] }}</span>
            </div>
          </div>
        </div>
        <div class="text-sm text-white/70 mb-4 line-clamp-3" v-html="note.content"></div>
        <!-- Only show Edit/Delete buttons if current user is the author or admin -->
        <div v-if="canEditNote(note)" class="flex gap-2">
          <button @click="startEditNote(note)"
                  class="flex-1 px-3 py-1 rounded bg-blue-500/30 text-blue-300 text-sm hover:bg-blue-500/50 transition"
                  aria-label="Edit note">
            ✏️ Edit
          </button>
          <button @click="deleteNote(note.id)"
                  class="flex-1 px-3 py-1 rounded bg-red-500/30 text-red-300 text-sm hover:bg-red-500/50 transition"
                  aria-label="Delete note">
            🗑️ Delete
          </button>
        </div>
        <!-- Show read-only view for notes user cannot edit -->
        <div v-else class="text-xs text-white/50 px-3 py-2">
          You can only view this note
        </div>
      </div>
      <div v-else>
        <!-- Edit Mode -->
        <h4 class="text-sm font-semibold text-white/60 mb-2">Editing Note</h4>
        <input v-model="editingNote.title" type="text"
               placeholder="Note title"
               class="input mb-2"
               aria-label="Edit note title" />
        <WysiwygEditor v-model="editingNote.content" />
        <label class="flex items-center gap-2 mb-3 px-3 py-1 rounded bg-white/10 w-fit">
          <input type="checkbox" v-model="editingNote.is_public" class="rounded" />
          <span class="text-sm text-white/70">Public</span>
        </label>
        <div class="flex gap-2">
          <button @click="saveEditNote(note.id)"
                  class="flex-1 btn bg-green-500 text-white"
                  aria-label="Save changes">
            ✓ Save
          </button>
          <button @click="cancelEditNote"
                  class="flex-1 px-4 py-2 rounded-md bg-gray-500/30 text-white hover:bg-gray-500/50 transition"
                  aria-label="Cancel editing">
            ✕ Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</section>


      <!-- Dashboard -->
      <section v-if="view==='dashboard'" class="w-full max-w-6xl mx-auto px-6 py-12">
        <!-- Header -->
        <div class="mb-10">
          <h2 class="text-4xl font-bold mb-2">📊 My Dashboard</h2>
          <p class="text-white/60">Track your learning progress and achievements</p>
        </div>

        <!-- Quick Stats -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-10">
          <div class="card p-4 bg-gradient-to-br from-indigo-500/20 to-purple-500/20">
        <div class="text-3xl font-bold text-indigo-400">{{ enrolledCourses.length }}</div>
        <div class="text-xs text-white/60 mt-1">Courses Enrolled</div>
          </div>
          <div class="card p-4 bg-gradient-to-br from-teal-500/20 to-green-500/20">
        <div class="text-3xl font-bold text-teal-400">{{ notes.length }}</div>
        <div class="text-xs text-white/60 mt-1">Notes Created</div>
          </div>
          <div class="card p-4 bg-gradient-to-br from-yellow-500/20 to-orange-500/20">
        <div class="text-3xl font-bold text-yellow-400">{{ Math.floor(enrolledCourses.length * 35) }}%</div>
        <div class="text-xs text-white/60 mt-1">Avg. Progress</div>
          </div>
          <div class="card p-4 bg-gradient-to-br from-pink-500/20 to-rose-500/20">
        <div class="text-3xl font-bold text-pink-400">{{ Math.max(5, enrolledCourses.length * 2) }}</div>
        <div class="text-xs text-white/60 mt-1">Learning Streak</div>
          </div>
        </div>

        <!-- Welcome & Profile Section -->
        <div class="card mb-8 bg-gradient-to-r from-indigo-500/10 to-purple-500/10 border-l-4 border-indigo-500 p-6">
          <div class="flex items-center gap-4">
        <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-indigo-500 to-teal-400 flex items-center justify-center text-white font-bold text-2xl">
          {{ usernameDisplay.charAt(0).toUpperCase() }}
        </div>
        <div>
          <h3 class="text-2xl font-bold text-white">Welcome back, {{ usernameDisplay }}!</h3>
          <p class="text-white/60 text-sm mt-1">Keep up the great learning momentum 🚀</p>
        </div>
          </div>
        </div>

        <!-- Two Column Layout -->
        <div class="grid lg:grid-cols-3 gap-8">
          <!-- Left Column: Enrolled Courses -->
          <div class="lg:col-span-2">
        <div class="mb-6">
          <h3 class="text-2xl font-bold text-white mb-2">My Courses</h3>
          <p class="text-white/60 text-sm">{{ enrolledCourses.length }} course{{ enrolledCourses.length !== 1 ? 's' : '' }} in progress</p>
        </div>

        <div v-if="enrolledCourses.length === 0" class="card text-center py-12">
          <div class="text-4xl mb-3">📚</div>
          <p class="text-white/60 mb-4">No courses yet. Start your learning journey!</p>
          <button @click="view='courses'" class="btn bg-gradient-to-r from-teal-400 to-indigo-500 text-black">
            Browse Courses
          </button>
        </div>

        <div v-else class="space-y-4">
          <div v-for="courseId in enrolledCourses" :key="courseId" class="card group hover:shadow-lg hover:shadow-indigo-500/20 transition">
            <div class="flex items-start justify-between mb-3">
          <div class="flex-1">
            <h4 class="text-lg font-semibold text-white group-hover:text-indigo-300 transition">
              {{ courses.find(c => c.id === courseId)?.title || 'Course #' + courseId }}
            </h4>
            <p class="text-sm text-white/60 mt-1">{{ courses.find(c => c.id === courseId)?.description || 'Loading...' }}</p>
          </div>
            </div>
            
            <!-- Progress Bar -->
            <div class="mb-3">
          <div class="flex justify-between text-xs text-white/60 mb-1">
            <span>Progress</span>
            <span>{{ Math.floor(Math.random() * 40) + 20 }}%</span>
          </div>
          <div class="w-full bg-white/10 rounded-full h-2 overflow-hidden">
            <div class="bg-gradient-to-r from-teal-400 to-indigo-500 h-full rounded-full" :style="{ width: Math.floor(Math.random() * 40) + 20 + '%' }"></div>
          </div>
            </div>

            <div class="flex gap-2">
          <button @click="openCourse(courseId)" class="flex-1 px-3 py-2 rounded-md bg-indigo-500/30 text-indigo-300 text-sm hover:bg-indigo-500/50 transition font-medium">
            Continue Learning
          </button>
          <button @click="enrolledCourses = enrolledCourses.filter(id => id !== courseId)" class="px-3 py-2 rounded-md bg-red-500/30 text-red-300 text-sm hover:bg-red-500/50 transition" aria-label="Remove course">
            ✕
          </button>
            </div>
          </div>
        </div>
          </div>

          <!-- Right Column: Activity & Recommendations -->
          <div class="space-y-6">
        <!-- Recent Activity -->
        <div>
          <h3 class="text-xl font-bold text-white mb-4">Recent Activity</h3>
          <div class="card p-4 space-y-3">
            <div class="flex items-center gap-3 pb-3 border-b border-white/10">
          <div class="text-2xl">📝</div>
          <div class="text-sm">
            <div class="text-white font-semibold">Created {{ notes.length }} note{{ notes.length !== 1 ? 's' : '' }}</div>
            <div class="text-xs text-white/50">Recently</div>
          </div>
            </div>
            <div class="flex items-center gap-3 pb-3 border-b border-white/10">
          <div class="text-2xl">📚</div>
          <div class="text-sm">
            <div class="text-white font-semibold">Enrolled in {{ enrolledCourses.length }} course{{ enrolledCourses.length !== 1 ? 's' : '' }}</div>
            <div class="text-xs text-white/50">Active</div>
          </div>
            </div>
            <div class="flex items-center gap-3">
          <div class="text-2xl">🔥</div>
          <div class="text-sm">
            <div class="text-white font-semibold">{{ Math.max(3, Math.floor(Math.random() * 15)) }} day streak</div>
            <div class="text-xs text-white/50">Keep it up!</div>
          </div>
            </div>
          </div>
        </div>

        <!-- Recommended Courses -->
        <div>
          <h3 class="text-xl font-bold text-white mb-4">Recommended For You</h3>
          <div class="space-y-2">
            <div v-for="course in courses.filter(c => !enrolledCourses.includes(c.id)).slice(0, 3)" :key="course.id" class="card p-3 hover:shadow-lg transition cursor-pointer">
          <h4 class="text-sm font-semibold text-white truncate">{{ course.title }}</h4>
          <p class="text-xs text-white/50 mt-1 line-clamp-1">{{ course.description }}</p>
          <button @click="enroll(course.id)" class="mt-2 w-full px-2 py-1 rounded text-xs bg-teal-500/30 text-teal-300 hover:bg-teal-500/50 transition font-medium">
            Explore
          </button>
            </div>
          </div>
        </div>

        <!-- Learning Goals -->
        <div>
          <h3 class="text-xl font-bold text-white mb-4">Your Goals</h3>
          <div class="card p-4 space-y-3">
            <label class="flex items-center gap-3 cursor-pointer group">
          <input type="checkbox" class="rounded accent-teal-400" checked />
          <span class="text-sm text-white/70 group-hover:text-white">Complete 3 courses</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
          <input type="checkbox" class="rounded accent-teal-400" />
          <span class="text-sm text-white/70 group-hover:text-white">Create 10 notes</span>
            </label>
            <label class="flex items-center gap-3 cursor-pointer group">
          <input type="checkbox" class="rounded accent-teal-400" />
          <span class="text-sm text-white/70 group-hover:text-white">30 day learning streak</span>
            </label>
          </div>
        </div>
          </div>
        </div>
      </section>

      <!-- Login/Register -->
      <section v-if="view==='course'" class="w-full max-w-6xl mx-auto px-6 py-12">
        <CourseDetail :courseId="currentCourseId" :onEnroll="enroll" />
      </section>

      <section v-if="view==='admin'" class="w-full max-w-6xl mx-auto px-6 py-12">
        <AdminDashboard />
      </section>

      <section v-if="view==='login' || view==='register'" class="w-full max-w-md">
        
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
import heroBg from './assets/img/Copilot_20251208_154055.png'
import CourseDetail from './components/CourseDetail.vue'
import AdminDashboard from './components/AdminDashboard.vue'
import Toast from './components/Toast.vue'
import WysiwygEditor from './components/WysiwygEditor.vue'

// ============================================================================
// STATE MANAGEMENT: Core application state and UI visibility
// ============================================================================
const view = ref('home') // Current view: 'home', 'login', 'register', 'courses', 'course', 'notes', 'dashboard', 'admin'
const toast = ref(null) // Reference to Toast component for showing notifications
const username = ref(localStorage.getItem('username') || '') // Login form input
const courses = ref([]) // All available courses loaded from API
const notes = ref([]) // User's notes for filtering in notes view
const enrolledCourses = ref([]) // List of course IDs user has enrolled in
const isLoggedIn = ref(!!localStorage.getItem('access_token')) // Auth state derived from token presence
const isAdmin = ref(false) // Admin role for showing admin dashboard and controls
const usernameDisplay = ref(localStorage.getItem('username') || '') // Display name in navbar (cached from login)
const currentCourseId = ref(null) // Currently viewed course ID

function refreshAuthState() {
  // Sync local auth state with localStorage (used after login/logout/token refresh)
  isLoggedIn.value = !!localStorage.getItem('access_token')
  usernameDisplay.value = localStorage.getItem('username') || ''
}

// ============================================================================
// COMPUTED PROPERTIES: Derived state for view rendering
// ============================================================================

// Featured course (first course in list) shown on home page hero section
const featuredCourse = computed(() => (courses.value && courses.value.length) ? courses.value[0] : { id: null, title: '', description: '', duration: '' })

// Hero section background image with dark overlay for readability
const heroBackgroundStyle = computed(() => ({
  background: `linear-gradient(180deg, rgba(6,10,20,0.82), rgba(6,10,20,0.9)), url(${heroBg}) center/cover no-repeat`
}))

// API base URL configuration — update VITE_API_BASE in .env.local for development
const API_BASE = import.meta.env.VITE_API_BASE || ''

// Logo URL with fallback: use static path in production (Django), imported asset in dev
const logoUrl = computed(() => {
  if (typeof import.meta.env.MODE === 'string' && import.meta.env.MODE === 'production') {
    return '/static/nexusboard_vue/assets/favicon-Cxjdwhm0.ico'
  }
  return logo
})

// ============================================================================
// POLLING & INITIALIZATION: Auto-refresh data to show admin-created courses
// ============================================================================
let pollHandle = null
const POLL_INTERVAL_MS = 8000 // Fetch course updates every 8 seconds

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
const newNoteIsPublic = ref(false)
const selectedLessonId = ref('')
const notesFilter = ref('all')
const editingNoteId = ref(null)
const editingNote = ref({ title: '', content: '', is_public: false })

const filteredNotes = computed(() => {
  if (notesFilter.value === 'public') return notes.value.filter(n => n.is_public)
  if (notesFilter.value === 'private') return notes.value.filter(n => !n.is_public)
  return notes.value
})

const courseSearchQuery = ref('')
const courseDifficultyFilter = ref('')

const filteredCourses = computed(() => {
  let filtered = courses.value
  
  if (courseSearchQuery.value) {
    const query = courseSearchQuery.value.toLowerCase()
    filtered = filtered.filter(c => 
      c.title.toLowerCase().includes(query) || 
      c.description.toLowerCase().includes(query)
    )
  }
  
  if (courseDifficultyFilter.value) {
    filtered = filtered.filter(c => c.difficulty === courseDifficultyFilter.value)
  }
  
  return filtered
})

const lessonOptions = computed(() => {
  const opts = []
  for (const course of courses.value || []) {
    const lessons = course.lessons || []
    for (const lesson of lessons) {
      opts.push({ id: lesson.id, title: lesson.title, course: course.title })
    }
  }
  return opts
})

const lessonTitleMap = computed(() => {
  const map = {}
  for (const opt of lessonOptions.value) {
    map[opt.id] = `${opt.course} — ${opt.title}`
  }
  return map
})

const password = ref('')
const regUsername = ref('')
const regEmail = ref('')
const regPassword = ref('')
// ============================================================================
// NOTE MANAGEMENT: Create, read, update, delete notes with public/private sharing
// ============================================================================

// Check if current user can edit/delete a note (must be author or admin)
function canEditNote(note) {
  // Only allow edit if user is the author or is admin
  return note.author === usernameDisplay.value || isAdmin.value
}

// Enter edit mode for a note: populate form with existing data
function startEditNote(note) {
  editingNoteId.value = note.id
  editingNote.value = {
    title: note.title,
    content: note.content,
    is_public: note.is_public || false,
  }
}

// Exit edit mode and clear form without saving
function cancelEditNote() {
  editingNoteId.value = null
  editingNote.value = { title: '', content: '', is_public: false }
}

// Update existing note on server via PUT /api/notes/{id}/
async function saveEditNote(noteId) {
  if (!editingNote.value.title || !editingNote.value.content) {
    toast.value?.showToast('Please provide both a title and content.', 'error')
    return
  }

  try {
    const res = await axios.put(`/api/notes/${noteId}/`, {
      title: editingNote.value.title,
      content: editingNote.value.content,
      is_public: editingNote.value.is_public,
    })
    
    if (res.status === 200) {
      // Update note in local array after server confirmation
      const noteIndex = notes.value.findIndex(n => n.id === noteId)
      if (noteIndex !== -1) {
        notes.value[noteIndex] = res.data
      }
      editingNoteId.value = null
      editingNote.value = { title: '', content: '', is_public: false }
      toast.value?.showToast('Note updated successfully!', 'success', 2000)
    } else {
      toast.value?.showToast('Failed to update note.', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error updating note.', 'error')
  }
}

async function deleteNote(noteId) {
  // Confirm deletion with user before sending DELETE request
  if (!confirm('Are you sure you want to delete this note?')) {
    return
  }

  try {
    const res = await axios.delete(`/api/notes/${noteId}/`)
    
    if (res.status === 204 || res.status === 200) {
      // Remove deleted note from local array
      notes.value = notes.value.filter(n => n.id !== noteId)
      toast.value?.showToast('Note deleted successfully!', 'success', 2000)
    } else {
      toast.value?.showToast('Failed to delete note.', 'error')
    }
  } catch (err) {
    toast.value?.showToast(err?.response?.data?.detail || 'Error deleting note.', 'error')
  }
}

// ============================================================================
// AUTHENTICATION: Login, registration, token management, logout
// ============================================================================

// Submit login form: POST username/password to /api/token/ endpoint
async function submitLogin() {
  try {
    const res = await axios.post('/api/token/', {
      username: username.value,
      password: password.value,
    })
    if (res && res.data && res.data.access) {
      // Save tokens to localStorage and update auth state
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

// Submit registration form: POST to /api/auth/signup/ endpoint
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
  if (!newNoteContent.value) {
    toast.value?.showToast('Please provide content.', 'error')
    return
  }
  const lessonId = selectedLessonId.value || lessonOptions.value[0]?.id
  if (!lessonId) {
    toast.value?.showToast('Please select a lesson first.', 'error')
    return
  }
  try {
    const res = await axios.post('/api/notes/', {
      lesson: lessonId,
      title: newNoteTitle.value,
      content: newNoteContent.value,
      is_public: newNoteIsPublic.value,
    })
    if (res.status === 201) {
      notes.value.push(res.data)
      newNoteTitle.value = ''
      newNoteContent.value = ''
      newNoteIsPublic.value = false
      selectedLessonId.value = ''
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
    if (res && (res.status === 201 || res.status === 200)) {
      toast.value?.showToast('Enrolled successfully!', 'success', 2000)
    } else {
      // server didn't create enrollment; leave optimistic state (user will see server state on refresh)
    }
  } catch (err) {
    // On error (e.g., 401), revert optimistic update and prompt login
    if (err?.response?.status === 401) {
      // Revert optimistic enrollment update if auth failed
      if (addedOptimistically) enrolledCourses.value = enrolledCourses.value.filter(id => id !== courseId)
      view.value = 'login'
      return
    }
    console.error('Enrollment failed', err)
  }
}

// ============================================================================
// SESSION MANAGEMENT: Logout and navigation helpers
// ============================================================================

// Clear authentication tokens and reset UI to home
function logout() {
  clearAuth()
  refreshAuthState()
  toast.value?.showToast('See you next time!', 'success', 1500)
  view.value = 'home'
}

// Navigate to login view if not already logged in
function goToLogin() { 
  if (isLoggedIn.value) { view.value = 'home'; return }
  view.value = 'login' 
}

// Navigate to register view if not already logged in
function goToRegister() { 
  if (isLoggedIn.value) { view.value = 'home'; return }
  view.value = 'register' 
}

// ============================================================================
// VIDEO EMBEDDING: Convert oembed/watch URLs to responsive YouTube iframes
// ============================================================================

// Process HTML to convert <oembed> tags and YouTube URLs into responsive embed iframes
// Handles: YouTube watch URLs (youtube.com/watch?v=ID), short URLs (youtu.be/ID), embed URLs
function processEmbeds(html) {
  if (!html) return ''
  try {
    return html.replace(/<oembed[^>]*url=["']([^"']+)["'][^>]*>(?:<\/oembed>)?/gi, (m, url) => {
      let embedSrc = url
      // Convert YouTube watch/short URLs to embed format to fix Error 153
      if (/youtube\.com\/watch/.test(url) || /youtu\.be\//.test(url)) {
        const ytMatch = url.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{6,})/)
        const vid = ytMatch ? ytMatch[1] : null
        if (vid) embedSrc = `https://www.youtube.com/embed/${vid}`
      }
      // Return responsive iframe with 16:9 aspect ratio (padding-bottom: 56.25%)
      return `<div class="media-embed" style="position:relative;padding-bottom:56.25%;height:0;overflow:hidden;max-width:100%;"><iframe src="${embedSrc}" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="position:absolute;top:0;left:0;width:100%;height:100%;border:0"></iframe></div>`
    })
  } catch (e) {
    return html
  }
}

</script>

<style scoped>
.nav-btn {
  @apply text-sm text-white/80 hover:text-white transition focus:outline-none focus:ring-2 focus:ring-indigo-400 focus:ring-offset-2 focus:ring-offset-transparent rounded px-2 py-1;
}

.card {
  @apply bg-[rgba(255,255,255,0.05)] rounded-xl p-6 shadow-lg hover:shadow-xl transition;
}

.btn {
  @apply px-4 py-2 rounded-md bg-teal-400 text-black font-semibold hover:bg-teal-300 transition focus:outline-none focus:ring-2 focus:ring-teal-200 focus:ring-offset-2 focus:ring-offset-mb-bg;
}

.btn-lg {
  @apply px-6 py-3 rounded-lg font-bold shadow-md hover:opacity-90 transition focus:outline-none focus:ring-2 focus:ring-indigo-300 focus:ring-offset-2 focus:ring-offset-mb-bg;
}

.cta-btn {
  @apply px-6 py-3 rounded-lg font-bold shadow-md transition focus:outline-none focus:ring-2 focus:ring-mb-primary focus:ring-offset-2 focus:ring-offset-mb-bg;
}

.input {
  @apply bg-[rgba(255,255,255,0.05)] border border-white/10 p-3 rounded-md outline-none 
         text-lg text-white placeholder:text-white/40 focus:ring-2 focus:ring-indigo-400 focus:border-indigo-400 transition;
}

/* Accessibility: Screen reader only text for skip links */
.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.focus\:not-sr-only:focus {
  position: static;
  width: auto;
  height: auto;
  padding: inherit;
  margin: inherit;
  overflow: visible;
  clip: auto;
  white-space: normal;
}

</style> 