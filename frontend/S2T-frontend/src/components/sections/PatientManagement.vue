<template>
  <div class="patient-management">
    <div class="page-header">
      <h2>Patient Management</h2>
      <div class="header-actions">
        <Button 
          variant="outline" 
          @click="refreshPatients"
          :loading="isLoading"
          icon="🔄"
          text="Refresh"
        />
        <Button 
          variant="primary" 
          @click="openCreatePatientModal"
          icon="➕"
          text="New Patient"
        />
      </div>
    </div>

    <!-- Search and Filters -->
    <div class="search-section">
      <div class="search-bar">
        <input
          v-model="localSearchQuery"
          type="text"
          placeholder="Search patients..."
          class="search-input"
        />
        <span class="search-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" class="search-svg">
            <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
          </svg>
        </span>
      </div>
      
      <div class="filters">
        <select v-model="localFilters.gender" class="filter-select">
          <option value="">All genders</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
        </select>
        
        <select v-model="localFilters.hasRecordings" class="filter-select">
          <option value="">All patients</option>
          <option value="true">With recordings</option>
          <option value="false">Without recordings</option>
        </select>
      </div>
    </div>

    <!-- Patient Stats -->
    <div class="patient-stats">
      <div class="stat-card">
        <div class="stat-number">{{ patientsCount }}</div>
        <div class="stat-label">Total Patients</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ filteredPatientsCount }}</div>
        <div class="stat-label">Filtered Results</div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <Spinner size="large" text="Loading patients..." />
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-container">
      <div class="error-message">
        <span class="error-icon">
          <svg viewBox="0 0 24 24" fill="currentColor" class="error-svg">
            <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
          </svg>
        </span>
        <span>{{ error }}</span>
      </div>
      <Button variant="secondary" @click="refreshPatients" text="Try Again" />
    </div>

    <!-- Patient List -->
    <div v-else-if="patients.length > 0" class="patient-list">
      <div v-for="patient in patients" :key="patient.id" class="patient-card">
        <div class="patient-avatar">
          <div class="avatar-circle" :class="getPatientAvatarClass(patient)">
            {{ getPatientInitials(patient.name) }}
          </div>
        </div>
        <div class="patient-info">
          <h3>{{ patient.name }}</h3>
          <p class="patient-details">
            {{ patient.age }} years old • {{ patient.gender }}
          </p>
          <p class="patient-contact">
            📞 {{ patient.phone || 'No phone number' }}
          </p>
          <p class="patient-observations">
            📝 {{ patient.observations?.length || 0 }} observations
          </p>
          <p class="patient-updated">
            Last modified: {{ formatDate(patient.updatedAt) }}
          </p>
        </div>
        
        <div class="patient-actions">
          <Button 
            variant="secondary" 
            size="small"
            @click="editPatient(patient)"
            text="Edit"
          />
          <Button 
            variant="outline" 
            size="small"
            @click="viewPatient(patient)"
            text="View"
          />
          <Button 
            variant="error" 
            size="small"
            @click="deletePatient(patient)"
            text="Delete"
          />
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty-state">
      <div class="empty-icon">
        <svg viewBox="0 0 24 24" fill="currentColor" class="empty-icon-svg">
          <path d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"/>
          <path d="M8 21v-2a2 2 0 012-2h4a2 2 0 012 2v2"/>
        </svg>
      </div>
      <h3>No patients found</h3>
      <p>Create the first patient to get started.</p>
      <Button variant="primary" @click="openCreatePatientModal" text="Create First Patient" />
    </div>

    <!-- Create/Edit Patient Modal -->
        <Modal
          :is-open="showCreateModal"
          :title="isViewMode ? 'View Patient' : (patientVM.currentPatient ? 'Edit Patient' : 'New Patient')"
          size="large"
          @close="closeCreatePatientModal"
        >
      <PatientForm
        :patient="debugPatientData"
        :is-view-mode="isViewMode"
        @save="handleSavePatient"
        @cancel="closeCreatePatientModal"
      />
    </Modal>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Delete Patient"
      :message="deleteMessage"
      :details="deleteDetails"
      confirm-text="Delete"
      cancel-text="Cancel"
      :loading="isLoading"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
      @close="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch, computed } from 'vue'
