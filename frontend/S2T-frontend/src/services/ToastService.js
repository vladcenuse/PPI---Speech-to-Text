/**
 * Toast Service
 * Comprehensive toast notification system
 */

import { reactive, ref } from 'vue'

class ToastService {
  constructor() {
    this.toasts = reactive([])
    this.maxToasts = 5
    this.defaultDuration = 5000
    this.position = 'top-left'
  }

  /**
   * Show a toast notification
   */
  show(message, type = 'info', options = {}) {
    const toast = {
      id: Date.now() + Math.random(),
      message,
      type,
      duration: options.duration || this.defaultDuration,
      position: options.position || this.position,
      timestamp: new Date().toISOString(),
      persistent: options.persistent || false,
      actions: options.actions || [],
      title: options.title || null,
      icon: options.icon || this.getDefaultIcon(type),
      closable: options.closable !== false
    }

    this.toasts.push(toast)

    // Remove oldest toast if we exceed max count
    if (this.toasts.length > this.maxToasts) {
      this.toasts.shift()
    }

    // Auto remove toast after duration (unless persistent)
    if (!toast.persistent && toast.duration > 0) {
      setTimeout(() => {
        this.remove(toast.id)
      }, toast.duration)
    }

    return toast.id
  }

  /**
   * Show success toast
   */
  success(message, options = {}) {
    return this.show(message, 'success', {
      icon: '✓',
      ...options
    })
  }

  /**
   * Show error toast
   */
  error(message, options = {}) {
    return this.show(message, 'error', {
      icon: '✕',
      duration: options.duration || 7000, // Longer duration for errors
      ...options
    })
  }

  /**
   * Show warning toast
   */
  warning(message, options = {}) {
    return this.show(message, 'warning', {
      icon: '!',
      ...options
    })
  }

  /**
   * Show info toast
   */
  info(message, options = {}) {
    return this.show(message, 'info', {
      icon: 'i',
      ...options
    })
  }

  /**
   * Show loading toast
   */
  loading(message, options = {}) {
    return this.show(message, 'loading', {
      icon: '⟳',
      persistent: true,
      closable: false,
      ...options
    })
  }

  /**
   * Show confirmation toast with actions
   */
  confirm(message, actions = [], options = {}) {
    return this.show(message, 'confirm', {
      icon: '?',
      persistent: true,
      actions,
      ...options
    })
  }

  /**
   * Remove toast by ID
   */
  remove(toastId) {
    const index = this.toasts.findIndex(toast => toast.id === toastId)
    if (index > -1) {
      this.toasts.splice(index, 1)
    }
  }

  /**
   * Clear all toasts
   */
  clear() {
    this.toasts.splice(0)
  }

  /**
   * Clear toasts by type
   */
  clearByType(type) {
    this.toasts.splice(0, this.toasts.length, ...this.toasts.filter(toast => toast.type !== type))
  }

  /**
   * Get default icon for toast type
   */
  getDefaultIcon(type) {
    const icons = {
      success: '✓',
      error: '✕',
      warning: '!',
      info: 'i',
      loading: '⟳',
      confirm: '?'
    }
    return icons[type] || icons.info
  }

  /**
   * Update toast message
   */
  update(toastId, updates) {
    const toast = this.toasts.find(t => t.id === toastId)
    if (toast) {
      Object.assign(toast, updates)
    }
  }

  /**
   * Convert loading toast to success
   */
  loadingToSuccess(toastId, message) {
    this.update(toastId, {
      type: 'success',
      message,
      icon: '✓',
      persistent: false,
      closable: true
    })
    
    // Auto remove after success
    setTimeout(() => {
      this.remove(toastId)
    }, 3000)
  }

  /**
   * Convert loading toast to error
   */
  loadingToError(toastId, message) {
    this.update(toastId, {
      type: 'error',
      message,
      icon: '✕',
      persistent: false,
      closable: true
    })
    
    // Auto remove after error
    setTimeout(() => {
      this.remove(toastId)
    }, 5000)
  }

  /**
   * Get toasts by position
   */
  getToastsByPosition(position) {
    return this.toasts.filter(toast => toast.position === position)
  }

  /**
   * Get toasts by type
   */
  getToastsByType(type) {
    return this.toasts.filter(toast => toast.type === type)
  }

  /**
   * Check if there are any toasts
   */
  hasToasts() {
    return this.toasts.length > 0
  }

  /**
   * Get toast count
   */
  getToastCount() {
    return this.toasts.length
  }

  /**
   * Get toast count by type
   */
  getToastCountByType(type) {
    return this.toasts.filter(toast => toast.type === type).length
  }
}

// Create and export singleton instance
export const toastService = new ToastService()
export default toastService

