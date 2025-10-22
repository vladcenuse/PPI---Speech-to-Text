<template>
  <div class="recording-view">
    <HeaderBar />
    <main class="main-content">
      <div class="page-header">
        <h2>Audio Recording</h2>
        <p>Record medical observations and save them for transcription</p>
      </div>

      <!-- Recording Status -->
      <div class="recording-status-card">
        <div class="status-indicator" :class="{ 'status-indicator--recording': isRecording }">
          <div class="status-icon">
            {{ isRecording ? '🔴' : '⚪' }}
          </div>
          <div class="status-text">
            <span v-if="isRecording">Recording...</span>
            <span v-else-if="isProcessing">Processing...</span>
            <span v-else>Ready to record</span>
          </div>
        </div>
        
        <div v-if="isRecording" class="recording-timer">
          <span class="timer-text">{{ formattedDuration }}</span>
        </div>
      </div>

      <!-- Recording Controls -->
      <div class="recording-controls">
        <button
          :class="['record-button', { 'record-button--recording': isRecording }]"
          :disabled="!canRecord || isProcessing"
          @click="toggleRecording"
        >
          <svg viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
            <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
          </svg>
          <span>{{ isRecording ? 'Stop Recording' : 'Start Recording' }}</span>
        </button>
      </div>

      <!-- Audio Visualization -->
      <div v-if="isRecording" class="audio-visualization">
        <div class="visualization-title">Audio Level</div>
        <div class="audio-bars">
          <div 
            v-for="(bar, index) in 20" 
            :key="index"
            class="audio-bar"
            :style="{ height: getRandomBarHeight() + '%' }"
          ></div>
        </div>
      </div>

      <!-- Recording History -->
      <div v-if="recordings.length > 0" class="recording-history">
        <h3>Recent Recordings</h3>
        <div class="history-list">
          <div 
            v-for="recording in recordings.slice(0, 5)" 
            :key="recording.id"
            class="history-item"
            :data-recording-id="recording.id"
          >
            <div class="recording-info">
              <div class="recording-title">Recording {{ recording.id }}</div>
              <div class="recording-details">
                {{ formatDate(recording.timestamp) }} - {{ recording.duration }}
              </div>
            </div>
            <div class="recording-actions">
              <button 
                @click="playRecording(recording.id)" 
                class="action-button play-button"
                :disabled="isProcessing"
                :title="`Play ${recording.title}`"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M8 5v14l11-7z"/>
                </svg>
              </button>
              <button 
                @click="deleteRecording(recording.id)" 
                class="action-button delete-button"
                :disabled="isProcessing"
              >
                <svg viewBox="0 0 24 24" fill="currentColor">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z"/>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon">🎤</div>
        <h3>No recordings yet</h3>
        <p>Start recording to capture medical observations</p>
      </div>
    </main>

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Delete Recording"
      :message="deleteMessage"
      :details="deleteDetails"
      confirm-text="Delete"
      cancel-text="Cancel"
      @confirm="confirmDelete"
      @cancel="cancelDelete"
      @close="cancelDelete"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import HeaderBar from '@/components/layout/HeaderBar.vue'
import ConfirmModal from '@/components/common/ConfirmModal.vue'
import { toastService } from '@/services/ToastService.js'

// State
const isRecording = ref(false)
const isProcessing = ref(false)
const canRecord = ref(true)
const recordingDuration = ref(0)
const recordingStartTime = ref(null)
const mediaRecorder = ref(null)
const audioChunks = ref([])
const recordings = ref([])
const showDeleteModal = ref(false)
const recordingToDelete = ref(null)
const currentAudio = ref(null)

// Computed
const formattedDuration = computed(() => {
  const minutes = Math.floor(recordingDuration.value / 60)
  const seconds = Math.floor(recordingDuration.value % 60)
  return `${minutes}:${seconds.toString().padStart(2, '0')}`
})

