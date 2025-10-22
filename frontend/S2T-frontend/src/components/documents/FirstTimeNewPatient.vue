<template>
  <div class="document-template first-time-patient">
    <h3>First Time New Patient Assessment</h3>
    <div class="form-section">
      <!-- Patient Information -->
      <div class="form-group">
        <label for="patientName">Patient Full Name</label>
        <input 
          type="text" 
          id="patientName" 
          v-model="formData.patientName" 
          @click="emitFieldClick('patientName')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'patientName' }"
          placeholder="Enter patient's full name"
        />
      </div>

      <div class="form-group">
        <label for="dateOfBirth">Date of Birth</label>
        <input 
          type="date" 
          id="dateOfBirth" 
          v-model="formData.dateOfBirth" 
          @click="emitFieldClick('dateOfBirth')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'dateOfBirth' }"
        />
      </div>

      <div class="form-group">
        <label for="gender">Gender</label>
        <select 
          id="gender" 
          v-model="formData.gender" 
          @click="emitFieldClick('gender')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'gender' }"
        >
          <option value="">Select Gender</option>
          <option value="Male">Male</option>
          <option value="Female">Female</option>
          <option value="Other">Other</option>
          <option value="Prefer not to say">Prefer not to say</option>
        </select>
      </div>

      <div class="form-group">
        <label for="contactInfo">Contact Information</label>
        <textarea 
          id="contactInfo" 
          v-model="formData.contactInfo" 
          @click="emitFieldClick('contactInfo')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'contactInfo' }"
          placeholder="Phone number, email address, emergency contact"
        ></textarea>
      </div>

      <!-- Medical History -->
      <div class="form-group">
        <label for="chiefComplaint">Chief Complaint</label>
        <textarea 
          id="chiefComplaint" 
          v-model="formData.chiefComplaint" 
          @click="emitFieldClick('chiefComplaint')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'chiefComplaint' }"
          placeholder="Primary reason for visit"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="presentIllness">History of Present Illness</label>
        <textarea 
          id="presentIllness" 
          v-model="formData.presentIllness" 
          @click="emitFieldClick('presentIllness')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'presentIllness' }"
          placeholder="Detailed description of current symptoms and their progression"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="pastMedicalHistory">Past Medical History</label>
        <textarea 
          id="pastMedicalHistory" 
          v-model="formData.pastMedicalHistory" 
          @click="emitFieldClick('pastMedicalHistory')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'pastMedicalHistory' }"
          placeholder="Previous medical conditions, surgeries, hospitalizations"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="medications">Current Medications</label>
        <textarea 
          id="medications" 
          v-model="formData.medications" 
          @click="emitFieldClick('medications')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'medications' }"
          placeholder="List all current medications, dosages, and frequency"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="allergies">Allergies</label>
        <textarea 
          id="allergies" 
          v-model="formData.allergies" 
          @click="emitFieldClick('allergies')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'allergies' }"
          placeholder="Drug allergies, food allergies, environmental allergies"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="familyHistory">Family History</label>
        <textarea 
          id="familyHistory" 
          v-model="formData.familyHistory" 
          @click="emitFieldClick('familyHistory')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'familyHistory' }"
          placeholder="Relevant family medical history"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="socialHistory">Social History</label>
        <textarea 
          id="socialHistory" 
          v-model="formData.socialHistory" 
          @click="emitFieldClick('socialHistory')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'socialHistory' }"
          placeholder="Smoking, alcohol, occupation, lifestyle factors"
        ></textarea>
      </div>

      <!-- Physical Examination -->
      <div class="form-group">
        <label for="vitalSigns">Vital Signs</label>
        <textarea 
          id="vitalSigns" 
          v-model="formData.vitalSigns" 
          @click="emitFieldClick('vitalSigns')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'vitalSigns' }"
          placeholder="Blood pressure, heart rate, temperature, respiratory rate, oxygen saturation"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="physicalExam">Physical Examination Findings</label>
        <textarea 
          id="physicalExam" 
          v-model="formData.physicalExam" 
          @click="emitFieldClick('physicalExam')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'physicalExam' }"
          placeholder="General appearance, head/neck, cardiovascular, respiratory, abdominal, neurological findings"
        ></textarea>
      </div>

      <!-- Assessment and Plan -->
      <div class="form-group">
        <label for="assessment">Assessment</label>
        <textarea 
          id="assessment" 
          v-model="formData.assessment" 
          @click="emitFieldClick('assessment')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'assessment' }"
          placeholder="Clinical impression and working diagnosis"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="plan">Treatment Plan</label>
        <textarea 
          id="plan" 
          v-model="formData.plan" 
          @click="emitFieldClick('plan')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'plan' }"
          placeholder="Diagnostic tests, medications, follow-up instructions"
        ></textarea>
      </div>

      <div class="form-group">
        <label for="followUp">Follow-up Instructions</label>
        <textarea 
          id="followUp" 
          v-model="formData.followUp" 
          @click="emitFieldClick('followUp')"
          :class="{ 'recording-active': isMicrophoneActive && activeRecordingField === 'followUp' }"
          placeholder="When to return, warning signs to watch for, lifestyle modifications"
        ></textarea>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, inject } from 'vue'

const props = defineProps({
  isMicrophoneActive: Boolean
})

const emit = defineEmits(['field-click'])

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

.form-group input[type="text"],
.form-group input[type="date"],
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 0.8rem 1rem;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 1rem;
  transition: all 0.2s ease-in-out;
  box-sizing: border-box;
}

.form-group textarea {
  min-height: 100px;
  resize: vertical;
}

.form-group select {
  cursor: pointer;
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
</style>
