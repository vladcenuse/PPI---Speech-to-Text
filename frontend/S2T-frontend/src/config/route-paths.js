/**
 * Route Paths Configuration
 * Centralized route path definitions for consistent navigation
 */

export const ROUTE_PATHS = {
  // Main Routes
  HOME: '/',
  PATIENTS: '/patients',
  RECORDING: '/recording',
  DOCUMENTS: '/documents',
  
  // Patient Routes
  PATIENT_LIST: '/patients',
  PATIENT_CREATE: '/patients/create',
  PATIENT_EDIT: '/patients/edit/:id',
  PATIENT_DETAILS: '/patients/:id',
  
  
  // Export Routes
  EXPORT_PATIENT: '/export/patient/:id',
  EXPORT_LIST: '/export/list',
  
  // Settings Routes
  SETTINGS: '/settings',
  PROFILE: '/profile',
  
  // Error Routes
  NOT_FOUND: '/404',
  ERROR: '/error'
}

// Helper function to generate dynamic routes
export const generateRoute = (path, params = {}) => {
  let route = path
  
  Object.entries(params).forEach(([key, value]) => {
    route = route.replace(`:${key}`, String(value))
  })
  
  return route
}

// Route path validation
export const isValidRoute = (path) => {
  return Object.values(ROUTE_PATHS).includes(path)
}
