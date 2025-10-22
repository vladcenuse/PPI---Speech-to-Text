<template>
  <div class="medical-report">
    <div class="document-header">
      <h2>Medical Report</h2>
      <div class="report-info">
        <div class="info-item">
          <label>Date:</label>
          <span>{{ patientData.date }}</span>
        </div>
        <div class="info-item">
          <label>Patient:</label>
          <span>{{ patientData.patientName || 'Select Patient' }}</span>
        </div>
      </div>
    </div>

    <div class="form-sections">
      <!-- Chief Complaint -->
      <div class="form-section">
        <h3>Chief Complaint</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'chiefComplaint' }"
          @click="handleFieldClick('chiefComplaint')"
        >
          <label>Primary reason for visit:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.chiefComplaint"
              placeholder="Click to record or type the chief complaint..."
              rows="3"
              @input="updateField('chiefComplaint', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'chiefComplaint'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- History of Present Illness -->
      <div class="form-section">
        <h3>History of Present Illness</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'historyOfPresentIllness' }"
          @click="handleFieldClick('historyOfPresentIllness')"
        >
          <label>Detailed history and symptoms:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.historyOfPresentIllness"
              placeholder="Click to record or type the history of present illness..."
              rows="4"
              @input="updateField('historyOfPresentIllness', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'historyOfPresentIllness'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Physical Examination -->
      <div class="form-section">
        <h3>Physical Examination</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'physicalExamination' }"
          @click="handleFieldClick('physicalExamination')"
        >
          <label>Examination findings:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.physicalExamination"
              placeholder="Click to record or type physical examination findings..."
              rows="4"
              @input="updateField('physicalExamination', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'physicalExamination'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Diagnosis -->
      <div class="form-section">
        <h3>Diagnosis</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'diagnosis' }"
          @click="handleFieldClick('diagnosis')"
        >
          <label>Medical diagnosis:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.diagnosis"
              placeholder="Click to record or type the diagnosis..."
              rows="3"
              @input="updateField('diagnosis', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'diagnosis'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Treatment -->
      <div class="form-section">
        <h3>Treatment Plan</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'treatment' }"
          @click="handleFieldClick('treatment')"
        >
          <label>Recommended treatment:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.treatment"
              placeholder="Click to record or type the treatment plan..."
              rows="4"
              @input="updateField('treatment', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'treatment'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Recommendations -->
      <div class="form-section">
        <h3>Recommendations</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'recommendations' }"
          @click="handleFieldClick('recommendations')"
        >
          <label>Follow-up recommendations:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.recommendations"
              placeholder="Click to record or type recommendations..."
              rows="3"
              @input="updateField('recommendations', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'recommendations'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  patientData: {
    type: Object,
    required: true
  },
  isRecording: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['field-click', 'field-update'])

// Local reactive data
const localData = reactive({
  chiefComplaint: props.patientData.chiefComplaint || '',
  historyOfPresentIllness: props.patientData.historyOfPresentIllness || '',
  physicalExamination: props.patientData.physicalExamination || '',
  diagnosis: props.patientData.diagnosis || '',
  treatment: props.patientData.treatment || '',
  recommendations: props.patientData.recommendations || ''
})

// Watch for changes in patientData
watch(() => props.patientData, (newData) => {
  Object.assign(localData, {
    chiefComplaint: newData.chiefComplaint || '',
    historyOfPresentIllness: newData.historyOfPresentIllness || '',
    physicalExamination: newData.physicalExamination || '',
    diagnosis: newData.diagnosis || '',
    treatment: newData.treatment || '',
    recommendations: newData.recommendations || ''
  })
}, { deep: true })

const handleFieldClick = (fieldName) => {
  emit('field-click', fieldName)
}

const updateField = (fieldName, value) => {
  console.log(`MedicalReport: Updating field ${fieldName} with value:`, value)
  localData[fieldName] = value
  emit('field-update', fieldName, value)
  console.log(`MedicalReport: Emitted field-update event for ${fieldName}`)
}
</script>

<style scoped>
.medical-report {
  max-width: 800px;
  margin: 0 auto;
}

.document-header {
  border-bottom: 2px solid #e9ecef;
  padding-bottom: 1.5rem;
  margin-bottom: 2rem;
}

.document-header h2 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 2rem;
}

.report-info {
  display: flex;
  gap: 2rem;
  flex-wrap: wrap;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.info-item label {
  font-weight: 600;
  color: #495057;
}

.info-item span {
  color: #6c757d;
  padding: 0.25rem 0.75rem;
  background: #f8f9fa;
  border-radius: 4px;
}

.form-sections {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.form-section {
  border: 1px solid #e9ecef;
  border-radius: 8px;
  padding: 1.5rem;
  background: #fafbfc;
}

.form-section h3 {
  color: #2c3e50;
  margin-bottom: 1rem;
  font-size: 1.3rem;
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
}

.field-container {
  position: relative;
  cursor: pointer;
  transition: all 0.3s ease;
  border-radius: 6px;
  padding: 0.5rem;
}

.field-container:hover {
  background: #f8f9fa;
}

.field-container--recording {
  background: #fff3cd;
  border: 2px solid #ffc107;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(255, 193, 7, 0); }
  100% { box-shadow: 0 0 0 0 rgba(255, 193, 7, 0); }
}

.field-container label {
  display: block;
  font-weight: 600;
  color: #495057;
  margin-bottom: 0.5rem;
}

.field-input {
  position: relative;
}

.field-input textarea {
  width: 100%;
  border: 1px solid #ced4da;
  border-radius: 6px;
  padding: 0.75rem;
  font-size: 0.95rem;
  line-height: 1.5;
  resize: vertical;
  transition: all 0.3s ease;
}

.field-input textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.recording-indicator {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: #dc3545;
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 4px;
  font-size: 0.8rem;
  font-weight: 600;
}

.recording-dot {
  width: 8px;
  height: 8px;
  background: white;
  border-radius: 50%;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}

@media (max-width: 768px) {
  .report-info {
    flex-direction: column;
    gap: 1rem;
  }
  
  .form-section {
    padding: 1rem;
  }
}
</style>
