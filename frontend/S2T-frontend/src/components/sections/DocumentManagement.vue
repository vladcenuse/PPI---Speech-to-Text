<template>
  <div class="document-management">
    <div class="page-header">
      <h2>Document Templates</h2>
      <p>Fill document templates with voice input and export them</p>
    </div>

    <!-- Document Selection -->
    <div class="document-selection">
      <h3>Select Document Template</h3>
      <div class="template-grid">
        <div 
          v-for="template in documentTemplates" 
          :key="template.id"
          :class="['template-card', getTemplateCardClass(template), { 'template-card--selected': selectedDocument?.id === template.id }]"
          @click="selectDocument(template)"
        >
          <div class="template-icon" :class="getTemplateIconClass(template)">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
          </div>
          <h4>{{ template.name }}</h4>
          <p>{{ template.description }}</p>
        </div>
      </div>
    </div>

    <!-- Document Form -->
    <div v-if="selectedDocument" class="document-form-section">
      <div class="form-header">
        <div class="form-title-section">
          <h3 v-if="!isEditingTitle">{{ currentFormName || selectedDocument?.name || 'Untitled Form' }}</h3>
          <input 
            v-else
            v-model="currentFormName"
            @blur="finishEditingTitle"
            @keyup.enter="finishEditingTitle"
            class="form-name-input"
            ref="titleInputRef"
          />
          <button 
            @click="startEditingTitle" 
            class="edit-title-btn"
            title="Edit form name"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M20.71,7.04C21.1,6.65 21.1,6 20.71,5.63L18.37,3.29C18,2.9 17.35,2.9 16.96,3.29L15.12,5.12L18.87,8.87M3,17.25V21H6.75L17.81,9.93L14.06,6.18L3,17.25Z"/>
            </svg>
          </button>
        </div>
        <div class="form-actions">
          <button
            @click="saveDocument"
            class="export-button save-button"
            :disabled="!hasFormData"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M15,9H5V5H15M12,19A3,3 0 0,1 9,16A3,3 0 0,1 12,13A3,3 0 0,1 15,16A3,3 0 0,1 12,19M17,3H5C3.89,3 3,3.9 3,5V19A2,2 0 0,0 5,21H19A2,2 0 0,0 21,19V7L17,3Z"/>
            </svg>
            <span>Save Document</span>
          </button>
        </div>
      </div>

      <!-- Patient Selection -->
      <div class="patient-selection-section">
        <div class="patient-selection-header">
          <h4>Select Patient for Document</h4>
          <button 
            @click="showPatientSelector = !showPatientSelector"
            class="patient-selector-toggle"
            :class="{ 'active': showPatientSelector }"
          >
            {{ selectedPatient ? 'Change Patient' : 'Select Patient' }}
            <span class="toggle-icon">{{ showPatientSelector ? '▲' : '▼' }}</span>
          </button>
        </div>
        
        <div v-if="showPatientSelector" class="patient-selector">
          <div class="patient-search">
            <input 
              v-model="patientSearchQuery"
              type="text" 
              placeholder="Search patients..."
              class="patient-search-input"
            />
          </div>
          <div class="patient-list">
            <div 
              v-for="patient in filteredPatients" 
              :key="patient.id"
              class="patient-option"
              :class="{ 'selected': selectedPatient?.id === patient.id }"
              @click="selectPatient(patient)"
            >
              <div class="patient-avatar">
                {{ getPatientInitials(patient.name) }}
              </div>
              <div class="patient-info">
                <div class="patient-name">{{ patient.name }}</div>
                <div class="patient-details">{{ patient.age }} years old • {{ patient.gender }}</div>
              </div>
            </div>
            <div v-if="filteredPatients.length === 0" class="no-patients">
              <p>No patients found. <a href="#" @click.prevent="navigateToPatients">Create a new patient</a></p>
            </div>
          </div>
        </div>
        
        <div v-if="selectedPatient" class="selected-patient-info">
          <div class="selected-patient-avatar">
            {{ getPatientInitials(selectedPatient.name) }}
          </div>
          <div class="selected-patient-details">
            <div class="selected-patient-name">{{ selectedPatient.name }}</div>
            <div class="selected-patient-meta">{{ selectedPatient.age }} years old • {{ selectedPatient.gender }}</div>
          </div>
          <button @click="clearPatientSelection" class="clear-patient-btn">✕</button>
        </div>
      </div>

      <!-- Dynamic Document Component -->
      <div class="document-form">
        <component 
          :is="selectedDocument.component"
          :patient-data="patientData"
          @field-update="handleFieldUpdate"
        />
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="currentColor" class="empty-icon-svg">
          <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
        </svg>
      </div>
      <h3>Select a Document Template</h3>
      <p>Choose a document template from above to start filling out the form.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import MedicalReport from '@/components/documents/MedicalReport.vue'
