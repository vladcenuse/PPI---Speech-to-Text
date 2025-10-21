<script setup>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'

// State management
const currentView = ref('dashboard')
const patientFiles = ref([])
const currentPatientFile = ref(null)
const isLoading = ref(false)
const audioFile = ref(null)
const transcriptionResult = ref(null)

// Form data for new patient file
const newPatientFile = ref({
  patient_name: '',
  patient_id: '',
  date: new Date().toISOString().split('T')[0],
  doctor_name: 'Dr. Alina Baciu',
  anamneza: '',
  examen_clinic: '',
  diagnostic: '',
  tratament: '',
  recomandari: '',
  observatii: ''
})

// API base URL
const API_BASE = 'http://127.0.0.1:8000'

// Load patient files on mount
onMounted(async () => {
  await loadPatientFiles()
})

// Load all patient files
const loadPatientFiles = async () => {
  try {
    const response = await axios.get(`${API_BASE}/api/patient-files`)
    patientFiles.value = response.data
  } catch (error) {
    console.error('Error loading patient files:', error)
  }
}

// Create new patient file
const createPatientFile = async () => {
  try {
    isLoading.value = true
    const response = await axios.post(`${API_BASE}/api/patient-files`, newPatientFile.value)
    patientFiles.value.push(response.data)
    resetForm()
    currentView.value = 'dashboard'
  } catch (error) {
    console.error('Error creating patient file:', error)
  } finally {
    isLoading.value = false
  }
}

