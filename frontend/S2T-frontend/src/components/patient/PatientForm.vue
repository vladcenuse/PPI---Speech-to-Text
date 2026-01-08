<template>
  <div class="patient-form">
    <form @submit.prevent="handleSubmit" class="form">
      <div class="form-section">
        <h3 class="section-title">Informații Personale</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="name" class="form-label">Nume Complet *</label>
            <input
              id="name"
              v-model="formData.name"
              type="text"
              class="form-input"
              :class="{ 'form-input--error': errors.name, 'form-input--disabled': isViewMode }"
              :disabled="isViewMode"
              placeholder="Introduceți numele complet"
              required
            />
            <span v-if="errors.name" class="form-error">{{ errors.name }}</span>
          </div>
          
          <div class="form-group">
            <label for="age" class="form-label">Vârstă *</label>
            <input
              id="age"
              :value="computedAge"
              type="number"
              class="form-input"
              :class="{ 'form-input--error': errors.age, 'form-input--disabled': true }"
              disabled
              placeholder="Calculat automat"
              readonly
            />
            <span v-if="errors.age" class="form-error">{{ errors.age }}</span>
          </div>
        </div>
        
        <div class="form-row">
          <div class="form-group">
            <label for="gender" class="form-label">Gen *</label>
            <select
              id="gender"
              v-model="formData.gender"
              class="form-select"
              :class="{ 'form-select--error': errors.gender, 'form-select--disabled': isViewMode }"
              :disabled="isViewMode"
              required
            >
              <option value="">Selectați genul</option>
              <option value="Male">Masculin</option>
              <option value="Female">Feminin</option>
            </select>
            <span v-if="errors.gender" class="form-error">{{ errors.gender }}</span>
          </div>
          
          <div class="form-group">
            <label for="dateOfBirth" class="form-label">Data Nașterii *</label>
            <input
              id="dateOfBirth"
              v-model="formData.dateOfBirth"
              type="date"
              class="form-input"
              :class="{ 'form-input--error': errors.dateOfBirth, 'form-input--disabled': isViewMode }"
              :disabled="isViewMode"
              required
            />
            <span v-if="errors.dateOfBirth" class="form-error">{{ errors.dateOfBirth }}</span>
          </div>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Informații de Contact</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="phone" class="form-label">Telefon</label>
            <input
              id="phone"
              v-model="formData.phone"
              type="tel"
              class="form-input"
              :class="{ 'form-input--disabled': isViewMode }"
              :disabled="isViewMode"
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
              :class="{ 'form-input--disabled': isViewMode }"
              :disabled="isViewMode"
              placeholder="example@email.com"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="address" class="form-label">Adresă</label>
          <textarea
            id="address"
            v-model="formData.address"
            class="form-textarea"
            :class="{ 'form-textarea--disabled': isViewMode }"
            :disabled="isViewMode"
            placeholder="Introduceți adresa completă"
            rows="3"
          ></textarea>
        </div>
      </div>

      <div class="form-section">
        <h3 class="section-title">Informații Medicale</h3>
        
        <div class="form-row">
          <div class="form-group">
            <label for="bloodType" class="form-label">Grupa Sanguină</label>
            <select
              id="bloodType"
              v-model="formData.bloodType"
              class="form-select"
              :class="{ 'form-select--disabled': isViewMode }"
              :disabled="isViewMode"
            >
              <option value="">Selectați grupa sanguină</option>
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
            <label for="insuranceNumber" class="form-label">Număr Asigurare</label>
            <input
              id="insuranceNumber"
              v-model="formData.insuranceNumber"
              type="text"
              class="form-input"
              :class="{ 'form-input--disabled': isViewMode }"
              :disabled="isViewMode"
              placeholder="Număr asigurare"
            />
          </div>
        </div>
        
        <div class="form-group">
          <label for="medicalHistory" class="form-label">Istoric Medical</label>
          <textarea
            id="medicalHistory"
            v-model="formData.medicalHistory"
            class="form-textarea"
            :class="{ 'form-textarea--disabled': isViewMode }"
            :disabled="isViewMode"
            placeholder="Descrieți istoricul medical al pacientului"
            rows="4"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="allergies" class="form-label">Alergii</label>
          <textarea
            id="allergies"
            v-model="formData.allergies"
            class="form-textarea"
            :class="{ 'form-textarea--disabled': isViewMode }"
            :disabled="isViewMode"
            placeholder="Lista alergiilor cunoscute"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="currentMedications" class="form-label">Medicamente Curente</label>
          <textarea
            id="currentMedications"
            v-model="formData.currentMedications"
            class="form-textarea"
            :class="{ 'form-textarea--disabled': isViewMode }"
            :disabled="isViewMode"
            placeholder="Lista medicamentelor curente"
            rows="3"
          ></textarea>
        </div>
        
        <div class="form-group">
          <label for="emergencyContact" class="form-label">Contact Urgență</label>
          <textarea
            id="emergencyContact"
            v-model="formData.emergencyContact"
            class="form-textarea"
            :class="{ 'form-textarea--disabled': isViewMode }"
            :disabled="isViewMode"
            placeholder="Informații contact urgență"
            rows="2"
          ></textarea>
        </div>
      </div>

      <div v-if="errors.general" class="form-error-general">
        <span class="error-icon">✕</span>
        <span>{{ errors.general }}</span>
      </div>

      <div class="form-actions">
        <Button
          type="button"
          variant="outline"
          @click="handleCancel"
          :text="isViewMode ? 'Închide' : 'Anulează'"
        />
        <Button
          v-if="!isViewMode"
          type="submit"
          variant="primary"
          :loading="isSubmitting"
          text="Salvează"
        />
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, watch, computed } from 'vue'
import Button from '@/components/common/Button.vue'
import { PatientForm as PatientFormModel } from '@/models/PatientForm.js'