import ConsultationForm from '@/components/documents/ConsultationForm.vue'
import PrescriptionForm from '@/components/documents/PrescriptionForm.vue'
import FirstTimeNewPatient from '@/components/documents/FirstTimeNewPatient.vue'
import { usePatientViewModel } from '@/viewmodels/PatientViewModel.js'
import { toastService } from '@/services/ToastService.js'

// ViewModels
const patientVM = usePatientViewModel()

// State
const selectedDocument = ref(null)
const selectedPatient = ref(null)
const showPatientSelector = ref(false)
const patientSearchQuery = ref('')
const currentFormName = ref('')
const isEditingTitle = ref(false)
const titleInputRef = ref(null)
const patientData = reactive({
  // Document Information
  date: new Date().toISOString().split('T')[0], // Today's date in YYYY-MM-DD format
  
  // Personal Information
  name: '',
  age: '',
  gender: '',
  phone: '',
  email: '',
  address: '',
  
  // Medical Information
  bloodType: '',
  insuranceNumber: '',
  medicalHistory: '',
  allergies: '',
  currentMedications: '',
  emergencyContact: '',
  
  // Consultation specific
  chiefComplaint: '',
  symptoms: '',
  diagnosis: '',
  treatment: '',
  followUp: '',
  
  // Prescription specific
  medicationName: '',
  dosage: '',
  frequency: '',
  duration: '',
  instructions: '',
  
  // New patient specific
  occupation: '',
  maritalStatus: '',
  preferredLanguage: '',
  referralSource: '',
  
  // First Time New Patient Assessment fields
  patientName: '',
  dateOfBirth: '',
  contactInfo: '',
  presentIllness: '',
  pastMedicalHistory: '',
  medications: '',
  familyHistory: '',
  socialHistory: '',
  vitalSigns: '',
  physicalExam: '',
  assessment: '',
  plan: ''
})

// Document templates
const documentTemplates = ref([
  {
    id: 'medical-report',
    name: 'Medical Report',
    description: 'Comprehensive medical examination report',
    component: MedicalReport
  },
  {
    id: 'consultation-form',
    name: 'Consultation Form',
    description: 'Patient consultation and diagnosis form',
    component: ConsultationForm
  },
  {
    id: 'prescription-form',
    name: 'Prescription Form',
    description: 'Medication prescription and dosage form',
    component: PrescriptionForm
  },
  {
    id: 'new-patient-form',
    name: 'New Patient Form',
    description: 'First-time patient intake form',
    component: FirstTimeNewPatient
  }
])

// Computed properties
const hasFormData = computed(() => {
  return Object.values(patientData).some(value => 
    value && value.toString().trim() !== ''
  )
})

const filteredPatients = computed(() => {
  if (!patientSearchQuery.value.trim()) {
    return patientVM.patients.value || []
  }
  
  const query = patientSearchQuery.value.toLowerCase()
  return (patientVM.patients.value || []).filter(patient => 
    patient.name.toLowerCase().includes(query) ||
    patient.gender.toLowerCase().includes(query) ||
    (patient.age && patient.age.toString().includes(query))
  )
})

