<template>
  <div class="documents-view">
    <HeaderBar />
    <main class="main-content">
      <div class="page-header">
        <h2>Document Templates</h2>
        <p>Select a document template and fill it with patient data using voice input</p>
      </div>

      <!-- Document Type Selection -->
      <div v-if="!selectedDocument" class="document-selection">
        <h3>Choose Document Type</h3>
        <div class="document-grid">
          <div 
            v-for="document in documentTypes" 
            :key="document.id"
            class="document-card"
            @click="selectDocument(document)"
          >
            <div class="document-icon">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
              </svg>
            </div>
            <h4>{{ document.name }}</h4>
            <p>{{ document.description }}</p>
          </div>
        </div>
      </div>

      <!-- Document Form -->
      <div v-else class="document-form">
        <div class="form-header">
          <div class="form-title">
            <button @click="goBack" class="back-button">
              <svg viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/>
              </svg>
            </button>
            <h3>{{ selectedDocument.name }}</h3>
          </div>
          <div class="form-actions">
            <div class="mic-controls">
              <button 
                @click="toggleMicrophone" 
                :class="['mic-button', { 'mic-button--active': isMicActive }]"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
                  <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
                </svg>
                <span>{{ isMicActive ? 'Stop Recording' : 'Start Recording' }}</span>
              </button>
            </div>
            
            <div class="export-controls">
              <button 
                @click="exportToPDF" 
                class="export-button pdf-button"
                :disabled="!hasFormData"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
                <span>Export PDF</span>
              </button>
              
              <button 
                @click="exportToWord" 
                class="export-button word-button"
                :disabled="!hasFormData"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
                </svg>
                <span>Export Word</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Document Content -->
        <div class="document-content">
          <component 
            :is="selectedDocument.component" 
            :patient-data="patientData"
            :is-recording="isMicActive"
            @field-click="handleFieldClick"
            @field-update="handleFieldUpdate"
          />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import HeaderBar from '@/components/layout/HeaderBar.vue'
import MedicalReport from '@/components/documents/MedicalReport.vue'
import ConsultationForm from '@/components/documents/ConsultationForm.vue'
import PrescriptionForm from '@/components/documents/PrescriptionForm.vue'
import FirstTimeNewPatient from '@/components/documents/FirstTimeNewPatient.vue'
import { toastService } from '@/services/ToastService.js'

// Document types
const documentTypes = [
  {
    id: 'first-time-patient',
    name: 'First Time New Patient',
    description: 'Comprehensive initial patient assessment and intake form',
    component: FirstTimeNewPatient
  },
  {
    id: 'medical-report',
    name: 'Medical Report',
    description: 'Comprehensive medical examination report',
    component: MedicalReport
  },
  {
    id: 'consultation',
    name: 'Consultation Form',
    description: 'Patient consultation and diagnosis form',
    component: ConsultationForm
  },
  {
    id: 'prescription',
    name: 'Prescription Form',
    description: 'Medication prescription and treatment plan',
    component: PrescriptionForm
  }
]

// State
const selectedDocument = ref(null)
const isMicActive = ref(false)
const currentField = ref(null)
const patientData = reactive({
  patientName: '',
  patientId: '',
  date: new Date().toISOString().split('T')[0],
  // Medical Report fields
  chiefComplaint: '',
  historyOfPresentIllness: '',
  physicalExamination: '',
  diagnosis: '',
  treatment: '',
  recommendations: '',
  // Consultation fields
  symptoms: '',
  vitalSigns: '',
  assessment: '',
  plan: '',
  // Prescription fields
  medications: '',
  dosage: '',
  instructions: '',
  followUp: ''
})

// Methods
const selectDocument = (document) => {
  selectedDocument.value = document
}

const goBack = () => {
  selectedDocument.value = null
  isMicActive.value = false
  currentField.value = null
}

const toggleMicrophone = () => {
  isMicActive.value = !isMicActive.value
  if (isMicActive.value) {
    console.log('Microphone activated')
    // TODO: Implement actual microphone functionality
  } else {
    console.log('Microphone deactivated')
    currentField.value = null
  }
}

const handleFieldClick = (fieldName) => {
  if (isMicActive.value) {
    currentField.value = fieldName
    console.log(`Recording for field: ${fieldName}`)
  }
}

const handleFieldUpdate = (fieldName, value) => {
  if (patientData.hasOwnProperty(fieldName)) {
    patientData[fieldName] = value
  }
}

// Computed property to check if form has data
const hasFormData = computed(() => {
  return Object.values(patientData).some(value => 
    value && value.toString().trim() !== ''
  )
})

