<template>
  <teleport to="body">
    <div class="toast-container">
      <transition-group name="toast" tag="div">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="getToastClasses(toast)"
          @click="removeToast(toast.id)"
        >
          <div class="toast-icon">
            <span>{{ getToastIcon(toast.type) }}</span>
          </div>
          <div class="toast-content">
            <div class="toast-title">{{ toast.title }}</div>
            <div class="toast-message">{{ toast.message }}</div>
          </div>
          <button class="toast-close" @click.stop="removeToast(toast.id)">
            ✕
          </button>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// Props
const props = defineProps({
  toasts: {
    type: Array,
    default: () => []
  }
})

// Emits
const emit = defineEmits(['remove'])

// Data
const autoRemoveTimers = ref(new Map())

// Methods
const removeToast = (toastId) => {
  // Clear auto-remove timer if exists
  const timer = autoRemoveTimers.value.get(toastId)
  if (timer) {
    clearTimeout(timer)
    autoRemoveTimers.value.delete(toastId)
  }
  
  emit('remove', toastId)
}

const getToastClasses = (toast) => {
  return [
    'toast',
    `toast--${toast.type}`,
    {
      'toast--clickable': toast.clickable !== false
    }
  ]
}

const getToastIcon = (type) => {
  const icons = {
    success: '✅',
    error: '❌',
    warning: '⚠️',
    info: 'ℹ️'
  }
  return icons[type] || icons.info
}

const setupAutoRemove = (toast) => {
  if (toast.duration && toast.duration > 0) {
    const timer = setTimeout(() => {
      removeToast(toast.id)
    }, toast.duration)
    
    autoRemoveTimers.value.set(toast.id, timer)
  }
}

// Watch for new toasts
import { watch } from 'vue'
watch(() => props.toasts, (newToasts) => {
  newToasts.forEach(toast => {
    if (!autoRemoveTimers.value.has(toast.id)) {
      setupAutoRemove(toast)
    }
  })
}, { deep: true })

// Cleanup on unmount
onUnmounted(() => {
  autoRemoveTimers.value.forEach(timer => clearTimeout(timer))
  autoRemoveTimers.value.clear()
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 1rem;
  right: 1rem;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  max-width: 400px;
  width: 100%;
}

.toast {
  display: flex;
  align-items: flex-start;
  gap: 0.75rem;
  padding: 1rem;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  border-left: 4px solid;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.toast--clickable:hover {
  transform: translateX(-2px);
  box-shadow: 0 8px 12px -1px rgba(0, 0, 0, 0.15), 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

.toast--success {
  border-left-color: #10b981;
  background: #f0fdf4;
}

.toast--error {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.toast--warning {
  border-left-color: #f59e0b;
  background: #fffbeb;
}

.toast--info {
  border-left-color: #3b82f6;
  background: #eff6ff;
}

.toast-icon {
  flex-shrink: 0;
  font-size: 1.25rem;
  line-height: 1;
}

.toast-content {
  flex: 1;
  min-width: 0;
}

.toast-title {
  font-weight: 600;
  font-size: 0.875rem;
  color: #1f2937;
  margin-bottom: 0.25rem;
}

.toast-message {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.4;
}

.toast-close {
  flex-shrink: 0;
  background: none;
  border: none;
  font-size: 1rem;
  color: #9ca3af;
  cursor: pointer;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
  line-height: 1;
}

.toast-close:hover {
  background: rgba(0, 0, 0, 0.05);
  color: #6b7280;
}

/* Toast transitions */
.toast-enter-active {
  transition: all 0.3s ease;
}

.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.toast-move {
  transition: transform 0.3s ease;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
  .toast {
    background: #1f2937;
    color: #f9fafb;
  }
  
  .toast--success {
    background: #064e3b;
  }
  
  .toast--error {
    background: #7f1d1d;
  }
  
  .toast--warning {
    background: #78350f;
  }
  
  .toast--info {
    background: #1e3a8a;
  }
  
  .toast-title {
    color: #f9fafb;
  }
  
  .toast-message {
    color: #d1d5db;
  }
  
  .toast-close {
    color: #9ca3af;
  }
  
  .toast-close:hover {
    background: rgba(255, 255, 255, 0.1);
    color: #d1d5db;
  }
}

/* Mobile responsiveness */
@media (max-width: 640px) {
  .toast-container {
    left: 1rem;
    right: 1rem;
    max-width: none;
  }
}
</style>