// Methods
const selectDocument = (template) => {
  // Check if this is a unique template (New Patient Form)
  if (template.id === 'new-patient-form' && selectedPatient.value) {
    // Check if a New Patient Form already exists for this patient
    const allDocuments = JSON.parse(localStorage.getItem('medicalDocuments') || '[]')
    const existingForm = allDocuments.find(doc => 
      doc.documentId === 'new-patient-form' && 
      doc.patientId === selectedPatient.value.id
    )
    
    if (existingForm) {
      toastService.warning(
        'Form Already Exists',
        `This patient already has a New Patient Form. Please edit the existing form or select a different patient.`
      )
      return
    }
  }
  
  selectedDocument.value = template
  // Always set default form name to template name when selecting a new document
  currentFormName.value = template.name
  // Update date to today's date when selecting a new document
  patientData.date = new Date().toISOString().split('T')[0]
  console.log('Selected document:', template.name)
  console.log('Current form name:', currentFormName.value)
}

const startEditingTitle = () => {
  // Ensure we have a value before editing
  if (!currentFormName.value || currentFormName.value.trim() === '') {
    currentFormName.value = selectedDocument.value?.name || 'Untitled Form'
  }
  isEditingTitle.value = true
  // Focus the input after it's rendered
  setTimeout(() => {
    titleInputRef.value?.focus()
  }, 10)
}

const finishEditingTitle = () => {
  isEditingTitle.value = false
  // Ensure form name is not empty
  if (!currentFormName.value || !currentFormName.value.trim()) {
    currentFormName.value = selectedDocument.value?.name || 'Untitled Form'
  }
}

const selectPatient = (patient) => {
  selectedPatient.value = patient
  showPatientSelector.value = false
  
  // Update patient data with selected patient's information
  updatePatientDataFromSelection(patient)
  
  console.log('Selected patient for document:', patient.name)
}

const clearPatientSelection = () => {
  selectedPatient.value = null
  // Clear patient-specific data
  clearPatientData()
  console.log('Cleared patient selection')
}

const updatePatientDataFromSelection = (patient) => {
  // Only update basic patient info, don't overwrite document-specific data
  patientData.date = new Date().toISOString().split('T')[0]
  patientData.patientId = patient.id
  patientData.hasPatientSelected = true
  
  // Only update fields that don't already have values (to preserve user input)
  if (!patientData.name || patientData.name === '') patientData.name = patient.name || ''
  if (!patientData.age || patientData.age === '') patientData.age = patient.age || ''
  if (!patientData.gender || patientData.gender === '') patientData.gender = patient.gender || ''
  if (!patientData.phone || patientData.phone === '') patientData.phone = patient.phone || ''
  if (!patientData.email || patientData.email === '') patientData.email = patient.email || ''
  if (!patientData.address || patientData.address === '') patientData.address = patient.address || ''
  if (!patientData.bloodType || patientData.bloodType === '') patientData.bloodType = patient.bloodType || ''
  if (!patientData.insuranceNumber || patientData.insuranceNumber === '') patientData.insuranceNumber = patient.insuranceNumber || ''
  if (!patientData.medicalHistory || patientData.medicalHistory === '') patientData.medicalHistory = patient.medicalHistory || ''
  if (!patientData.allergies || patientData.allergies === '') patientData.allergies = patient.allergies || ''
  if (!patientData.currentMedications || patientData.currentMedications === '') patientData.currentMedications = patient.currentMedications || ''
  if (!patientData.emergencyContact || patientData.emergencyContact === '') patientData.emergencyContact = patient.emergencyContact || ''
  
  // For New Patient Form - always update these fields (they get locked)
  patientData.patientName = patient.name || ''
  patientData.dateOfBirth = patient.dateOfBirth || ''
}

