import { authService } from './AuthService.js'

const API_BASE_URL = 'http://127.0.0.1:8000/api'

class ApiClient {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const authHeaders = authService.getAuthHeader()
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...authHeaders,
        ...options.headers,
      },
    }

    if (authHeaders.Authorization) {
      console.log(' Sending Authorization header:', authHeaders.Authorization.substring(0, 20) + '...')
    } else {
      console.warn(' No Authorization header found!')
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        if (response.status === 401) {
          console.warn('Session expired or invalid. Clearing auth and redirecting to login...')
          authService.clearAuth()
          window.dispatchEvent(new Event('auth-changed'))
          throw new Error('Session expired or invalid. Please login again.')
        }
        
        const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
      }

      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async get(endpoint) {
    return this.request(endpoint, { method: 'GET' })
  }

  async post(endpoint, data) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    })
  }

  async put(endpoint, data) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  }

  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' })
  }

  async getPatients() {
    return this.get('/patients/')
  }

  async getPatient(id) {
    return this.get(`/patients/${id}`)
  }

  async createPatient(patient) {
    return this.post('/patients', patient)
  }

  async updatePatient(id, patient) {
    return this.put(`/patients/${id}`, patient)
  }

  async deletePatient(id) {
    return this.delete(`/patients/${id}`)
  }

  async getDocuments() {
    return this.get('/documents')
  }

  async getDocumentsByPatient(patientId) {
    return this.get(`/documents/patient/${patientId}`)
  }

  async getDocument(id) {
    return this.get(`/documents/${id}`)
  }

  async createDocument(document) {
    return this.post('/documents', document)
  }

  async updateDocument(id, document) {
    return this.put(`/documents/${id}`, document)
  }

  async deleteDocument(id) {
    return this.delete(`/documents/${id}`)
  }

  async transcribeAudio(audioFile) {
    const formData = new FormData()
    formData.append('audio_file', audioFile)

    const response = await fetch(`${this.baseURL}/transcribe`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ detail: 'Unknown error' }))
      throw new Error(errorData.detail || `HTTP error! status: ${response.status}`)
    }

    return await response.json()
  }

  async testConnection() {
    try {
      console.log('🔍 Testing connection to:', this.baseURL)
      const response = await fetch('http://127.0.0.1:8000/health')
      const data = await response.json()
      console.log('✅ Backend is reachable:', data)
      return { success: true, data }
    } catch (error) {
      console.error('❌ Backend connection failed:', error)
      return { success: false, error: error.message }
    }
  }
}

export const apiClient = new ApiClient()

apiClient.testConnection()
