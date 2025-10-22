<template>
  <div class="consultation-form">
    <div class="document-header">
      <h2>Consultation Form</h2>
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
      <!-- Symptoms -->
      <div class="form-section">
        <h3>Presenting Symptoms</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'symptoms' }"
          @click="handleFieldClick('symptoms')"
        >
          <label>Current symptoms and complaints:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.symptoms"
              placeholder="Click to record or type the presenting symptoms..."
              rows="4"
              @input="updateField('symptoms', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'symptoms'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Vital Signs -->
      <div class="form-section">
        <h3>Vital Signs</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'vitalSigns' }"
          @click="handleFieldClick('vitalSigns')"
        >
          <label>Blood pressure, temperature, pulse, etc.:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.vitalSigns"
              placeholder="Click to record or type vital signs..."
              rows="3"
              @input="updateField('vitalSigns', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'vitalSigns'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Assessment -->
      <div class="form-section">
        <h3>Clinical Assessment</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'assessment' }"
          @click="handleFieldClick('assessment')"
        >
          <label>Clinical findings and assessment:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.assessment"
              placeholder="Click to record or type clinical assessment..."
              rows="4"
              @input="updateField('assessment', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'assessment'" class="recording-indicator">
              <div class="recording-dot"></div>
              <span>Recording...</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Treatment Plan -->
      <div class="form-section">
        <h3>Treatment Plan</h3>
        <div 
          class="field-container"
          :class="{ 'field-container--recording': isRecording && currentField === 'plan' }"
          @click="handleFieldClick('plan')"
        >
          <label>Recommended treatment and follow-up:</label>
          <div class="field-input">
            <textarea 
              v-model="localData.plan"
              placeholder="Click to record or type treatment plan..."
              rows="4"
              @input="updateField('plan', $event.target.value)"
            ></textarea>
            <div v-if="isRecording && currentField === 'plan'" class="recording-indicator">
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
  symptoms: props.patientData.symptoms || '',
  vitalSigns: props.patientData.vitalSigns || '',
  assessment: props.patientData.assessment || '',
  plan: props.patientData.plan || ''
})

// Watch for changes in patientData
watch(() => props.patientData, (newData) => {
  Object.assign(localData, {
    symptoms: newData.symptoms || '',
    vitalSigns: newData.vitalSigns || '',
    assessment: newData.assessment || '',
    plan: newData.plan || ''
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
.consultation-form {
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
