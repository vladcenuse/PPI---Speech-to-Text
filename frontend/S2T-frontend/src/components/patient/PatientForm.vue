<template>
  <div class="patient-form">
    <form @submit.prevent="handleSubmit" class="form">
      <!-- Personal Information -->
      <div class="form-section">
        <h3 class="section-title">Personal Information</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="name" class="form-label">Full Name *</label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.name }"
              placeholder="Enter full name"
              required
            />
            <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
          </div>
          
          <div class="form-group">
            <label for="age" class="form-label">Age *</label>
            <input
              id="age"
              v-model.number="formData.age"
              type="number"
              class="form-input"
              :class="{ 'form-input--error': errors.age }"
              placeholder="Age"
              min="0"
              max="150"
              required
            />
            <span v-if="errors.age" class="form-error">{{ errors.age }}</span>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="gender" class="form-label">Gender *</label>
            <select
              id="gender"
              v-model="formData.gender"
              class="form-select"
              :class="{ 'form-select--error': errors.gender }"
              required
            >
              <option value="">Select gender</option>
              <option value="Male">Male</option>
              <option value="Female">Female</option>
            </select>
            <span v-if="errors.gender" class="form-error">{{ errors.gender }}</span>
          </div>
          
          <div class="form-group">
            <label for="dateOfBirth" class="form-label">Date of Birth</label>
            <input
              id="dateOfBirth"
              v-model="formData.dateOfBirth"
              type="date"
              class="form-input"
            />
          </div>
        </div>
      </div>

      <!-- Contact Information -->
      <div class="form-section">
        <h3 class="section-title">Contact Information</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="phone" class="form-label">Phone</label>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              class="form-input"
              placeholder="0712345678"
            />
          </div>
          
          <div class="form-group">
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="formData.email"
              type="email"
              class="form-input"
              placeholder="example@email.com"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="address" class="form-label">Address</label>
          <textarea
            id="address"
            v-model="formData.address"
            class="form-textarea"
            placeholder="Enter complete address"
            rows="3"
          ></textarea>
        </div>
      </div>

      <!-- Medical Information -->
      <div class="form-section">
        <h3 class="section-title">Medical Information</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="bloodType" class="form-label">Blood Type</label>
            <select
              id="bloodType"
              v-model="formData.bloodType"
              class="form-select"
            >
              <option value="">Select blood type</option>
              <option value="A+">A+</option>
              <option value="A-">A-</option>
              <option value="B+">B+</option>
              <option value="B-">B-</option>
              <option value="AB+">AB+</option>
              <option value="AB-">AB-</option>
              <option value="O+">O+</option>
              <option value="O-">O-</option>
            </select>
          </div>
          
          <div class="form-group">
            <label for="insuranceNumber" class="form-label">Insurance Number</label>
            <input
              id="insuranceNumber"
              v-model="formData.insuranceNumber"
              type="text"
              class="form-input"
              placeholder="Insurance number"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="medicalHistory" class="form-label">Medical History</label>
          <textarea
            id="medicalHistory"
            v-model="formData.medicalHistory"
            class="form-textarea"
            placeholder="Describe the patient's medical history"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="allergies" class="form-label">Allergies</label>
          <textarea
            id="allergies"
            v-model="formData.allergies"
            class="form-textarea"
            placeholder="List of known allergies"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="currentMedications" class="form-label">Current Medications</label>
          <textarea
            id="currentMedications"
            v-model="formData.currentMedications"
            class="form-textarea"
            placeholder="List of current medications"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="emergencyContact" class="form-label">Emergency Contact</label>
          <textarea
            id="emergencyContact"
            v-model="formData.emergencyContact"
            class="form-textarea"
            placeholder="Emergency contact information"
            rows="2"
          ></textarea>
        </div>
      </div>

      <!-- General Error Display -->
      <div v-if="errors.general" class="form-error-general">
        <span class="error-icon">✕</span>
        <span>{{ errors.general }}</span>
      </div>

      <!-- Form Actions -->
      <div class="form-actions">
        <Button
          type="button"
          variant="outline"
          @click="handleCancel"
          text="Cancel"
        />
        <Button
          type="submit"
          variant="primary"
          :loading="isSubmitting"
          text="Save"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import Button from '@/components/common/Button.vue'
import { PatientForm as PatientFormModel } from '@/models/PatientForm.js'

// Props
const props = defineProps({
  patient: {
    type: Object,
    default: null
  }
})