// Upload and transcribe audio
const uploadAudio = async () => {
  if (!audioFile.value) return
  
  try {
    isLoading.value = true
    const formData = new FormData()
    formData.append('file', audioFile.value)
    
    const response = await axios.post(`${API_BASE}/api/transcribe-audio`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    
    transcriptionResult.value = response.data
    
    // Auto-fill the form with transcribed data
    if (response.data.extracted_data) {
      const data = response.data.extracted_data
      newPatientFile.value.anamneza = data.anamneza || ''
      newPatientFile.value.examen_clinic = data.examen_clinic || ''
      newPatientFile.value.diagnostic = data.diagnostic || ''
      newPatientFile.value.tratament = data.tratament || ''
      newPatientFile.value.recomandari = data.recomandari || ''
      newPatientFile.value.observatii = data.observatii || ''
    }
    
  } catch (error) {
    console.error('Error transcribing audio:', error)
  } finally {
    isLoading.value = false
  }
}

// Handle file selection
const handleFileSelect = (event) => {
  audioFile.value = event.target.files[0]
}

// Export to Word
const exportToWord = async (fileId) => {
  try {
    const response = await axios.get(`${API_BASE}/api/export-to-word/${fileId}`, {
      responseType: 'blob'
    })
    
    const url = window.URL.createObjectURL(new Blob([response.data]))
    const link = document.createElement('a')
    link.href = url
    link.setAttribute('download', `fisa_pacient_${fileId}.docx`)
    document.body.appendChild(link)
    link.click()
    link.remove()
  } catch (error) {
    console.error('Error exporting to Word:', error)
  }
}

// Reset form
const resetForm = () => {
  newPatientFile.value = {
    patient_name: '',
    patient_id: '',
    date: new Date().toISOString().split('T')[0],
    doctor_name: 'Dr. Alina Baciu',
    anamneza: '',
    examen_clinic: '',
    diagnostic: '',
    tratament: '',
    recomandari: '',
    observatii: ''
  }
  audioFile.value = null
  transcriptionResult.value = null
}

// View patient file details
const viewPatientFile = (file) => {
  currentPatientFile.value = file
  currentView.value = 'view'
}

// Delete patient file
const deletePatientFile = async (fileId) => {
  if (!confirm('Sigur doriți să ștergeți această fișă?')) return
  
  try {
    await axios.delete(`${API_BASE}/api/patient-files/${fileId}`)
    patientFiles.value = patientFiles.value.filter(f => f.id !== fileId)
  } catch (error) {
    console.error('Error deleting patient file:', error)
  }
}

// Computed properties
const hasTranscription = computed(() => transcriptionResult.value && transcriptionResult.value.status === 'completed')
</script>

<template>
  <div class="app">
    <!-- Header -->
    <header class="header">
      <h1>🎙️ Asistent Medical Voice-to-Text</h1>
      <p class="subtitle">Dr. Alina Baciu - Automatizarea întocmirii fișei pacientului</p>
    </header>

    <!-- Navigation -->
    <nav class="nav">
      <button 
        @click="currentView = 'dashboard'" 
        :class="{ active: currentView === 'dashboard' }"
        class="nav-btn"
      >
        📋 Dashboard
      </button>
      <button 
        @click="currentView = 'create'; resetForm()" 
        :class="{ active: currentView === 'create' }"
        class="nav-btn"
      >
        ➕ Fișă Nouă
      </button>
    </nav>

    <!-- Dashboard View -->
    <div v-if="currentView === 'dashboard'" class="dashboard">
      <h2>Fișe Pacienți</h2>
      
      <div v-if="patientFiles.length === 0" class="empty-state">
        <p>Nu există fișe pacienți încă.</p>
        <button @click="currentView = 'create'" class="btn btn-primary">
          Creează Prima Fișă
        </button>
      </div>

      <div v-else class="patient-files-grid">
        <div v-for="file in patientFiles" :key="file.id" class="patient-file-card">
          <div class="file-header">
            <h3>{{ file.patient_name }}</h3>
            <span class="file-id">ID: {{ file.patient_id }}</span>
          </div>
          
          <div class="file-info">
            <p><strong>Data:</strong> {{ new Date(file.date).toLocaleDateString('ro-RO') }}</p>
            <p><strong>Medic:</strong> {{ file.doctor_name }}</p>
            <p><strong>Status:</strong> 
              <span :class="`status status-${file.transcription_status}`">
                {{ file.transcription_status }}
              </span>
            </p>
          </div>

          <div class="file-actions">
            <button @click="viewPatientFile(file)" class="btn btn-secondary">
              👁️ Vezi
            </button>
            <button @click="exportToWord(file.id)" class="btn btn-success">
              📄 Export Word
            </button>
            <button @click="deletePatientFile(file.id)" class="btn btn-danger">
              🗑️ Șterge
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Patient File View -->
    <div v-if="currentView === 'create'" class="create-form">
      <h2>Fișă Pacient Nouă</h2>
      
      <div class="form-section">
        <h3>📁 Informații Pacient</h3>
        <div class="form-row">
          <div class="form-group">
            <label>Nume Pacient:</label>
            <input v-model="newPatientFile.patient_name" type="text" required>
          </div>
          <div class="form-group">
            <label>ID Pacient:</label>
            <input v-model="newPatientFile.patient_id" type="text" required>
          </div>
          <div class="form-group">
            <label>Data:</label>
            <input v-model="newPatientFile.date" type="date" required>
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3>🎙️ Încărcare Audio</h3>
        <div class="audio-upload">
          <input 
            @change="handleFileSelect" 
            type="file" 
            accept="audio/*" 
            id="audio-file"
            class="file-input"
          >
          <label for="audio-file" class="file-label">
            {{ audioFile ? audioFile.name : 'Selectează fișier audio...' }}
          </label>
          <button 
            @click="uploadAudio" 
            :disabled="!audioFile || isLoading"
            class="btn btn-primary"
          >
            {{ isLoading ? '⏳ Procesează...' : '🎤 Transcrie Audio' }}
          </button>
        </div>

        <div v-if="hasTranscription" class="transcription-result">
          <h4>✅ Transcriere Completă</h4>
          <p>{{ transcriptionResult.transcription }}</p>
        </div>
      </div>

      <div class="form-section">
        <h3>📝 Secțiuni Medicale</h3>
        <div class="medical-sections">
          <div class="form-group">
            <label>Anamneză:</label>
            <textarea v-model="newPatientFile.anamneza" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label>Examen Clinic:</label>
            <textarea v-model="newPatientFile.examen_clinic" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label>Diagnostic:</label>
            <textarea v-model="newPatientFile.diagnostic" rows="2"></textarea>
          </div>
          
          <div class="form-group">
            <label>Tratament:</label>
            <textarea v-model="newPatientFile.tratament" rows="3"></textarea>
          </div>
          
          <div class="form-group">
            <label>Recomandări:</label>
            <textarea v-model="newPatientFile.recomandari" rows="2"></textarea>
          </div>
          
          <div class="form-group">
            <label>Observații:</label>
            <textarea v-model="newPatientFile.observatii" rows="2"></textarea>
          </div>
        </div>
      </div>

      <div class="form-actions">
        <button @click="currentView = 'dashboard'" class="btn btn-secondary">
          ❌ Anulează
        </button>
        <button 
          @click="createPatientFile" 
          :disabled="isLoading || !newPatientFile.patient_name || !newPatientFile.patient_id"
          class="btn btn-primary"
        >
          {{ isLoading ? '⏳ Salvează...' : '💾 Salvează Fișa' }}
        </button>
      </div>
    </div>

    <!-- View Patient File -->
    <div v-if="currentView === 'view' && currentPatientFile" class="view-file">
      <div class="view-header">
        <h2>{{ currentPatientFile.patient_name }}</h2>
        <button @click="currentView = 'dashboard'" class="btn btn-secondary">
          ← Înapoi
        </button>
      </div>

      <div class="file-details">
        <div class="detail-section">
          <h3>Informații Pacient</h3>
          <p><strong>ID:</strong> {{ currentPatientFile.patient_id }}</p>
          <p><strong>Data:</strong> {{ new Date(currentPatientFile.date).toLocaleDateString('ro-RO') }}</p>
          <p><strong>Medic:</strong> {{ currentPatientFile.doctor_name }}</p>
        </div>

        <div class="detail-section">
          <h3>Anamneză</h3>
          <p>{{ currentPatientFile.anamneza || 'Nu este completat' }}</p>
        </div>

        <div class="detail-section">
          <h3>Examen Clinic</h3>
          <p>{{ currentPatientFile.examen_clinic || 'Nu este completat' }}</p>
        </div>

        <div class="detail-section">
          <h3>Diagnostic</h3>
          <p>{{ currentPatientFile.diagnostic || 'Nu este completat' }}</p>
        </div>

        <div class="detail-section">
          <h3>Tratament</h3>
          <p>{{ currentPatientFile.tratament || 'Nu este completat' }}</p>
        </div>

        <div class="detail-section">
          <h3>Recomandări</h3>
          <p>{{ currentPatientFile.recomandari || 'Nu este completat' }}</p>
        </div>

        <div class="detail-section">
          <h3>Observații</h3>
          <p>{{ currentPatientFile.observatii || 'Nu este completat' }}</p>
        </div>
      </div>

      <div class="view-actions">
        <button @click="exportToWord(currentPatientFile.id)" class="btn btn-success">
          📄 Export Word
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.app {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 10px;
}

.header h1 {
  margin: 0 0 10px 0;
  font-size: 2.5rem;
}

.subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1rem;
}

