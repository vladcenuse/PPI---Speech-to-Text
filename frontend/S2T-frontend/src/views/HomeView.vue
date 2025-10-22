<template>
  <div class="home-view">
    <HeaderBar />
    <main class="main-content">
      <div class="welcome-section">
        <h2>Welcome to Speech-to-Text Medical System</h2>
        <p>Transform healthcare documentation with AI-powered voice recognition technology</p>
        
        <div class="action-buttons">
          <router-link to="/patients" class="btn btn-primary">
            Manage Patients
          </router-link>
          <router-link to="/recording" class="btn btn-secondary">
            Start Recording
          </router-link>
          <router-link to="/documents" class="btn btn-secondary">
            Document Templates
          </router-link>
        </div>
      </div>
      
      <div class="features-grid">
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3z"/>
              <path d="M17 11c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z"/>
            </svg>
          </div>
          <h3>Voice Recording</h3>
          <p>Record medical observations with high-quality audio capture and advanced noise reduction technology</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z"/>
            </svg>
          </div>
          <h3>Smart Document Processing</h3>
          <p>Intelligently process transcribed audio into structured medical documents with AI-powered data extraction</p>
        </div>
        <div class="feature-card">
          <div class="feature-icon">
            <svg viewBox="0 0 24 24" fill="currentColor">
              <path d="M14,2H6A2,2 0 0,0 4,4V20A2,2 0 0,0 6,22H18A2,2 0 0,0 20,20V8L14,2M18,20H6V4H13V9H18V20Z M12,12L8,16H11V20H13V16H16L12,12Z"/>
            </svg>
          </div>
          <h3>Export Documents</h3>
          <p>Generate professional Word documents and PDFs from patient records with customizable templates</p>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import HeaderBar from '@/components/layout/HeaderBar.vue'
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  position: relative;
  overflow: hidden;
}

.home-view::before {
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

.welcome-section {
  text-align: center;
  margin-bottom: 5rem;
  animation: fadeInUp 1s ease-out;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.welcome-section h2 {
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

@keyframes shimmer {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.welcome-section p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1.4rem;
  margin-bottom: 3rem;
  font-weight: 300;
  line-height: 1.6;
  text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.action-buttons {
  display: flex;
  gap: 1.5rem;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 1s ease-out 0.3s both;
}

.btn {
  padding: 1.2rem 2.5rem;
  border-radius: 50px;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: none;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  font-size: 1.1rem;
  letter-spacing: 0.5px;
  text-transform: uppercase;
}

.btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s;
}

.btn:hover::before {
  left: 100%;
}

.btn-primary {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  color: white;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.btn-primary:hover {
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.15);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px) scale(1.05);
  box-shadow: 0 15px 35px rgba(255, 255, 255, 0.2);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2.5rem;
  margin-top: 4rem;
  animation: fadeInUp 1s ease-out 0.6s both;
}

.feature-card {
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(20px);
  padding: 3rem 2.5rem;
  border-radius: 20px;
  box-shadow: 
    0 8px 32px rgba(0,0,0,0.1),
    inset 0 1px 0 rgba(255,255,255,0.2);
  text-align: center;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.2);
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.feature-card:hover::before {
  opacity: 1;
}

.feature-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 
    0 20px 40px rgba(0,0,0,0.15),
    inset 0 1px 0 rgba(255,255,255,0.3);
  border-color: rgba(255, 255, 255, 0.4);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 2rem;
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.4);
}

.feature-card:hover .feature-icon {
  transform: scale(1.15) rotate(5deg);
  box-shadow: 0 15px 35px rgba(255, 107, 107, 0.6);
}

.feature-icon svg {
  width: 40px;
  height: 40px;
  transition: transform 0.3s ease;
}

.feature-card:hover .feature-icon svg {
  transform: scale(1.1);
}

.feature-card h3 {
  color: white;
  margin-bottom: 1.5rem;
  font-size: 1.5rem;
  font-weight: 600;
  text-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.feature-card p {
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.7;
  font-size: 1rem;
  font-weight: 300;
  text-shadow: 0 1px 5px rgba(0,0,0,0.2);
}

/* Responsive Design */
@media (max-width: 768px) {
  .main-content {
    padding: 2rem 1rem;
  }
  
  .welcome-section h2 {
    font-size: 2.5rem;
  }
  
  .welcome-section p {
    font-size: 1.2rem;
  }
  
  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .btn {
    width: 100%;
    max-width: 300px;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .feature-card {
    padding: 2rem 1.5rem;
  }
}

@media (max-width: 480px) {
  .welcome-section h2 {
    font-size: 2rem;
  }
  
  .welcome-section p {
    font-size: 1rem;
  }
  
  .feature-card {
    padding: 1.5rem 1rem;
  }
  
  .feature-icon {
    width: 60px;
    height: 60px;
  }
  
  .feature-icon svg {
    width: 30px;
    height: 30px;
  }
}
</style>