// Emits
const emit = defineEmits(['save', 'cancel'])

// State
const isSubmitting = ref(false)
const errors = reactive({})

// Form data
const formData = reactive({
  name: '',
  age: null,
  gender: '',
  dateOfBirth: '',
  phone: '',
  email: '',
  address: '',
  bloodType: '',
  insuranceNumber: '',
  medicalHistory: '',
  allergies: '',
  currentMedications: '',
  emergencyContact: ''
})

// Initialize form data
if (props.patient) {
  Object.assign(formData, {
    name: props.patient.name || '',
    age: props.patient.age || null,
    gender: props.patient.gender || '',
    dateOfBirth: props.patient.dateOfBirth || '',
    phone: props.patient.phone || '',
    email: props.patient.email || '',
    address: props.patient.address || '',
    bloodType: props.patient.bloodType || '',
    insuranceNumber: props.patient.insuranceNumber || '',
    medicalHistory: props.patient.medicalHistory || '',
    allergies: props.patient.allergies || '',
    currentMedications: props.patient.currentMedications || '',
    emergencyContact: props.patient.emergencyContact || ''
  })
}

// Methods
const validateForm = () => {
  // Clear previous errors
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true

  // Validate required fields
  if (!formData.name.trim()) {
    errors.name = 'Name is required'
    isValid = false
  }

  if (!formData.age || formData.age < 0 || formData.age > 150) {
    errors.age = 'Age must be between 0 and 150 years'
    isValid = false
  }

  if (!formData.gender) {
    errors.gender = 'Gender is required'
    isValid = false
  }

  // Validate email if provided
  if (formData.email && !isValidEmail(formData.email)) {
    errors.email = 'Email address is not valid'
    isValid = false
  }

  // Validate phone if provided
  if (formData.phone && !isValidPhone(formData.phone)) {
    errors.phone = 'Phone number is not valid'
    isValid = false
  }

  // Show general error if validation fails
  if (!isValid) {
    errors.general = 'Please fill in all required fields and correct the displayed errors.'
  }

  return isValid
}

const isValidEmail = (email) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return emailRegex.test(email)
}

const isValidPhone = (phone) => {
  const phoneRegex = /^[0-9\s\+\-\(\)]{10,}$/
  return phoneRegex.test(phone)
}

const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true

  try {
    // Create patient model with form data
    const patientData = new PatientFormModel({
      ...formData,
      // Preserve existing ID if editing
      id: props.patient?.id || null,
      // Preserve existing timestamps if editing
      createdAt: props.patient?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    })
    
    // Emit save event with the patient data
    emit('save', patientData.toJSON())
  } catch (error) {
    console.error('Error saving patient:', error)
    // Show error to user
    errors.general = 'An error occurred while saving the patient. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
}

// Watch for form changes to clear errors
watch(formData, () => {
  // Clear field errors when user starts typing
  Object.keys(errors).forEach(key => {
    if (key !== 'general' && formData[key]) {
      delete errors[key]
    }
  })
  
  // Clear general error when user makes any change
  if (errors.general) {
    delete errors.general
  }
}, { deep: true })
</script>

<style scoped>
.patient-form {
  max-width: 800px;
  margin: 0 auto;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  background: #f8f9fa;
  padding: 1.5rem;
  border-radius: 12px;
  border: 1px solid #e9ecef;
}

.section-title {
  margin: 0 0 1.5rem 0;
  color: #2c3e50;
  font-size: 1.25rem;
  font-weight: 600;
  border-bottom: 2px solid #667eea;
  padding-bottom: 0.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-label {
  font-weight: 500;
  color: #374151;
  font-size: 0.875rem;
}

.form-input,
.form-select,
.form-textarea {
  padding: 0.75rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s, box-shadow 0.3s;
  background: white;
}

.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-input--error,
.form-select--error {
  border-color: #dc3545;
}

.form-input--error:focus,
.form-select--error:focus {
  border-color: #dc3545;
  box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
}

.form-textarea {
  resize: vertical;
  min-height: 80px;
}

.form-error {
  color: #dc3545;
  font-size: 0.875rem;
  font-weight: 500;
}

.form-error-general {
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 6px;
  padding: 0.75rem;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #dc2626;
  font-size: 0.875rem;
}

.form-error-general .error-icon {
  font-size: 1rem;
  flex-shrink: 0;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 1rem;
  padding-top: 1rem;
  border-top: 1px solid #e5e7eb;
}

/* Responsive design */
@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>

