/**
 * Application Routes Configuration
 * Vue Router configuration with route definitions and guards
 */

import { createRouter, createWebHistory } from 'vue-router'
import { ROUTE_PATHS } from './route-paths.js'

// Lazy-loaded components for better performance
const HomeView = () => import('@/views/HomeView.vue')
const PatientView = () => import('@/views/PatientView.vue')
const RecordingView = () => import('@/views/RecordingView.vue')
const DocumentsView = () => import('@/views/DocumentsView.vue')

/**
 * Application Routes Configuration
 */
export const appRoutes = [
  {
    path: ROUTE_PATHS.HOME,
    name: 'Home',
    component: HomeView,
    meta: {
      title: 'Home',
      description: 'Speech-to-Text Medical System Homepage',
      requiresAuth: false
    }
  },
  {
    path: ROUTE_PATHS.PATIENTS,
    name: 'Patients',
    component: PatientView,
    meta: {
      title: 'Patient Management',
      description: 'Manage patient records and information',
      requiresAuth: false
    }
  },
  {
    path: ROUTE_PATHS.RECORDING,
    name: 'Recording',
    component: RecordingView,
    meta: {
      title: 'Audio Recording',
      description: 'Record medical observations and save them',
      requiresAuth: false
    }
  },
  {
    path: ROUTE_PATHS.DOCUMENTS,
    name: 'Documents',
    component: DocumentsView,
    meta: {
      title: 'Document Templates',
      description: 'Fill document templates with voice input',
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: ROUTE_PATHS.HOME
  }
]

/**
 * Navigation menu configuration
 */
export const navigationMenu = [
  {
    path: ROUTE_PATHS.HOME,
    name: 'Home',
    icon: '🏠',
    requiresAuth: false
  },
  {
    path: ROUTE_PATHS.PATIENTS,
    name: 'Patients',
    icon: '👥',
    requiresAuth: false
  },
  {
    path: ROUTE_PATHS.RECORDING,
    name: 'Recording',
    icon: '🎙️',
    requiresAuth: false
  },
  {
    path: ROUTE_PATHS.DOCUMENTS,
    name: 'Documents',
    icon: '📄',
    requiresAuth: false
  },
]

/**
 * Create and configure the router
 */
export const createAppRouter = () => {
  const router = createRouter({
    history: createWebHistory(),
    routes: appRoutes
  })

  // Global navigation guards
  router.beforeEach((to, from, next) => {
    // Set page title from route meta
    if (to.meta?.title) {
      document.title = `${to.meta.title} - Speech-to-Text Medical System`
    }
    
    // Allow all routes without authentication
    next()
  })

  // Error handling
  router.onError((error) => {
    console.error('Router error:', error)
    // Redirect to home on error
    router.push('/')
  })

  return router
}