const clearPatientData = () => {
  // Clear patient-specific fields but keep document-specific fields
  Object.assign(patientData, {
    date: new Date().toISOString().split('T')[0], // Keep today's date
    name: '',
    age: '',
    gender: '',
    phone: '',
    email: '',
    address: '',
    bloodType: '',
    insuranceNumber: '',
    medicalHistory: '',
    allergies: '',
    currentMedications: '',
    emergencyContact: '',
    patientId: null
  })
}

const getPatientInitials = (name) => {
  if (!name) return '??'
  const names = name.trim().split(' ')
  if (names.length >= 2) {
    return (names[0][0] + names[names.length - 1][0]).toUpperCase()
  }
  return names[0][0].toUpperCase()
}

const navigateToPatients = () => {
  // This would navigate to the patients section
  // For now, we'll just show an alert
  alert('Please go to the Patients tab to create a new patient.')
}

const getTemplateCardClass = (template) => {
  const classMap = {
    'medical-report': 'template-medical',
    'consultation-form': 'template-consultation',
    'prescription-form': 'template-prescription',
    'new-patient-form': 'template-new-patient'
  }
  return classMap[template.id] || 'template-default'
}

const getTemplateIconClass = (template) => {
  const classMap = {
    'medical-report': 'icon-medical',
    'consultation-form': 'icon-consultation',
    'prescription-form': 'icon-prescription',
    'new-patient-form': 'icon-new-patient'
  }
  return classMap[template.id] || 'icon-default'
}

const handleFieldUpdate = (fieldName, value) => {
  console.log(`Updating field: ${fieldName} with value:`, value)
  if (patientData.hasOwnProperty(fieldName)) {
    patientData[fieldName] = value
    console.log(`Updated patientData.${fieldName}:`, patientData[fieldName])
  } else {
    console.warn(`Field ${fieldName} not found in patientData`)
  }
}