const deleteMessage = computed(() => {
  if (recordingToDelete.value) {
    return `Are you sure you want to delete Recording ${recordingToDelete.value}?`
  }
  return 'Are you sure you want to delete this recording?'
})

const deleteDetails = computed(() => {
  if (recordingToDelete.value) {
    const recording = recordings.value.find(r => r.id === recordingToDelete.value)
    if (recording) {
      return `This will permanently remove the recording from ${formatDate(recording.timestamp)} (${recording.duration}). This action cannot be undone.`
    }
  }
  return 'This action cannot be undone.'
})

// Methods
const toggleRecording = async () => {
  if (isRecording.value) {
    await stopRecording()
  } else {
    await startRecording()
  }
}

const startRecording = async () => {
  try {
    isRecording.value = true
    recordingStartTime.value = Date.now()
    recordingDuration.value = 0
    
    // Request microphone access
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    
    // Create MediaRecorder
    mediaRecorder.value = new MediaRecorder(stream)
    audioChunks.value = []
    
    // Handle data available
    mediaRecorder.value.ondataavailable = (event) => {
      if (event.data.size > 0) {
        audioChunks.value.push(event.data)
      }
    }
    
    // Start recording
    mediaRecorder.value.start()
    
    // Start duration timer
    const timer = setInterval(() => {
      if (isRecording.value) {
        recordingDuration.value = Math.floor((Date.now() - recordingStartTime.value) / 1000)
      } else {
        clearInterval(timer)
      }
    }, 1000)
    
    console.log('Recording started with real audio')
    toastService.success('Recording started', 'Microphone is now active')
    
  } catch (error) {
    console.error('Failed to start recording:', error)
    toastService.error('Recording failed', 'Could not access microphone')
    isRecording.value = false
  }
}

const stopRecording = async () => {
  try {
    isRecording.value = false
    isProcessing.value = true
    
    // Stop the MediaRecorder
    if (mediaRecorder.value && mediaRecorder.value.state === 'recording') {
      mediaRecorder.value.stop()
    }
    
    // Wait for the recording to finish processing
    await new Promise((resolve) => {
      if (mediaRecorder.value) {
        mediaRecorder.value.onstop = () => {
          // Create audio blob from chunks
          const audioBlob = new Blob(audioChunks.value, { type: 'audio/wav' })
          
          // Create audio URL
          const audioUrl = URL.createObjectURL(audioBlob)
          
          // Create recording entry with real audio
          const recording = {
            id: Date.now(),
            title: `Recording ${recordings.value.length + 1}`,
            timestamp: new Date(),
            duration: formattedDuration.value,
            size: `${(audioBlob.size / (1024 * 1024)).toFixed(1)} MB`,
            audioBlob: audioBlob,
            audioUrl: audioUrl
          }
          
          recordings.value.unshift(recording)
          
          // Show success message
          toastService.success('Recording saved!', `Recording ${recording.title} has been saved successfully`)
          
          resolve()
        }
      } else {
        resolve()
      }
    })
    
    setTimeout(() => {
      isProcessing.value = false
    }, 1000)
    
    console.log('Recording stopped and saved with real audio')
    
  } catch (error) {
    console.error('Failed to stop recording:', error)
    toastService.error('Recording failed', 'Could not save recording')
    isProcessing.value = false
  }
}