import Button from '@/components/common/Button.vue'
import Modal from '@/components/common/Modal.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import Spinner from '@/components/common/Spinner.vue'
import PatientForm from '@/components/patient/PatientForm.vue'
import { usePatientViewModel } from '@/viewmodels/PatientViewModel.js'

// ViewModels
const patientVM = usePatientViewModel()

// Local state
const showCreateModal = ref(false)
const showDeleteModal = ref(false)
const patientToDelete = ref(null)
const isViewMode = ref(false)
const localSearchQuery = ref('')
const localFilters = reactive({
  gender: '',
  hasRecordings: ''
})

// Computed properties from ViewModels
const {
  patients,
  isLoading,
  error,
  patientsCount,
  filteredPatientsCount,
  loadPatients,
  createPatient,
  updatePatient,
  deletePatient: deletePatientVM,
  setCurrentPatient,
  setSearchQuery,
  setFilters,
  clearFilters
} = patientVM

// Computed properties for delete modal
const deleteMessage = computed(() => {
  if (patientToDelete.value) {
    return `Are you sure you want to delete patient "${patientToDelete.value.name}"?`
  }
  return ''
})

const deleteDetails = computed(() => {
  if (patientToDelete.value) {
    return `This action will permanently delete all data for patient ${patientToDelete.value.name}, including observations and associated recordings.`
  }
  return ''
})

// Debug computed property for patient data
const debugPatientData = computed(() => {
  console.log('Debug: currentPatient computed value:', patientVM.currentPatient)
  console.log('Debug: currentPatient type:', typeof patientVM.currentPatient)
  console.log('Debug: currentPatient value:', patientVM.currentPatient?.value || patientVM.currentPatient)
  return patientVM.currentPatient
})

// Methods
const refreshPatients = async () => {
  await loadPatients()
}

const openCreatePatientModal = () => {
  setCurrentPatient(null)
  isViewMode.value = false
  showCreateModal.value = true
}

const closeCreatePatientModal = () => {
  setCurrentPatient(null)
  isViewMode.value = false
  showCreateModal.value = false
}

const handleCreatePatient = async (patientData) => {
  const result = await createPatient(patientData)
  if (result.success) {
    closeCreatePatientModal()
  }
}

const handleUpdatePatient = async (patientData) => {
  const currentPatient = patientVM.currentPatient?.value || patientVM.currentPatient
  console.log('handleUpdatePatient - currentPatient:', currentPatient)
  console.log('handleUpdatePatient - patientData:', patientData)
  
  if (currentPatient && currentPatient.id) {
    console.log('Updating patient with ID:', currentPatient.id)
    const result = await updatePatient(currentPatient.id, patientData)
    if (result.success) {
      closeCreatePatientModal()
    }
  } else {
    console.error('Cannot update patient: no current patient or ID found')
  }
}

const handleSavePatient = async (patientData) => {
  console.log('handleSavePatient called with:', patientData)
  console.log('Current patient:', patientVM.currentPatient)
  
  const currentPatient = patientVM.currentPatient?.value || patientVM.currentPatient
  console.log('Current patient value:', currentPatient)
  console.log('Patient ID from currentPatient:', currentPatient?.id)
  console.log('Patient ID from patientData:', patientData.id)
  
  if (currentPatient && currentPatient.id) {
    console.log('Updating existing patient with ID:', currentPatient.id)
    await handleUpdatePatient(patientData)
  } else {
    console.log('Creating new patient...')
    await handleCreatePatient(patientData)
  }
}

const editPatient = (patient) => {
  console.log('editPatient called with:', patient)
  console.log('Patient data:', JSON.stringify(patient, null, 2))
  setCurrentPatient(patient)
  console.log('After setCurrentPatient, currentPatient:', patientVM.currentPatient)
  isViewMode.value = false
  showCreateModal.value = true
}

const viewPatient = (patient) => {
  console.log('viewPatient called with:', patient)
  setCurrentPatient(patient)
  isViewMode.value = true
  showCreateModal.value = true
}

const deletePatient = (patient) => {
  patientToDelete.value = patient
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  if (patientToDelete.value) {
    const result = await deletePatientVM(patientToDelete.value.id)
    if (result.success) {
      showDeleteModal.value = false
      patientToDelete.value = null
    }
  }
}