const props = defineProps({
  patient: {
    type: Object,
    default: null
  },
  isViewMode: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['save', 'cancel'])

const isSubmitting = ref(false)
const errors = reactive({})

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

const calculateAge = (dateOfBirth) => {
  if (!dateOfBirth || !dateOfBirth.trim()) {
    return null
  }
  const birthDate = new Date(dateOfBirth)
  if (isNaN(birthDate.getTime())) {
    return null
  }
  const today = new Date()
  let age = today.getFullYear() - birthDate.getFullYear()
  const monthDiff = today.getMonth() - birthDate.getMonth()
  if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
    age--
  }
  return age >= 0 ? age : null
}

const computedAge = computed(() => {
  return calculateAge(formData.dateOfBirth)
})

watch(() => formData.dateOfBirth, (newDateOfBirth) => {
  if (newDateOfBirth && newDateOfBirth.trim()) {
    const calculatedAge = calculateAge(newDateOfBirth)
    if (calculatedAge !== null) {
      formData.age = calculatedAge
    }
  } else {
    formData.age = null
  }
})

const initializeFormData = () => {
  try {
    const patientData = props.patient?.value || props.patient
    console.log('Initializing form with patient data:', patientData)
    
    if (patientData && typeof patientData === 'object') {
      console.log('Patient data found, populating form')
      Object.assign(formData, {
        name: (typeof patientData.name === 'string') ? patientData.name.trim() : '',
        age: (typeof patientData.age === 'number' && !isNaN(patientData.age)) ? patientData.age : null,
        gender: (typeof patientData.gender === 'string') ? patientData.gender.trim() : '',
        dateOfBirth: (typeof patientData.dateOfBirth === 'string') ? patientData.dateOfBirth.trim() : '',
        phone: (typeof patientData.phone === 'string') ? patientData.phone.trim() : '',
        email: (typeof patientData.email === 'string') ? patientData.email.trim() : '',
        address: (typeof patientData.address === 'string') ? patientData.address.trim() : '',
        bloodType: (typeof patientData.bloodType === 'string') ? patientData.bloodType.trim() : '',
        insuranceNumber: (typeof patientData.insuranceNumber === 'string') ? patientData.insuranceNumber.trim() : '',
        medicalHistory: (typeof patientData.medicalHistory === 'string') ? patientData.medicalHistory.trim() : '',
        allergies: (typeof patientData.allergies === 'string') ? patientData.allergies.trim() : '',
        currentMedications: (typeof patientData.currentMedications === 'string') ? patientData.currentMedications.trim() : '',
        emergencyContact: (typeof patientData.emergencyContact === 'string') ? patientData.emergencyContact.trim() : ''
      })
      if (formData.dateOfBirth && formData.dateOfBirth.trim()) {
        const calculatedAge = calculateAge(formData.dateOfBirth)
        if (calculatedAge !== null) {
          formData.age = calculatedAge
        }
      }
      console.log('Form data after assignment:', formData)
    } else {
      console.log('No patient data, initializing form for new patient')
      Object.assign(formData, {
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
    }
  } catch (error) {
    console.error('Error initializing form data:', error)
    Object.assign(formData, {
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
  }
}

initializeFormData()

watch(() => props.patient, (newPatient) => {
  console.log('Patient prop changed:', newPatient)
  console.log('Patient prop type:', typeof newPatient)
  console.log('Patient prop value:', newPatient?.value || newPatient)
  initializeFormData()
}, { immediate: true, deep: false })

watch(() => props.isViewMode, (newViewMode) => {
  console.log('View mode changed:', newViewMode)
  initializeFormData()
}, { immediate: false })

const validateForm = () => {
  Object.keys(errors).forEach(key => delete errors[key])
  
  let isValid = true

  try {
    if (!formData.name || typeof formData.name !== 'string' || !formData.name.trim()) {
      errors.name = 'Numele este obligatoriu'
      isValid = false
    } else if (formData.name.trim().length < 2) {
      errors.name = 'Numele trebuie să aibă cel puțin 2 caractere'
      isValid = false
    }

    if (!formData.dateOfBirth || !formData.dateOfBirth.trim()) {
      errors.dateOfBirth = 'Data nașterii este obligatorie'
      isValid = false
    } else {
      const birthDate = new Date(formData.dateOfBirth)
      const today = new Date()
      if (isNaN(birthDate.getTime())) {
        errors.dateOfBirth = 'Data nașterii nu este validă'
        isValid = false
      } else if (birthDate > today) {
        errors.dateOfBirth = 'Data nașterii nu poate fi în viitor'
        isValid = false
      } else if (birthDate.getFullYear() < 1900) {
        errors.dateOfBirth = 'Data nașterii nu poate fi înainte de 1900'
        isValid = false
      } else {
        const calculatedAge = calculateAge(formData.dateOfBirth)
        if (calculatedAge === null || calculatedAge < 0 || calculatedAge > 150) {
          errors.age = 'Vârstă invalidă calculată din data nașterii'
          isValid = false
        } else {
          formData.age = calculatedAge
        }
      }
    }

    if (!formData.gender || typeof formData.gender !== 'string' || !formData.gender.trim()) {
      errors.gender = 'Genul este obligatoriu'
      isValid = false
    }

    if (formData.email && formData.email.trim()) {
      if (!isValidEmail(formData.email.trim())) {
        errors.email = 'Adresa de email nu este validă'
        isValid = false
      }
    }

    if (formData.phone && formData.phone.trim()) {
      if (!isValidPhone(formData.phone.trim())) {
        errors.phone = 'Numărul de telefon nu este valid'
        isValid = false
      }
    }


    if (!isValid) {
      errors.general = 'Vă rugăm să completați toate câmpurile obligatorii și să corectați erorile afișate.'
    }

  } catch (validationError) {
    console.error('Validation error:', validationError)
    errors.general = 'A apărut o eroare în timpul validării. Vă rugăm să verificați datele introduse.'
    isValid = false
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
  console.log('handleSubmit called')
  console.log('Form data:', formData)
  console.log('Props patient:', props.patient)
  
  if (isSubmitting.value) {
    console.log('Already submitting, ignoring duplicate submission')
    return
  }
  
  if (!validateForm()) {
    console.log('Form validation failed')
    return
  }

  console.log('Form validation passed')
  isSubmitting.value = true

  try {
    const currentPatient = props.patient?.value || props.patient
    console.log('Current patient data for ID extraction:', currentPatient)
    console.log('Patient ID:', currentPatient?.id)
    console.log('Patient createdAt:', currentPatient?.createdAt)
    
    const sanitizedFormData = {
      name: (formData.name || '').trim(),
      age: Number(formData.age) || null,
      gender: (formData.gender || '').trim(),
      dateOfBirth: (formData.dateOfBirth || '').trim(),
      phone: (formData.phone || '').trim(),
      email: (formData.email || '').trim(),
      address: (formData.address || '').trim(),
      bloodType: (formData.bloodType || '').trim(),
      insuranceNumber: (formData.insuranceNumber || '').trim(),
      medicalHistory: (formData.medicalHistory || '').trim(),
      allergies: (formData.allergies || '').trim(),
      currentMedications: (formData.currentMedications || '').trim(),
      emergencyContact: (formData.emergencyContact || '').trim()
    }
    
    const patientData = new PatientFormModel({
      ...sanitizedFormData,
      id: currentPatient?.id || null,
      createdAt: currentPatient?.createdAt || new Date().toISOString(),
      updatedAt: new Date().toISOString()
    })
    
    console.log('Created patient model:', patientData)
    console.log('Emitting save event with:', patientData.toJSON())
    
    emit('save', patientData.toJSON())
  } catch (error) {
    console.error('Error saving patient:', error)
    if (error.message) {
      errors.general = `Eroare: ${error.message}`
    } else {
      errors.general = 'A apărut o eroare la salvarea pacientului. Vă rugăm să verificați datele introduse și să încercați din nou.'
    }
  } finally {
    isSubmitting.value = false
  }
}

const handleCancel = () => {
  emit('cancel')
}
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

.form-input--disabled,
.form-select--disabled,
.form-textarea--disabled {
  background-color: #f5f5f5;
  color: #666;
  cursor: not-allowed;
  opacity: 0.7;
}

.form-input--disabled:focus,
.form-select--disabled:focus,
.form-textarea--disabled:focus {
  border-color: #ddd;
  box-shadow: none;
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