.nav {
  display: flex;
  gap: 10px;
  margin-bottom: 30px;
  justify-content: center;
}

.nav-btn {
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  background: #f8f9fa;
  color: #495057;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.nav-btn:hover {
  background: #e9ecef;
  transform: translateY(-2px);
}

.nav-btn.active {
  background: #007bff;
  color: white;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  margin: 5px;
}

.btn-primary {
  background: #007bff;
  color: white;
}

.btn-secondary {
  background: #6c757d;
  color: white;
}

.btn-success {
  background: #28a745;
  color: white;
}

.btn-danger {
  background: #dc3545;
  color: white;
}

.btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.dashboard h2 {
  color: #333;
  margin-bottom: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  background: #f8f9fa;
  border-radius: 10px;
  border: 2px dashed #dee2e6;
}

.patient-files-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
}

.patient-file-card {
  background: white;
  border: 1px solid #dee2e6;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.patient-file-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.file-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.file-header h3 {
  margin: 0;
  color: #333;
}

.file-id {
  background: #e9ecef;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 0.8rem;
  color: #6c757d;
}

.file-info p {
  margin: 5px 0;
  color: #666;
}

.status {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: bold;
}

.status-pending {
  background: #fff3cd;
  color: #856404;
}

.status-completed {
  background: #d4edda;
  color: #155724;
}

.status-error {
  background: #f8d7da;
  color: #721c24;
}

.file-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.create-form, .view-file {
  background: white;
  border-radius: 10px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.form-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.form-section h3 {
  margin-top: 0;
  color: #333;
  border-bottom: 2px solid #007bff;
  padding-bottom: 10px;
}

.form-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 1rem;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  min-height: 80px;
}

.audio-upload {
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.file-input {
  display: none;
}

.file-label {
  padding: 10px 20px;
  background: #e9ecef;
  border: 2px dashed #6c757d;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 200px;
  text-align: center;
}

.file-label:hover {
  background: #dee2e6;
  border-color: #007bff;
}

.transcription-result {
  margin-top: 15px;
  padding: 15px;
  background: #d4edda;
  border: 1px solid #c3e6cb;
  border-radius: 6px;
  color: #155724;
}

.medical-sections {
  display: grid;
  gap: 15px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 15px;
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.view-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #007bff;
}

.view-header h2 {
  margin: 0;
  color: #333;
}

.file-details {
  display: grid;
  gap: 20px;
}

.detail-section {
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #007bff;
}

.detail-section h3 {
  margin-top: 0;
  color: #333;
}

.detail-section p {
  margin: 10px 0;
  line-height: 1.6;
  color: #555;
}

.view-actions {
  margin-top: 30px;
  text-align: center;
}

@media (max-width: 768px) {
  .app {
    padding: 10px;
  }
  
  .header h1 {
    font-size: 2rem;
  }
  
  .nav {
    flex-direction: column;
  }
  
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .audio-upload {
    flex-direction: column;
    align-items: stretch;
  }
  
  .file-actions {
    justify-content: center;
  }
}
</style>