const cancelDelete = () => {
  showDeleteModal.value = false
  patientToDelete.value = null
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('ro-RO', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getPatientInitials = (name) => {
  if (!name) return '??'
  const names = name.trim().split(' ')
  if (names.length >= 2) {
    return (names[0][0] + names[names.length - 1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

const getPatientAvatarClass = (patient) => {
  const colors = ['avatar-blue', 'avatar-green', 'avatar-purple', 'avatar-orange', 'avatar-teal', 'avatar-pink']
  const index = patient.id % colors.length
  return colors[index]
}

// Watch for search and filter changes
watch(localSearchQuery, (newQuery) => {
  setSearchQuery(newQuery)
})

watch(localFilters, (newFilters) => {
  setFilters(newFilters)
}, { deep: true })

// Lifecycle
onMounted(async () => {
  await loadPatients()
})
</script>

<style scoped>
.patient-management {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
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
  margin: 0;
  font-size: 2.5rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.header-actions {
  display: flex;
  gap: 1rem;
}

.search-section {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.search-bar {
  position: relative;
  margin-bottom: 1rem;
}

.search-input {
  width: 100%;
  padding: 1rem 1rem 1rem 3rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  font-size: 1rem;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.search-input::placeholder {
  color: rgba(255, 255, 255, 0.7);
}

.search-input:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: rgba(255, 255, 255, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-svg {
  width: 1rem;
  height: 1rem;
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.filter-select {
  padding: 0.75rem 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 0.875rem;
  min-width: 150px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.filter-select:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 0.5);
  background: rgba(255, 255, 255, 0.15);
}

.filter-select option {
  background: #667eea;
  color: white;
}

.patient-stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  text-align: center;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 
    0 15px 40px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.3);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
  margin-bottom: 0.5rem;
}

.stat-label {
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  font-weight: 500;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 200px;
}

.error-container {
  text-align: center;
  background: white;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  color: #dc3545;
  font-weight: 500;
  margin-bottom: 1rem;
}

.error-icon {
  display: flex;
  align-items: center;
  justify-content: center;
}

.error-svg {
  width: 1.25rem;
  height: 1.25rem;
  color: #dc3545;
}

.patient-list {
  display: grid;
  gap: 1rem;
}

.patient-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.patient-card::before {
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

.patient-card:hover::before {
  opacity: 1;
}

.patient-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.patient-avatar {
  margin-right: 1.5rem;
  display: flex;
  align-items: center;
}

.avatar-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.2rem;
  color: white;
  text-shadow: 0 2px 4px rgba(0,0,0,0.3);
  box-shadow: 0 4px 15px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
}

.patient-card:hover .avatar-circle {
  transform: scale(1.1);
  box-shadow: 0 6px 20px rgba(0,0,0,0.3);
}

/* Avatar color variations */
.avatar-blue {
  background: linear-gradient(135deg, #4ecdc4 0%, #44a08d 100%);
}

.avatar-green {
  background: linear-gradient(135deg, #a8e6cf 0%, #7fcdcd 100%);
}

.avatar-purple {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.avatar-orange {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
}

.avatar-teal {
  background: linear-gradient(135deg, #26d0ce 0%, #1a2980 100%);
}

.avatar-pink {
  background: linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%);
}

.patient-info {
  flex: 1;
}

.patient-info h3 {
  margin: 0 0 0.5rem 0;
  color: white;
  font-size: 1.5rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.patient-details {
  margin: 0.25rem 0;
  color: rgba(255, 255, 255, 0.8);
  font-weight: 500;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.patient-contact,
.patient-observations,
.patient-updated {
  margin: 0.25rem 0;
  color: rgba(255, 255, 255, 0.7);
  font-size: 0.9rem;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

.patient-actions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  min-width: 120px;
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
  transition: all 0.3s ease;
}

.empty-icon:hover {
  transform: scale(1.05);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
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
  margin-bottom: 2rem;
  font-size: 1.1rem;
  font-weight: 500;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

/* Responsive design */
@media (max-width: 768px) {
  .patient-management {
    padding: 1rem;
  }
  
  .page-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }
  
  .header-actions {
    justify-content: center;
  }
  
  .filters {
    flex-direction: column;
  }
  
  .filter-select {
    min-width: auto;
  }
  
  .patient-card {
    flex-direction: column;
    gap: 1rem;
  }
  
  .patient-actions {
    flex-direction: row;
    justify-content: space-between;
  }
}
</style>
