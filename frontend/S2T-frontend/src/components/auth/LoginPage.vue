<template>
  <div class="login-page">
    <div class="login-container">
      <div class="login-header">
        <h1>Speech-to-Text Medical System</h1>
        <p>Doctor Authentication</p>
      </div>

      <!-- Login Form -->
      <div v-if="!showRegister" class="login-form">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="login-username">Username</label>
            <input
              id="login-username"
              v-model="loginForm.username"
              type="text"
              required
              placeholder="Enter your username"
            />
          </div>
          <div class="form-group">
            <label for="login-password">Password</label>
            <input
              id="login-password"
              v-model="loginForm.password"
              type="password"
              required
              placeholder="Enter your password"
            />
          </div>
          <div v-if="loginError" class="error-message">
            {{ loginError }}
          </div>
          <button type="submit" class="btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <div class="form-footer">
          <p>Don't have an account? <a href="#" @click.prevent="showRegister = true">Register here</a></p>
        </div>
      </div>

      <!-- Registration Form -->
      <div v-else class="register-form">
        <h2>Create Account</h2>
        <form @submit.prevent="handleRegister">
          <div class="form-group">
            <label for="register-username">Username</label>
            <input
              id="register-username"
              v-model="registerForm.username"
              type="text"
              required
              placeholder="Choose a username"
            />
          </div>
          <div class="form-group">
            <label for="register-password">Password</label>
            <input
              id="register-password"
              v-model="registerForm.password"
              type="password"
              required
              placeholder="Create a password (min 6 characters)"
              minlength="6"
            />
          </div>
          <div class="form-group">
            <label for="register-confirm">Confirm Password</label>
            <input
              id="register-confirm"
              v-model="registerForm.confirmPassword"
              type="password"
              required
              placeholder="Confirm your password"
            />
          </div>
          <div v-if="registerError" class="error-message">
            {{ registerError }}
          </div>
          <button type="submit" class="btn-primary" :disabled="isLoading">
            {{ isLoading ? 'Creating account...' : 'Create Account' }}
          </button>
        </form>
        <div class="form-footer">
          <p>Already have an account? <a href="#" @click.prevent="showRegister = false">Login here</a></p>
        </div>
      </div>

      <!-- Success Modal -->
      <div v-if="showSuccessModal" class="modal-overlay" @click="showSuccessModal = false">
        <div class="modal-content" @click.stop>
          <div class="success-icon">✓</div>
          <h3>Account Created Successfully!</h3>
          <p>Your account has been created. You can now login with your credentials.</p>
          <button @click="handleSuccessClose" class="btn-primary">Go to Login</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { authService } from '@/services/AuthService.js'

const showRegister = ref(false)
const isLoading = ref(false)
const loginError = ref('')
const registerError = ref('')
const showSuccessModal = ref(false)

const loginForm = ref({
  username: '',
  password: '',
})

const registerForm = ref({
  username: '',
  password: '',
  confirmPassword: '',
})

const handleLogin = async () => {
  isLoading.value = true
  loginError.value = ''
  
  try {
    await authService.login(loginForm.value.username, loginForm.value.password)
    // Notify App.vue that auth state changed
    window.dispatchEvent(new Event('auth-changed'))
  } catch (error) {
    loginError.value = error.message || 'Login failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleRegister = async () => {
  isLoading.value = true
  registerError.value = ''
  
  if (registerForm.value.password !== registerForm.value.confirmPassword) {
    registerError.value = 'Passwords do not match'
    isLoading.value = false
    return
  }
  
  if (registerForm.value.password.length < 6) {
    registerError.value = 'Password must be at least 6 characters'
    isLoading.value = false
    return
  }
  
  try {
    await authService.register(
      registerForm.value.username,
      registerForm.value.password,
      registerForm.value.confirmPassword
    )
    showSuccessModal.value = true
  } catch (error) {
    registerError.value = error.message || 'Registration failed. Please try again.'
  } finally {
    isLoading.value = false
  }
}

const handleSuccessClose = () => {
  showSuccessModal.value = false
  showRegister.value = false
  // Clear registration form
  registerForm.value = {
    username: '',
    password: '',
    confirmPassword: '',
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 2rem;
}

.login-container {
  background: white;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 3rem;
  width: 100%;
  max-width: 450px;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h1 {
  color: #667eea;
  margin: 0 0 0.5rem 0;
  font-size: 1.8rem;
}

.login-header p {
  color: #666;
  margin: 0;
}

.login-form h2,
.register-form h2 {
  color: #333;
  margin-bottom: 1.5rem;
  text-align: center;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.form-group input {
  width: 100%;
  padding: 0.75rem;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

.form-group input:focus {
  outline: none;
  border-color: #667eea;
}

.error-message {
  background: #fee;
  color: #c33;
  padding: 0.75rem;
  border-radius: 8px;
  margin-bottom: 1rem;
  font-size: 0.9rem;
}

.btn-primary {
  width: 100%;
  padding: 0.75rem;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.3s;
}

.btn-primary:hover:not(:disabled) {
  background: #5568d3;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.form-footer {
  margin-top: 1.5rem;
  text-align: center;
}

.form-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.form-footer a:hover {
  text-decoration: underline;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 20px;
  padding: 2rem;
  max-width: 400px;
  text-align: center;
}

.success-icon {
  width: 80px;
  height: 80px;
  background: #4caf50;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 3rem;
  margin: 0 auto 1rem;
}

.modal-content h3 {
  color: #333;
  margin-bottom: 1rem;
}

.modal-content p {
  color: #666;
  margin-bottom: 1.5rem;
}
</style>

