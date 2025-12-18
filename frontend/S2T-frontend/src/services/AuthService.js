/**
 * Authentication Service
 * Handles doctor login, registration, and session management
 */

const API_BASE_URL = 'http://127.0.0.1:8000';
const AUTH_ENDPOINT = `${API_BASE_URL}/api/auth`;

class AuthService {
  constructor() {
    this.tokenKey = 's2t_auth_token';
    this.doctorKey = 's2t_doctor_info';
  }

  /**
   * Get stored auth token
   */
  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  /**
   * Get stored doctor info
   */
  getDoctorInfo() {
    const info = localStorage.getItem(this.doctorKey);
    return info ? JSON.parse(info) : null;
  }

  /**
   * Set auth token and doctor info
   */
  setAuth(token, doctorInfo) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.doctorKey, JSON.stringify(doctorInfo));
  }

  /**
   * Clear auth data
   */
  clearAuth() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.doctorKey);
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!this.getToken();
  }

  /**
   * Register a new doctor account
   */
  async register(username, password, confirmPassword) {
    try {
      const response = await fetch(`${AUTH_ENDPOINT}/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
          confirm_password: confirmPassword,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Registration failed');
      }

      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Login doctor
   */
  async login(username, password) {
    try {
      const response = await fetch(`${AUTH_ENDPOINT}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username,
          password,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || 'Login failed');
      }

      // Store token and doctor info
      const token = data.token || `Bearer ${data.doctor_id}_${Date.now()}`;
      console.log(' Login successful, storing token:', token.substring(0, 30) + '...');
      this.setAuth(token, {
        id: data.doctor_id,
        username: data.username,
      });
      console.log(' Token stored. Current token:', this.getToken()?.substring(0, 30) + '...');

      return data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Logout doctor
   */
  async logout() {
    try {
      const token = this.getToken();
      if (token) {
        await fetch(`${AUTH_ENDPOINT}/logout`, {
          method: 'POST',
          headers: {
            'Authorization': token,
          },
        });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      this.clearAuth();
    }
  }

  /**
   * Get authorization header for API requests
   */
  getAuthHeader() {
    const token = this.getToken();
    if (!token) {
      console.warn('⚠️ No token found in storage!');
      return {};
    }
    console.log('🔑 Getting auth header, token:', token.substring(0, 30) + '...');
    return { 'Authorization': token };
  }
}

// Create and export singleton instance
export const authService = new AuthService();
export default authService;