const playRecording = (recordingId) => {
  console.log('🎵 PLAY BUTTON CLICKED! Recording ID:', recordingId)
  console.log('Current recordings:', recordings.value)
  
  try {
    // Find the recording
    const recording = recordings.value.find(r => r.id === recordingId)
    if (!recording) {
      console.error('Recording not found:', recordingId)
      toastService.error('Recording not found', 'The selected recording could not be found')
      return
    }
    
    // Find the recording element for visual feedback
    const recordingElement = document.querySelector(`[data-recording-id="${recordingId}"]`)
    if (!recordingElement) {
      console.error('Recording element not found in DOM:', recordingId)
      toastService.error('Playback error', 'Could not find recording element')
      return
    }
    
    // Add visual feedback for playing state
    recordingElement.classList.add('playing')
    
    // Show immediate feedback
    toastService.success('Playing recording...', `Now playing: ${recording.title}`)
    
    // Stop any currently playing audio
    if (currentAudio.value) {
      currentAudio.value.pause()
      currentAudio.value.currentTime = 0
    }
    
    // Create audio element for playback
    const audio = new Audio()
    currentAudio.value = audio
    
    // Set the audio source
    if (recording.audioUrl) {
      audio.src = recording.audioUrl
    } else {
      toastService.error('Playback failed', 'No audio data available for this recording')
      recordingElement.classList.remove('playing')
      return
    }
    
    // Handle audio events
    audio.onloadeddata = () => {
      console.log('Audio loaded, starting playback')
      audio.play().catch(error => {
        console.error('Playback failed:', error)
        toastService.error('Playback failed', 'Could not play audio')
        recordingElement.classList.remove('playing')
      })
    }
    
    audio.onended = () => {
      console.log('Playback completed')
      recordingElement.classList.remove('playing')
      toastService.info('Playback complete', 'Recording playback finished')
      currentAudio.value = null
    }
    
    audio.onerror = (error) => {
      console.error('Audio error:', error)
      toastService.error('Playback failed', 'Error playing audio')
      recordingElement.classList.remove('playing')
      currentAudio.value = null
    }
    
    console.log('Audio playback started for recording:', recording.title)
    
  } catch (error) {
    console.error('Error playing recording:', error)
    toastService.error('Playback failed', 'An error occurred while playing the recording')
    
    // Remove visual feedback on error
    const recordingElement = document.querySelector(`[data-recording-id="${recordingId}"]`)
    if (recordingElement) {
      recordingElement.classList.remove('playing')
    }
  }
}

const deleteRecording = (recordingId) => {
  recordingToDelete.value = recordingId
  showDeleteModal.value = true
}

const confirmDelete = () => {
  if (recordingToDelete.value) {
    recordings.value = recordings.value.filter(r => r.id !== recordingToDelete.value)
    console.log('Recording deleted:', recordingToDelete.value)
    toastService.success('Recording deleted', 'The recording has been successfully removed')
  }
  showDeleteModal.value = false
  recordingToDelete.value = null
}

const cancelDelete = () => {
  showDeleteModal.value = false
  recordingToDelete.value = null
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getRandomBarHeight = () => {
  return Math.random() * 100
}

// Lifecycle
onMounted(() => {
  // Initialize recording functionality
  console.log('Recording view mounted')
})
</script>

<style scoped>
.recording-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.recording-view::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 80%, rgba(120, 119, 198, 0.3) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 40% 40%, rgba(120, 119, 198, 0.2) 0%, transparent 50%);
  animation: float 20s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  33% { transform: translateY(-20px) rotate(1deg); }
  66% { transform: translateY(10px) rotate(-1deg); }
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 4rem 2rem;
  position: relative;
  z-index: 1;
}

.page-header {
  text-align: center;
  margin-bottom: 3rem;
}

.page-header h2 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 3.5rem;
  font-weight: 700;
  text-shadow: 0 4px 20px rgba(0,0,0,0.3);
  background: linear-gradient(45deg, #ffffff, #f0f0f0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
}

