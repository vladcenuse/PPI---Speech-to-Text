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
        <h3>{{ selectedDocument.name }}</h3>
        <div class="form-actions">
          <button
            @click="debugData"
            class="export-button debug-button"
          >
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2M12,4A8,8 0 0,1 20,12A8,8 0 0,1 12,20A8,8 0 0,1 4,12A8,8 0 0,1 12,4M11,16.5L18,9.5L16.5,8L11,13.5L7.5,10L6,11.5L11,16.5Z"/>
            </svg>
            <span>Debug Data</span>
          </button>
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

// State
const selectedDocument = ref(null)
const patientData = reactive({
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

// Methods
const selectDocument = (template) => {
  selectedDocument.value = template
  console.log('Selected document:', template.name)
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

const debugData = () => {
  console.log('=== DEBUG DATA ===')
  console.log('Selected Document:', selectedDocument.value)
  console.log('Patient Data:', patientData)
  console.log('Has Form Data:', hasFormData.value)
  console.log('Non-empty fields:', Object.entries(patientData).filter(([key, value]) => value && value.toString().trim() !== ''))
  console.log('==================')
  
  const nonEmptyFields = Object.entries(patientData).filter(([key, value]) => value && value.toString().trim() !== '')
  const message = `Current data:\n\nNon-empty fields: ${nonEmptyFields.length}\n\nFields with data:\n${nonEmptyFields.map(([key, value]) => `${key}: "${value}"`).join('\n')}`
  alert(message)
}

const generatePDFContent = () => {
  const documentName = selectedDocument.value.name
  const currentDate = new Date().toLocaleDateString()
  
  console.log('Generating PDF content for:', documentName)
  console.log('Current patientData:', patientData)
  
  let content = `
    <!DOCTYPE html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>${documentName}</title>
      <style>
        @page {
          size: A4;
          margin: 2cm;
        }
        @media print {
          body { -webkit-print-color-adjust: exact; }
          .no-print { display: none; }
        }
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 800px;
          margin: 0 auto;
        }
        .header {
          text-align: center;
          border-bottom: 2px solid #667eea;
          padding-bottom: 20px;
          margin-bottom: 30px;
        }
        .header h1 {
          color: #667eea;
          margin: 0;
          font-size: 28px;
        }
        .header .date {
          color: #666;
          font-size: 14px;
          margin-top: 10px;
        }
        .section {
          margin-bottom: 25px;
        }
        .section h2 {
          color: #667eea;
          border-bottom: 1px solid #eee;
          padding-bottom: 5px;
          margin-bottom: 15px;
          font-size: 18px;
        }
        .field {
          margin-bottom: 10px;
          display: flex;
        }
        .field-label {
          font-weight: bold;
          min-width: 150px;
          color: #555;
        }
        .field-value {
          flex: 1;
          padding-left: 10px;
        }
        .footer {
          margin-top: 40px;
          text-align: center;
          font-size: 12px;
          color: #666;
          border-top: 1px solid #eee;
          padding-top: 20px;
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>${documentName}</h1>
        <div class="date">Generated on: ${currentDate}</div>
      </div>
  `
  
  let fieldCount = 0
  Object.entries(patientData).forEach(([key, value]) => {
    console.log(`Processing field: ${key} = "${value}"`)
    if (value && value.toString().trim() !== '') {
      const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
      content += `
        <div class="field">
          <div class="field-label">${label}:</div>
          <div class="field-value">${value}</div>
        </div>
      `
      fieldCount++
    }
  })
  
  console.log(`Added ${fieldCount} fields to PDF content`)
  
  content += `
      <div class="footer">
        <p>Document generated by Speech-to-Text Medical System</p>
        <p>Generated on: ${currentDate}</p>
      </div>
    </body>
    </html>
  `
  
  return content
}

const generateWordContent = () => {
  const documentName = selectedDocument.value.name
  const currentDate = new Date().toLocaleDateString()
  
  console.log('Generating Word content for:', documentName)
  console.log('Current patientData:', patientData)
  
  let content = `
    <!DOCTYPE html>
    <html xmlns:o="urn:schemas-microsoft-com:office:office"
          xmlns:w="urn:schemas-microsoft-com:office:word"
          xmlns="http://www.w3.org/TR/REC-html40">
    <head>
      <meta charset="utf-8">
      <meta name="ProgId" content="Word.Document">
      <meta name="Generator" content="Microsoft Word 15">
      <meta name="Originator" content="Microsoft Word 15">
      <title>${documentName}</title>
      <style>
        body {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
        }
        .header {
          text-align: center;
          border-bottom: 2px solid #667eea;
          padding-bottom: 20px;
          margin-bottom: 30px;
        }
        .header h1 {
          color: #667eea;
          margin: 0;
          font-size: 28px;
        }
        .header .date {
          color: #666;
          font-size: 14px;
          margin-top: 10px;
        }
        .section {
          margin-bottom: 25px;
        }
        .section h2 {
          color: #667eea;
          border-bottom: 1px solid #eee;
          padding-bottom: 5px;
          margin-bottom: 15px;
          font-size: 18px;
        }
        .field {
          margin-bottom: 10px;
          display: flex;
        }
        .field-label {
          font-weight: bold;
          min-width: 150px;
          color: #555;
        }
        .field-value {
          flex: 1;
          padding-left: 10px;
        }
        .footer {
          margin-top: 40px;
          text-align: center;
          font-size: 12px;
          color: #666;
          border-top: 1px solid #eee;
          padding-top: 20px;
        }
      </style>
    </head>
    <body>
      <div class="header">
        <h1>${documentName}</h1>
        <div class="date">Generated on: ${currentDate}</div>
      </div>
  `
  
  let fieldCount = 0
  Object.entries(patientData).forEach(([key, value]) => {
    console.log(`Processing field: ${key} = "${value}"`)
    if (value && value.toString().trim() !== '') {
      const label = key.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
      content += `
        <div class="field">
          <div class="field-label">${label}:</div>
          <div class="field-value">${value}</div>
        </div>
      `
      fieldCount++
    }
  })
  
  console.log(`Added ${fieldCount} fields to Word content`)
  
  content += `
      <div class="footer">
        <p>Document generated by Speech-to-Text Medical System</p>
        <p>Generated on: ${currentDate}</p>
      </div>
    </body>
    </html>
  `
  
  return content
}

const exportToPDF = () => {
  if (!hasFormData.value) {
    alert('Please fill in some data before exporting to PDF.')
    return
  }
  
  const htmlContent = generatePDFContent()
  
  // Open new window with print-optimized content
  const printWindow = window.open('', '_blank', 'width=800,height=600')
  printWindow.document.write(htmlContent)
  
  // Add print-specific styles
  printWindow.document.write(`
    <style>
      @media print {
        body { margin: 0; }
        .no-print { display: none; }
      }
    </style>
  `)
  
  printWindow.document.close()
  
  // Focus and trigger print dialog
  setTimeout(() => {
    printWindow.focus()
    printWindow.print()
    
    // Close window after printing (optional)
    setTimeout(() => {
      printWindow.close()
    }, 1000)
  }, 500)
  
  console.log('PDF export initiated')
}

const exportToWord = () => {
  if (!hasFormData.value) {
    alert('Please fill in some data before exporting to Word.')
    return
  }
  
  const htmlContent = generateWordContent()
  
  // Create blob with Word-compatible HTML
  const blob = new Blob([htmlContent], { type: 'text/html;charset=utf-8' })
  
  // Create download link
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.download = `${selectedDocument.value.name.replace(/\s+/g, '_')}_${new Date().toISOString().split('T')[0]}.html`
  
  // Trigger download
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  
  // Clean up
  URL.revokeObjectURL(link.href)
  
  console.log('Word export completed')
}

// Lifecycle
onMounted(() => {
  console.log('Document management mounted')
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

.form-header h3 {
  color: white;
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
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
}
</style>