// Export functionality
const exportToPDF = () => {
  if (!hasFormData.value) {
    toastService.warning('No data to export', 'Please fill in some form data before exporting')
    return
  }
  
  try {
    // Generate PDF content
    const pdfContent = generatePDFContent()
    
    // Create and download PDF
    const blob = new Blob([pdfContent], { type: 'application/pdf' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${selectedDocument.value.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    toastService.success('PDF exported!', 'Document has been downloaded successfully')
  } catch (error) {
    console.error('PDF export failed:', error)
    toastService.error('Export failed', 'Could not generate PDF file')
  }
}

const exportToWord = () => {
  if (!hasFormData.value) {
    toastService.warning('No data to export', 'Please fill in some form data before exporting')
    return
  }
  
  try {
    // Generate Word content
    const wordContent = generateWordContent()
    
    // Create and download Word document
    const blob = new Blob([wordContent], { type: 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${selectedDocument.value.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.docx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
    
    toastService.success('Word document exported!', 'Document has been downloaded successfully')
  } catch (error) {
    console.error('Word export failed:', error)
    toastService.error('Export failed', 'Could not generate Word document')
  }
}

// Generate PDF content
const generatePDFContent = () => {
  const documentName = selectedDocument.value.name
  const currentDate = new Date().toLocaleDateString()
  
  let content = `
    <html>
      <head>
        <title>${documentName}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
          h1 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
          h2 { color: #555; margin-top: 30px; }
          .field { margin: 15px 0; }
          .label { font-weight: bold; color: #333; }
          .value { margin-left: 20px; color: #666; }
          .empty { color: #999; font-style: italic; }
        </style>
      </head>
      <body>
        <h1>${documentName}</h1>
        <p><strong>Generated on:</strong> ${currentDate}</p>
        <hr>
  `
  
  // Add form data based on document type
  Object.entries(patientData).forEach(([key, value]) => {
    if (value && value.toString().trim() !== '') {
      const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
      content += `
        <div class="field">
          <div class="label">${label}:</div>
          <div class="value">${value}</div>
        </div>
      `
    }
  })
  
  content += `
      </body>
    </html>
  `
  
  return content
}

// Generate Word content
const generateWordContent = () => {
  const documentName = selectedDocument.value.name
  const currentDate = new Date().toLocaleDateString()
  
  let content = `
    <html xmlns:o="urn:schemas-microsoft-com:office:office"
          xmlns:w="urn:schemas-microsoft-com:office:word"
          xmlns="http://www.w3.org/TR/REC-html40">
      <head>
        <meta charset="utf-8">
        <title>${documentName}</title>
        <style>
          body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
          h1 { color: #333; border-bottom: 2px solid #667eea; padding-bottom: 10px; }
          h2 { color: #555; margin-top: 30px; }
          .field { margin: 15px 0; }
          .label { font-weight: bold; color: #333; }
          .value { margin-left: 20px; color: #666; }
        </style>
      </head>
      <body>
        <h1>${documentName}</h1>
        <p><strong>Generated on:</strong> ${currentDate}</p>
        <hr>
  `
  
  // Add form data based on document type
  Object.entries(patientData).forEach(([key, value]) => {
    if (value && value.toString().trim() !== '') {
      const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
      content += `
        <div class="field">
          <div class="label">${label}:</div>
          <div class="value">${value}</div>
        </div>
      `
    }
  })
  
  content += `
      </body>
    </html>
  `
  
  return content
}
</script>

<style scoped>
.documents-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.documents-view::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.2) 0%, transparent 50%);
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(1deg); }
  66% { transform: translateY(10px) rotate(-1deg); }
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 2rem;
  position: relative;
  z-index: 1;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 3.5rem;
  font-weight: 700;
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  background: linear-gradient(45deg, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
}

.page-header p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.4rem;
  font-weight: 300;
  line-height: 1.6;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

/* Document Selection */
.document-selection h3 {
  text-align: center;
  color: white;
  margin-bottom: 2rem;
  font-size: 1.8rem;
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.document-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-top: 2rem;
}

.document-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.document-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.document-card:hover::before {
  opacity: 1;
}

.document-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.document-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.document-card:hover .document-icon {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6);
}

.document-icon svg {
  width: 40px;
  height: 40px;
  transition: transform 0.3s ease;
}

.document-card:hover .document-icon svg {
  transform: scale(1.1);
}

.document-card h4 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.document-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  font-size: 1rem;
  font-weight: 300;
  text-shadow: 0 1px 5px rgba(0,0,0,0.3);
}

/* Document Form */
.document-form {
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  overflow: hidden;
}

.form-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 1.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-title {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-button {
  background: rgba(255, 255, 255, 0.2);
  border: none;
  color: white;
  padding: 0.5rem;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.back-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

.back-button svg {
  width: 20px;
  height: 20px;
}

.form-title h3 {
  margin: 0;
  font-size: 1.5rem;
}

.mic-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.mic-button {
  background: rgba(255, 255, 255, 0.2);
  border: 2px solid rgba(255, 255, 255, 0.3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.mic-button:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
}

.mic-button--active {
  background: #e74c3c;
  border-color: #c0392b;
  animation: pulse 2s infinite;
}

.mic-button svg {
  width: 20px;
  height: 20px;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.export-controls {
  display: flex;
  gap: 0.75rem;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.25rem;
  border-radius: 12px;
  font-weight: 600;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(20px);
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.export-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.export-button:hover::before {
  left: 100%;
}

.export-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
}

.pdf-button {
  background: rgba(220, 38, 38, 0.2);
  color: white;
  border: 1px solid rgba(220, 38, 38, 0.4);
}

.pdf-button:hover:not(:disabled) {
  background: rgba(220, 38, 38, 0.3);
  border-color: rgba(220, 38, 38, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(220, 38, 38, 0.4);
}

.word-button {
  background: rgba(0, 120, 212, 0.2);
  color: white;
  border: 1px solid rgba(0, 120, 212, 0.4);
}

.word-button:hover:not(:disabled) {
  background: rgba(0, 120, 212, 0.3);
  border-color: rgba(0, 120, 212, 0.6);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 120, 212, 0.4);
}

.export-button svg {
  width: 18px;
  height: 18px;
}

.document-content {
  padding: 2rem;
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .form-header {
    flex-direction: column;
    gap: 1rem;
    text-align: center;
  }
  
  .mic-controls {
    width: 100%;
    justify-content: center;
  }
}
</style>