.page-header p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.4rem;
  font-weight: 300;
  line-height: 1.6;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.recording-status-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  text-align: center;
  margin-bottom: 2rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.status-indicator {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.status-indicator--recording {
  animation: pulse 2s infinite;
}

.status-icon {
  font-size: 2rem;
}

.status-text {
  font-size: 1.4rem;
  font-weight: 600;
  color: white;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

.recording-timer {
  font-size: 2rem;
  font-weight: bold;
  color: #e74c3c;
}

.recording-controls {
  display: flex;
  justify-content: center;
  margin-bottom: 2rem;
}

.record-button {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  border: none;
  padding: 1.2rem 2.5rem;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  min-width: 200px;
  justify-content: center;
  position: relative;
  overflow: hidden;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.record-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.record-button:hover::before {
  left: 100%;
}

.record-button:hover:not(:disabled) {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6);
}

.record-button--recording {
  background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%);
  animation: pulse 2s infinite;
}

.record-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.record-button svg {
  width: 24px;
  height: 24px;
}

.audio-visualization {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.audio-visualization::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, transparent, rgba(255,255,255,0.05), transparent);
  animation: shimmer 3s ease-in-out infinite;
  pointer-events: none;
}

.visualization-title {
  text-align: center;
  font-weight: 700;
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
  background: linear-gradient(45deg, #ffffff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
}

.audio-bars {
  display: flex;
  align-items: end;
  justify-content: center;
  gap: 3px;
  height: 120px;
  padding: 1rem 0;
  position: relative;
  z-index: 1;
}

.audio-bar {
  width: 10px;
  background: linear-gradient(180deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  border-radius: 5px 5px 0 0;
  transition: height 0.1s ease;
  box-shadow: 
    0 2px 8px rgba(102, 126, 234, 0.3),
    inset 0 1px 0 rgba(255,255,255,0.2);
  position: relative;
  min-height: 4px;
}

.audio-bar::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(180deg, rgba(255,255,255,0.3) 0%, transparent 50%);
  border-radius: 5px 5px 0 0;
  pointer-events: none;
}

.audio-bar:hover {
  transform: scaleY(1.1);
  box-shadow: 
    0 4px 12px rgba(102, 126, 234, 0.4),
    inset 0 1px 0 rgba(255,255,255,0.3);
}

.recording-history {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 2rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.recording-history h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 8px rgba(0,0,0,0.3);
  background: linear-gradient(45deg, #ffffff, #e0e0e0);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: shimmer 3s ease-in-out infinite;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.recording-info {
  flex: 1;
}

.recording-title {
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 0.25rem;
}

.recording-details {
  color: #6c757d;
  font-size: 0.9rem;
}

.recording-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  background: #667eea;
  color: white;
  border: none;
  padding: 0.75rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 40px;
  min-height: 40px;
  position: relative;
  z-index: 10;
  pointer-events: auto;
}

.action-button:hover:not(:disabled) {
  background: #5a6fd8;
  transform: scale(1.05);
  box-shadow: 0 2px 8px rgba(0,0,0,0.2);
}

.action-button:active:not(:disabled) {
  transform: scale(0.95);
}

.action-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

.action-button svg {
  width: 18px;
  height: 18px;
  pointer-events: none;
}

.play-button {
  background: #28a745;
}

.play-button:hover:not(:disabled) {
  background: #218838;
  box-shadow: 0 2px 8px rgba(40, 167, 69, 0.3);
}

.delete-button {
  background: #dc3545;
}

.delete-button:hover:not(:disabled) {
  background: #c82333;
}

.history-item.playing {
  background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
  border-color: #2196f3;
  animation: pulse-playing 1.5s ease-in-out infinite;
}

@keyframes pulse-playing {
  0%, 100% { 
    box-shadow: 0 0 0 0 rgba(33, 150, 243, 0.4);
  }
  50% { 
    box-shadow: 0 0 0 8px rgba(33, 150, 243, 0);
  }
}

.empty-state {
  text-align: center;
  padding: 4rem 2rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-top: 2rem;
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.3));
}

.empty-state h3 {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 1.8rem;
  font-weight: 700;
  text-shadow: 0 2px 10px rgba(0,0,0,0.5);
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@media (max-width: 768px) {
  .main-content {
    padding: 1rem;
  }
  
  .record-button {
    min-width: 150px;
    padding: 0.75rem 1.5rem;
  }
}
</style>