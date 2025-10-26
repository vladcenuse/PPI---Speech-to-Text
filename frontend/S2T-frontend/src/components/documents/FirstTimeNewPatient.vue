<template>
  <div class="document-template first-time-patient">
    <h3>First Time New Patient Assessment</h3>
    <div class="form-section">
      <!-- Patient Information -->
      <div class="form-group">
        <label for="patientName">Patient Full Name</label>
        <div class="input-with-button">
          <input 
            type="text" 
            id="patientName" 
            :value="formData.patientName"
            @input="updateField('patientName', $event.target.value)"
            @click="emitFieldClick('patientName')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'patientName', 'field-locked': isFieldLocked }"
            :disabled="isFieldLocked"
            placeholder="Enter patient's full name"
          />
          <button 
            v-if="!isFieldLocked"
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'patientName' }"
            @click="toggleRecording('patientName')"
          >
            {{ isRecording && currentRecordingField === 'patientName' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="dateOfBirth">Date of Birth *</label>
        <div class="input-with-button">
          <input 
            type="date" 
            id="dateOfBirth" 
            :value="formData.dateOfBirth"
            @input="updateField('dateOfBirth', $event.target.value)"
            @click="emitFieldClick('dateOfBirth')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'dateOfBirth', 'field-locked': isFieldLocked }"
            :disabled="isFieldLocked"
            required
          />
          <button 
            v-if="!isFieldLocked"
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'dateOfBirth' }"
            @click="toggleRecording('dateOfBirth')"
          >
            {{ isRecording && currentRecordingField === 'dateOfBirth' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="gender">Gender *</label>
        <div class="input-with-button">
          <select 
            id="gender" 
            :value="formData.gender"
            @change="updateField('gender', $event.target.value)"
            @click="emitFieldClick('gender')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'gender', 'field-locked': isFieldLocked }"
            :disabled="isFieldLocked"
            required
          >
            <option value="">Select Gender</option>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
            <option value="Other">Other</option>
            <option value="Prefer not to say">Prefer not to say</option>
          </select>
          <button 
            v-if="!isFieldLocked"
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'gender' }"
            @click="toggleRecording('gender')"
          >
            {{ isRecording && currentRecordingField === 'gender' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="contactInfo">Contact Information</label>
        <div class="input-with-button">
          <textarea 
            id="contactInfo" 
            :value="formData.contactInfo"
            @input="updateField('contactInfo', $event.target.value)"
            @click="emitFieldClick('contactInfo')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'contactInfo' }"
            placeholder="Phone number, email address, emergency contact"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'contactInfo' }"
            @click="toggleRecording('contactInfo')"
          >
            {{ isRecording && currentRecordingField === 'contactInfo' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <!-- Medical History -->
      <div class="form-group">
        <label for="chiefComplaint">Chief Complaint</label>
        <div class="input-with-button">
          <textarea 
            id="chiefComplaint" 
            :value="formData.chiefComplaint"
            @input="updateField('chiefComplaint', $event.target.value)"
            @click="emitFieldClick('chiefComplaint')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'chiefComplaint' }"
            placeholder="Primary reason for visit"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'chiefComplaint' }"
            @click="toggleRecording('chiefComplaint')"
          >
            {{ isRecording && currentRecordingField === 'chiefComplaint' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="presentIllness">History of Present Illness</label>
        <div class="input-with-button">
          <textarea 
            id="presentIllness" 
            :value="formData.presentIllness"
            @input="updateField('presentIllness', $event.target.value)"
            @click="emitFieldClick('presentIllness')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'presentIllness' }"
            placeholder="Detailed description of current symptoms and their progression"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'presentIllness' }"
            @click="toggleRecording('presentIllness')"
          >
            {{ isRecording && currentRecordingField === 'presentIllness' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="pastMedicalHistory">Past Medical History</label>
        <div class="input-with-button">
          <textarea 
            id="pastMedicalHistory" 
            :value="formData.pastMedicalHistory"
            @input="updateField('pastMedicalHistory', $event.target.value)"
            @click="emitFieldClick('pastMedicalHistory')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'pastMedicalHistory' }"
            placeholder="Previous medical conditions, surgeries, hospitalizations"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'pastMedicalHistory' }"
            @click="toggleRecording('pastMedicalHistory')"
          >
            {{ isRecording && currentRecordingField === 'pastMedicalHistory' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="medications">Current Medications</label>
        <div class="input-with-button">
          <textarea 
            id="medications" 
            :value="formData.medications"
            @input="updateField('medications', $event.target.value)"
            @click="emitFieldClick('medications')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'medications' }"
            placeholder="List all current medications, dosages, and frequency"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'medications' }"
            @click="toggleRecording('medications')"
          >
            {{ isRecording && currentRecordingField === 'medications' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="allergies">Allergies</label>
        <div class="input-with-button">
          <textarea 
            id="allergies" 
            :value="formData.allergies"
            @input="updateField('allergies', $event.target.value)"
            @click="emitFieldClick('allergies')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'allergies' }"
            placeholder="Drug allergies, food allergies, environmental allergies"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'allergies' }"
            @click="toggleRecording('allergies')"
          >
            {{ isRecording && currentRecordingField === 'allergies' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="familyHistory">Family History</label>
        <div class="input-with-button">
          <textarea 
            id="familyHistory" 
            :value="formData.familyHistory"
            @input="updateField('familyHistory', $event.target.value)"
            @click="emitFieldClick('familyHistory')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'familyHistory' }"
            placeholder="Relevant family medical history"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'familyHistory' }"
            @click="toggleRecording('familyHistory')"
          >
            {{ isRecording && currentRecordingField === 'familyHistory' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="socialHistory">Social History</label>
        <div class="input-with-button">
          <textarea 
            id="socialHistory" 
            :value="formData.socialHistory"
            @input="updateField('socialHistory', $event.target.value)"
            @click="emitFieldClick('socialHistory')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'socialHistory' }"
            placeholder="Smoking, alcohol, occupation, lifestyle factors"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'socialHistory' }"
            @click="toggleRecording('socialHistory')"
          >
            {{ isRecording && currentRecordingField === 'socialHistory' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <!-- Physical Examination -->
      <div class="form-group">
        <label for="vitalSigns">Vital Signs</label>
        <div class="input-with-button">
          <textarea 
            id="vitalSigns" 
            :value="formData.vitalSigns"
            @input="updateField('vitalSigns', $event.target.value)"
            @click="emitFieldClick('vitalSigns')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'vitalSigns' }"
            placeholder="Blood pressure, heart rate, temperature, respiratory rate, oxygen saturation"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'vitalSigns' }"
            @click="toggleRecording('vitalSigns')"
          >
            {{ isRecording && currentRecordingField === 'vitalSigns' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="physicalExam">Physical Examination Findings</label>
        <div class="input-with-button">
          <textarea 
            id="physicalExam" 
            :value="formData.physicalExam"
            @input="updateField('physicalExam', $event.target.value)"
            @click="emitFieldClick('physicalExam')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'physicalExam' }"
            placeholder="General appearance, head/neck, cardiovascular, respiratory, abdominal, neurological findings"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'physicalExam' }"
            @click="toggleRecording('physicalExam')"
          >
            {{ isRecording && currentRecordingField === 'physicalExam' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <!-- Assessment and Plan -->
      <div class="form-group">
        <label for="assessment">Assessment</label>
        <div class="input-with-button">
          <textarea 
            id="assessment" 
            :value="formData.assessment"
            @input="updateField('assessment', $event.target.value)"
            @click="emitFieldClick('assessment')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'assessment' }"
            placeholder="Clinical impression and working diagnosis"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'assessment' }"
            @click="toggleRecording('assessment')"
          >
            {{ isRecording && currentRecordingField === 'assessment' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="plan">Treatment Plan</label>
        <div class="input-with-button">
          <textarea 
            id="plan" 
            :value="formData.plan"
            @input="updateField('plan', $event.target.value)"
            @click="emitFieldClick('plan')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'plan' }"
            placeholder="Diagnostic tests, medications, follow-up instructions"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'plan' }"
            @click="toggleRecording('plan')"
          >
            {{ isRecording && currentRecordingField === 'plan' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>

      <div class="form-group">
        <label for="followUp">Follow-up Instructions</label>
        <div class="input-with-button">
          <textarea 
            id="followUp" 
            :value="formData.followUp"
            @input="updateField('followUp', $event.target.value)"
            @click="emitFieldClick('followUp')"
            :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'followUp' }"
            placeholder="When to return, warning signs to watch for, lifestyle modifications"
          ></textarea>
          <button 
            type="button"
            class="record-button"
            :class="{ 'recording': isRecording && currentRecordingField === 'followUp' }"
            @click="toggleRecording('followUp')"
          >
            {{ isRecording && currentRecordingField === 'followUp' ? '⏹️' : '🎙️' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, inject, watch, ref, computed } from 'vue'

const props = defineProps({
  isMicrophoneActive: Boolean,
  patientData: {
    type: Object,
    default: () => ({})
  }
})

// Computed property to check if fields should be locked
const isFieldLocked = computed(() => {
  // Lock fields if:
  // 1. A patient is selected (hasPatientSelected is true), OR
  // 2. We're editing a saved document (check if we have an editingDocumentId flag)
  const hasSelectedPatient = props.patientData?.hasPatientSelected === true
  const isEditingSavedDocument = localStorage.getItem('editingDocumentId') !== null
  return hasSelectedPatient || isEditingSavedDocument
})

const emit = defineEmits(['field-click', 'field-update'])

// Recording state
const isRecording = ref(false)
const currentRecordingField = ref(null)
const recordingStarted = ref(false)

const formData = reactive({
  patientName: '',
  dateOfBirth: '',
  gender: '',
  contactInfo: '',
  chiefComplaint: '',
  presentIllness: '',
  pastMedicalHistory: '',
  medications: '',
  allergies: '',
  familyHistory: '',
  socialHistory: '',
  vitalSigns: '',
  physicalExam: '',
  assessment: '',
  plan: '',
  followUp: ''
})

const activeRecordingField = inject('activeRecordingField')

const emitFieldClick = (fieldName) => {
  emit('field-click', fieldName)
}

// Add MediaRecorder state
const mediaRecorder = ref(null)
const audioChunks = ref([])
const audioStream = ref(null)

// Toggle recording function
const toggleRecording = async (fieldName) => {
  if (isRecording.value && currentRecordingField.value === fieldName) {
    // Stop recording for this field
    await stopRecording(fieldName)
  } else if (!isRecording.value) {
    // Start recording for this field
    await startRecording(fieldName)
  }
}

const startRecording = async (fieldName) => {
  if (isRecording.value) {
    console.log('Already recording, please wait...')
    return
  }

  try {
    console.log(`Starting recording for field: ${fieldName}`)
    isRecording.value = true
    currentRecordingField.value = fieldName
    recordingStarted.value = true
    
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    console.log('Microphone access granted')
    
    // Store the stream
    audioStream.value = stream
    
    // Create MediaRecorder
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    mediaRecorder.value.onstop = async () => {
      await sendAudioToTranscriptionAPI(fieldName, stream)
    }
    
    // Start recording
    mediaRecorder.value.start()
    console.log('Recording started')
    
  } catch (error) {
    console.error('Failed to start recording:', error)
    isRecording.value = false
    currentRecordingField.value = null
    recordingStarted.value = false
    audioStream.value = null
    alert('Microphone access denied. Please allow microphone access to use speech-to-text.')
  }
}

const stopRecording = async (fieldName) => {
  if (!mediaRecorder.value || mediaRecorder.value.state === 'inactive') {
    return
  }
  
  console.log(`Stopping recording for field: ${fieldName}`)
  mediaRecorder.value.stop()
  
  // Stop all tracks if we have the stream
  if (audioStream.value) {
    audioStream.value.getTracks().forEach(track => track.stop())
    audioStream.value = null
  }
}

const sendAudioToTranscriptionAPI = async (fieldName, stream) => {
  try {
    // Stop all tracks to free microphone
    stream.getTracks().forEach(track => track.stop())
    
    // Create audio blob
    const audioBlob = new Blob(audioChunks.value, { type: 'audio/webm' })
    
    // Create form data
    const formData = new FormData()
    // Use a proper filename with extension
    const timestamp = Date.now()
    formData.append('audio_file', audioBlob, `recording_${timestamp}.webm`)
    
    console.log('Sending audio to transcription API...')
    
    // Send to backend
    const response = await fetch('http://127.0.0.1:8000/api/transcribe', {
      method: 'POST',
      body: formData
    })
    
    if (!response.ok) {
      const errorText = await response.text()
      console.error('Transcription API error:', response.status, errorText)
      throw new Error(`Transcription failed: ${response.statusText} - ${errorText}`)
    }
    
    const data = await response.json()
    console.log('Transcription result:', data.text)
    
    // Update the field with transcribed text
    updateField(fieldName, data.text)
    
  } catch (error) {
    console.error('Error during transcription:', error)
    const errorMsg = error.message || 'Failed to transcribe audio'
    alert(`Transcription error: ${errorMsg}`)
  } finally {
    isRecording.value = false
    currentRecordingField.value = null
    recordingStarted.value = false
    audioChunks.value = []
    audioStream.value = null
  }
}

const updateField = (fieldName, value) => {
  console.log(`FirstTimeNewPatient: Updating field ${fieldName} with value:`, value)
  formData[fieldName] = value
  emit('field-update', fieldName, value)
  console.log(`FirstTimeNewPatient: Emitted field-update event for ${fieldName}`)
}

// Watch for changes in patientData to sync with form
watch(() => props.patientData, (newData) => {
  console.log('FirstTimeNewPatient watch triggered with:', newData)
  
  // Always update these specific fields that come from patientData
  if (newData) {
    const newPatientName = newData.patientName || newData.name || ''
    const newDateOfBirth = newData.dateOfBirth || ''
    const newGender = newData.gender || ''
    
    // Only update if values have changed
    if (newPatientName && newPatientName !== formData.patientName) {
      formData.patientName = newPatientName
      console.log('Updated patientName to:', newPatientName)
    }
    if (newDateOfBirth && newDateOfBirth !== formData.dateOfBirth) {
      formData.dateOfBirth = newDateOfBirth
      console.log('Updated dateOfBirth to:', newDateOfBirth)
    }
    if (newGender && newGender !== formData.gender) {
      formData.gender = newGender
      console.log('Updated gender to:', newGender)
    }
    
    // Update other fields
    Object.assign(formData, {
      contactInfo: newData.contactInfo || '',
      chiefComplaint: newData.chiefComplaint || '',
      presentIllness: newData.presentIllness || '',
      pastMedicalHistory: newData.pastMedicalHistory || '',
      medications: newData.medications || '',
      allergies: newData.allergies || '',
      familyHistory: newData.familyHistory || '',
      socialHistory: newData.socialHistory || '',
      vitalSigns: newData.vitalSigns || '',
      physicalExam: newData.physicalExam || '',
      assessment: newData.assessment || '',
      plan: newData.plan || '',
      followUp: newData.followUp || ''
    })
  }
}, { deep: true, immediate: true })
</script>

<style scoped>
.document-template {
  padding: 1.5rem;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #fdfdfd;
}

.document-template h3 {
  color: #34495e;
  margin-bottom: 1.5rem;
  text-align: center;
  font-size: 1.8rem;
}

.form-section {
  display: grid;
  gap: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #34495e;
  font-weight: 600;
}

.input-with-button {
  display: flex;
  gap: 0.5rem;
  align-items: flex-start;
}

.input-with-button input[type="text"],
.input-with-button input[type="date"],
.input-with-button select,
.input-with-button textarea {
  flex: 1;
  padding: 0.8rem 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s ease-in-out;
  box-sizing: border-box;
}

.input-with-button textarea {
  min-height: 100px;
  resize: vertical;
}

.input-with-button select {
  cursor: pointer;
}

.record-button {
  padding: 0.8rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: all 0.3s ease;
  min-width: 50px;
  height: fit-content;
  display: flex;
  align-items: center;
  justify-content: center;
}

.record-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.record-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.record-button:active {
  transform: translateY(0);
}

.record-button.recording {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  animation: recordingPulse 1s infinite;
}

.record-button.recording:hover {
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

/* Recording active state */
.recording-active {
  border-color: #667eea !important;
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2) !important;
  animation: recordingPulse 2s infinite;
}

@keyframes recordingPulse {
  0% { box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2); }
  50% { box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.4); }
  100% { box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2); }
}

.form-group input[type="text"]:focus,
.form-group input[type="date"]:focus,
.form-group select:focus,
.form-group textarea:focus {
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
  outline: none;
}

.recording-active {
  border-color: #ffc107 !important;
  box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.4) !important;
  animation: pulse-border 1.5s infinite alternate;
}

@keyframes pulse-border {
  from {
    box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.4);
  }
  to {
    box-shadow: 0 0 0 6px rgba(255, 193, 7, 0.7);
  }
}

/* Locked field styles */
.field-locked {
  background-color: #f5f5f5 !important;
  color: #666 !important;
  cursor: not-allowed !important;
  border-color: #ccc !important;
  opacity: 0.7;
}

.field-locked:focus {
  border-color: #ccc !important;
  box-shadow: none !important;
}
</style>
