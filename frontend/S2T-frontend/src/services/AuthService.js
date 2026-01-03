const API_BASE_URL = 'http://127.0.0.1:8000';
const AUTH_ENDPOINT = `${API_BASE_URL}/api/auth`;

class AuthService {
  constructor() {
    this.tokenKey = 's2t_auth_token';
    this.doctorKey = 's2t_doctor_info';
  }

  getToken() {
    return localStorage.getItem(this.tokenKey);
  }

  getDoctorInfo() {
    const info = localStorage.getItem(this.doctorKey);
    return info ? JSON.parse(info) : null;
  }

  setAuth(token, doctorInfo) {
    localStorage.setItem(this.tokenKey, token);
    localStorage.setItem(this.doctorKey, JSON.stringify(doctorInfo));
  }

  clearAuth() {
    localStorage.removeItem(this.tokenKey);
    localStorage.removeItem(this.doctorKey);
  }

  isAuthenticated() {
    return !!this.getToken();
  }

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

export const authService = new AuthService();
export default authService;

