import { createRouter, createWebHistory } from 'vue-router'
import CourseList from './components/CourseList.vue'
import CourseDetail from './components/CourseDetail.vue'
import HomeFallback from './components/HomeFallback.vue'

const routes = [
  { path: '/', name: 'home', component: HomeFallback },
  { path: '/courses', name: 'courses', component: CourseList },
  { path: '/courses/:id', name: 'course-detail', component: CourseDetail, props: true },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router
