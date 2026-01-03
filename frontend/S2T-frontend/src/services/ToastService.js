class ToastService {
  constructor() {
    this.toasts = []
    this.nextId = 1
  }

  add(toast) {
    const id = this.nextId++
    const newToast = {
      id,
      type: 'info',
      position: 'top-right',
      duration: 4000,
      closable: true,
      persistent: false,
      ...toast
    }

    this.toasts.push(newToast)

    if (!newToast.persistent && newToast.duration > 0) {
      setTimeout(() => {
        this.remove(id)
      }, newToast.duration)
    }

    return id
  }

  remove(toastId) {
    this.toasts = this.toasts.filter(toast => toast.id !== toastId)
  }

  getToastsByPosition(position) {
    return this.toasts.filter(toast => toast.position === position)
  }

  clear() {
    this.toasts = []
  }

  success(title, message = '', options = {}) {
    return this.add({
      type: 'success',
      title,
      message,
      icon: '✅',
      ...options
    })
  }

  error(title, message = '', options = {}) {
    return this.add({
      type: 'error',
      title,
      message,
      icon: '❌',
      ...options
    })
  }

  warning(title, message = '', options = {}) {
    return this.add({
      type: 'warning',
      title,
      message,
      icon: '⚠️',
      ...options
    })
  }

  info(title, message = '', options = {}) {
    return this.add({
      type: 'info',
      title,
      message,
      icon: 'ℹ️',
      ...options
    })
  }

  loading(title, message = '', options = {}) {
    return this.add({
      type: 'loading',
      title,
      message,
      icon: '⏳',
      persistent: true,
      closable: false,
      ...options
    })
  }
}

const toastService = new ToastService()

export { toastService }