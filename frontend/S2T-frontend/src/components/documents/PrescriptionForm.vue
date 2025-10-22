<template>
  <div class="prescription-form">
    <div class="document-header">
      <h2>Prescription Form</h2>
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
      <!-- Medications -->
      <div class="form-section">
        <h3>Prescribed Medications</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'medications' }"
          @click="handleFieldClick('medications')"
        >
          <label>Medication names and types:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.medications"
              placeholder="Click to record or type prescribed medications..."
              rows="4"
              @input="updateField('medications', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'medications'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Dosage -->
      <div class="form-section">
        <h3>Dosage Instructions</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'dosage' }"
          @click="handleFieldClick('dosage')"
        >
          <label>Dosage amounts and frequency:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.dosage"
              placeholder="Click to record or type dosage instructions..."
              rows="3"
              @input="updateField('dosage', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'dosage'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Instructions -->
      <div class="form-section">
        <h3>Special Instructions</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'instructions' }"
          @click="handleFieldClick('instructions')"
        >
          <label>Special instructions and warnings:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.instructions"
              placeholder="Click to record or type special instructions..."
              rows="4"
              @input="updateField('instructions', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'instructions'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Follow-up -->
      <div class="form-section">
        <h3>Follow-up Instructions</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'followUp' }"
          @click="handleFieldClick('followUp')"
        >
          <label>Follow-up appointments and monitoring:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.followUp"
              placeholder="Click to record or type follow-up instructions..."
              rows="3"
              @input="updateField('followUp', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'followUp'" class="recording-indicator">
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
  medications: props.patientData.medications || '',
  dosage: props.patientData.dosage || '',
  instructions: props.patientData.instructions || '',
  followUp: props.patientData.followUp || ''
})

// Watch for changes in patientData
watch(() => props.patientData, (newData) => {
  Object.assign(localData, {
    medications: newData.medications || '',
    dosage: newData.dosage || '',
    instructions: newData.instructions || '',
    followUp: newData.followUp || ''
  })
}, { deep: true })

const handleFieldClick = (fieldName) => {
  emit('field-click', fieldName)
}

const updateField = (fieldName, value) => {
  localData[fieldName] = value
  emit('field-update', fieldName, value)
}
</script>

<style scoped>
.prescription-form {
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