const saveDocument = () => {
  if (!hasFormData.value) {
    toastService.warning(
      'No Data to Save',
      'Please fill in some data before saving the document.'
    )
    return
  }
  
  if (!selectedPatient.value) {
    toastService.warning(
      'No Patient Selected',
      'Please select a patient before saving the document.'
    )
    return
  }
  
  // Check if we're editing an existing document
  let editingDocumentId = localStorage.getItem('editingDocumentId')
  
  // Only check for duplicates for New Patient Form (it should be unique per patient)
  if (selectedDocument.value.id === 'new-patient-form' && !editingDocumentId) {
    const allDocuments = JSON.parse(localStorage.getItem('medicalDocuments') || '[]')
    const existingForm = allDocuments.find(doc => 
      doc.documentId === 'new-patient-form' && 
      doc.patientId === selectedPatient.value.id
    )
    
    if (existingForm) {
      const confirmed = confirm(
        'Warning: This patient already has a New Patient Form. Saving will replace the existing form. Do you want to continue?'
      )
      if (!confirmed) {
        return
      }
      // If user confirms, we'll update the existing form
      localStorage.setItem('editingDocumentId', existingForm.id.toString())
      editingDocumentId = existingForm.id.toString()
    }
  }
  
  // Get saved documents
  const savedDocuments = JSON.parse(localStorage.getItem('medicalDocuments') || '[]')
  console.log('Current saved documents before save:', savedDocuments)
  
  let documentRecord
  if (editingDocumentId) {
    console.log('Updating existing document with ID:', editingDocumentId)
    // Update existing document - preserve original ID format
    const originalDoc = savedDocuments.find(doc => doc.id == editingDocumentId || doc.id === editingDocumentId)
    
    documentRecord = {
      id: originalDoc?.id || editingDocumentId,
      patientId: selectedPatient.value.id,
      patientName: selectedPatient.value.name,
      documentType: selectedDocument.value.name,
      documentId: selectedDocument.value.id,
      customName: currentFormName.value || selectedDocument.value.name, // Store custom name
      date: patientData.date,
      data: { ...patientData },
      createdAt: originalDoc?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    
    // Find and update the document - handle both string and number IDs
    const documentIndex = savedDocuments.findIndex(doc => doc.id == editingDocumentId || doc.id === editingDocumentId)
    if (documentIndex !== -1) {
      savedDocuments[documentIndex] = documentRecord
      console.log('Document updated at index:', documentIndex)
    } else {
      console.warn('Document not found for update, adding as new')
      savedDocuments.push(documentRecord)
    }
    
    // Clear editing flags
    localStorage.removeItem('editingDocumentId')
    localStorage.removeItem('editingDocumentData')
    localStorage.removeItem('editingDocumentType')
    
    toastService.success(
      'Document Updated Successfully!',
      `"${currentFormName.value || selectedDocument.value.name}" has been updated for ${selectedPatient.value.name}.`
    )
    
    // Show confirmation alert
    setTimeout(() => {
      alert('✓ Document has been successfully updated!')
    }, 100)
  } else {
    console.log('Creating new document')
    // Create new document record - use a more unique ID
    documentRecord = {
      id: `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`,
      patientId: selectedPatient.value.id,
      patientName: selectedPatient.value.name,
      documentType: selectedDocument.value.name,
      documentId: selectedDocument.value.id,
      customName: currentFormName.value || selectedDocument.value.name, // Store custom name
      date: patientData.date,
      data: { ...patientData },
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    
    savedDocuments.push(documentRecord)
    console.log('Added new document to array')
    
    toastService.success(
      'Document Saved Successfully!',
      `"${currentFormName.value || selectedDocument.value.name}" has been saved for ${selectedPatient.value.name}.`
    )
    
    // Show confirmation alert
    setTimeout(() => {
      alert('✓ Document has been successfully saved!')
    }, 100)
  }
  
  // Save to localStorage
  localStorage.setItem('medicalDocuments', JSON.stringify(savedDocuments))
  console.log('Total documents saved:', savedDocuments.length)
  console.log('Document saved:', documentRecord)
  
  // Verify what's in localStorage
  const verifyDocuments = JSON.parse(localStorage.getItem('medicalDocuments') || '[]')
  console.log('Verification - Documents in localStorage:', verifyDocuments)
}

// Lifecycle
onMounted(async () => {
  console.log('Document management mounted')
  // Ensure date is set to today
  patientData.date = new Date().toISOString().split('T')[0]
  
  // Load patients when component mounts
  try {
    await patientVM.loadPatients()
    console.log('Patients loaded for document management')
  } catch (error) {
    console.error('Error loading patients:', error)
  }
  
  // Check if we're editing an existing document - use setTimeout to ensure DOM is ready
  setTimeout(() => {
    const editingDocumentId = localStorage.getItem('editingDocumentId')
    if (editingDocumentId) {
      console.log('Found document to edit:', editingDocumentId)
      const editingDocumentData = JSON.parse(localStorage.getItem('editingDocumentData') || '{}')
      const editingDocumentType = localStorage.getItem('editingDocumentType')
      
      console.log('Editing data:', editingDocumentData)
      console.log('Document type:', editingDocumentType)
      
      // Map document types to template IDs
      const typeToTemplateId = {
        'New Patient Form': 'new-patient-form',
        'Medical Report': 'medical-report',
        'Consultation Form': 'consultation-form',
        'Prescription Form': 'prescription-form'
      }
      
      // Find the document template
      const templateId = typeToTemplateId[editingDocumentType]
      const template = documentTemplates.value.find(t => t.id === templateId)
      
      console.log('Looking for template with ID:', templateId)
      console.log('Available templates:', documentTemplates.value.map(t => t.id))
      
      if (template) {
        // Select the document template
        selectedDocument.value = template
        console.log('Selected template:', template.name)
        
        // Small delay to ensure the template is selected
        setTimeout(() => {
          // Load the patient for this document
          if (editingDocumentData.patientId) {
            const patient = patientVM.patients.value.find(p => p.id === editingDocumentData.patientId)
            console.log('Looking for patient with ID:', editingDocumentData.patientId)
            console.log('Available patients:', patientVM.patients.value.map(p => ({ id: p.id, name: p.name })))
            
            if (patient) {
              selectedPatient.value = patient
              console.log('Selected patient:', patient.name)
              showPatientSelector.value = false
            }
          }
          
          // Populate form data with the saved document data
          // This should happen after patient selection to preserve form data
          Object.keys(editingDocumentData).forEach(key => {
            if (editingDocumentData[key] !== null && editingDocumentData[key] !== undefined && editingDocumentData[key] !== '') {
              patientData[key] = editingDocumentData[key]
            }
          })
          
          // Load custom form name if it exists, otherwise use template name
          const savedDocumentsList = JSON.parse(localStorage.getItem('medicalDocuments') || '[]')
          const editingDoc = savedDocumentsList.find(doc => doc.id == editingDocumentId || doc.id === editingDocumentId)
          if (editingDoc && editingDoc.customName) {
            currentFormName.value = editingDoc.customName
          } else {
            currentFormName.value = template.name
          }
          
          console.log('Form data populated:', patientData)
          
          // Don't clear editing flags here - they will be cleared when saving
          // The flags are only for loading the data, not for tracking state
        }, 100)
      } else {
        console.error('Template not found for document type:', editingDocumentType)
      }
    }
  }, 100)
})
</script>

<style scoped>
.document-management {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.page-header h2 {
  color: white;
  margin: 0 0 1rem 0;
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.page-header p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.2rem;
  margin: 0;
  text-shadow: 0 1px 5px rgba(0,0,0,0.3);
}

.document-selection {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;
}

.document-selection h3 {
  color: white;
  margin: 0 0 2rem 0;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.template-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.template-card {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 15px;
  border: 2px solid rgba(255, 255, 255, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: center;
}

.template-card:hover {
  background: rgba(255, 255, 255, 0.1);
  border-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.2);
}

.template-card--selected {
  background: rgba(102, 126, 234, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
  transform: translateY(-5px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.template-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto 1rem;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

/* Template icon color variations */
.icon-medical {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.icon-consultation {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
  box-shadow: 0 4px 15px rgba(78, 205, 196, 0.4);
}

.icon-prescription {
  background: linear-gradient(135deg, #a8e6cf 0%, #7fcdcd 100%);
  box-shadow: 0 4px 15px rgba(168, 230, 207, 0.4);
}

.icon-new-patient {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
  box-shadow: 0 4px 15px rgba(255, 154, 158, 0.4);
}

.icon-default {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.template-card:hover .template-icon {
  transform: scale(1.1);
}

.template-card:hover .icon-medical {
  box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6);
}

.template-card:hover .icon-consultation {
  box-shadow: 0 6px 20px rgba(78, 205, 196, 0.6);
}

.template-card:hover .icon-prescription {
  box-shadow: 0 6px 20px rgba(168, 230, 207, 0.6);
}

.template-card:hover .icon-new-patient {
  box-shadow: 0 6px 20px rgba(255, 154, 158, 0.6);
}

.template-card:hover .icon-default {
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

.template-icon svg {
  width: 30px;
  height: 30px;
  color: white;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.template-card h4 {
  color: white;
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
  font-weight: 600;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.template-card p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.document-form-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.form-title-section {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.form-header h3 {
  color: white;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.form-name-input {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  padding: 0.5rem 1rem;
  color: white;
  font-size: 1.8rem;
  font-weight: 700;
  min-width: 200px;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.form-name-input:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.edit-title-btn {
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  padding: 0.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
}

.edit-title-btn svg {
  width: 18px;
  height: 18px;
}

.edit-title-btn:hover {
  background: rgba(255, 255, 255, 0.2);
  border-color: rgba(102, 126, 234, 0.4);
  transform: scale(1.05);
}

.form-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.export-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.export-button svg {
  width: 1rem;
  height: 1rem;
  filter: drop-shadow(0 1px 2px rgba(0,0,0,0.2));
}

.export-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.save-button {
  background: linear-gradient(135deg, #28a745, #20c997);
  color: white;
}

.save-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(40, 167, 69, 0.3);
}

.debug-button {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
}

.debug-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.3);
}

.pdf-button {
  background: linear-gradient(135deg, #dc3545, #c82333);
  color: white;
}

.pdf-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(220, 53, 69, 0.3);
}

.word-button {
  background: linear-gradient(135deg, #007bff, #0056b3);
  color: white;
}

.word-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 123, 255, 0.3);
}

.document-form {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 2rem;
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.empty-state {
  text-align: center;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 3rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-top: 2rem;
}

.empty-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.empty-icon-svg {
  width: 40px;
  height: 40px;
  color: white;
  filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));
}

.empty-state h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.empty-state p {
  color: rgba(255, 255, 255, 0.8);
  margin: 0;
  font-size: 1.1rem;
  font-weight: 500;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

/* Patient Selection Styles */
.patient-selection-section {
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  padding: 1.5rem;
  border-radius: 15px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
}

.patient-selection-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.patient-selection-header h4 {
  color: white;
  margin: 0;
  font-size: 1.2rem;
  font-weight: 600;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
}

.patient-selector-toggle {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.patient-selector-toggle:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
}

.patient-selector-toggle.active {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.toggle-icon {
  font-size: 0.8rem;
  transition: transform 0.3s ease;
}

.patient-selector {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-radius: 10px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  max-height: 300px;
  overflow: hidden;
}

.patient-search {
  padding: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.patient-search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 8px;
  color: white;
  font-size: 0.9rem;
  backdrop-filter: blur(10px);
}

.patient-search-input::placeholder {
  color: rgba(255, 255, 255, 0.6);
}

.patient-search-input:focus {
  outline: none;
  border-color: rgba(102, 126, 234, 0.5);
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.patient-list {
  max-height: 200px;
  overflow-y: auto;
}

.patient-option {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}

.patient-option:hover {
  background: rgba(255, 255, 255, 0.1);
}

.patient-option.selected {
  background: rgba(102, 126, 234, 0.2);
  border-left: 3px solid #667eea;
}

.patient-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 0.9rem;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.patient-info {
  flex: 1;
}

.patient-name {
  color: white;
  font-weight: 600;
  font-size: 1rem;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.patient-details {
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.85rem;
  margin-top: 0.25rem;
}

.selected-patient-info {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(102, 126, 234, 0.1);
  border-radius: 10px;
  border: 1px solid rgba(102, 126, 234, 0.2);
  margin-top: 1rem;
}

.selected-patient-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.selected-patient-details {
  flex: 1;
}

.selected-patient-name {
  color: white;
  font-weight: 600;
  font-size: 1.1rem;
  text-shadow: 0 1px 3px rgba(0,0,0,0.3);
}

.selected-patient-meta {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
  margin-top: 0.25rem;
}

.clear-patient-btn {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: rgba(255, 107, 107, 0.2);
  border: 1px solid rgba(255, 107, 107, 0.3);
  color: #ff6b6b;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: all 0.3s ease;
}

.clear-patient-btn:hover {
  background: rgba(255, 107, 107, 0.3);
  transform: scale(1.1);
}

.no-patients {
  padding: 2rem;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

.no-patients a {
  color: #667eea;
  text-decoration: none;
  font-weight: 600;
}

.no-patients a:hover {
  text-decoration: underline;
}

/* Responsive design */
@media (max-width: 768px) {
  .document-management {
    padding: 1rem;
  }
  
  .form-header {
    flex-direction: column;
    align-items: stretch;
  }
  
  .form-actions {
    justify-content: center;
  }
  
  .template-grid {
    grid-template-columns: 1fr;
  }
  
  .export-button {
    flex: 1;
    justify-content: center;
  }
  
  .patient-selection-header {
    flex-direction: column;
    align-items: stretch;
    gap: 1rem;
  }
  
  .patient-selector-toggle {
    justify-content: center;
  }
}
</style>
