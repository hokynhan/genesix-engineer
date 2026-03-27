<template>
  <div class="login-container">
    <div class="glass-card">
      <div class="logo-box">
        <div class="logo-circle"></div>
      </div>
      <h2>Welcome Back</h2>
      <p class="subtitle">Please enter your details to sign in.</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="input-group">
          <label for="username">Username / Email</label>
          <input 
            type="email" 
            id="username" 
            v-model="email" 
            placeholder="Enter your email" 
            required
            :disabled="loading"
          >
        </div>
        
        <div class="input-group">
          <label for="password">Password</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            required
            :disabled="loading"
          >
        </div>
        
        <button type="submit" class="primary-btn" :disabled="loading">
          <span v-if="loading" class="spinner"></span>
          <span v-else>Login</span>
        </button>
      </form>
      
      <div v-if="errorMsg" class="error-message">
        {{ errorMsg }}
      </div>
    </div>
    
    <div class="background-elements">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'

const router = useRouter()
const email = ref('')
const password = ref('')
const errorMsg = ref('')
const loading = ref(false)

const handleLogin = async () => {
  try {
    loading.value = true
    errorMsg.value = ''
    
    const { error } = await supabase.auth.signInWithPassword({
      email: email.value,
      password: password.value
    })
    
    if (error) {
      errorMsg.value = error.message
    } else {
      router.push('/dashboard')
    }
  } catch (error) {
    errorMsg.value = 'An unexpected error occurred. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background-color: var(--bg-color);
}

.glass-card {
  background: var(--glass-bg);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border: 1px solid var(--glass-border);
  border-radius: 24px;
  padding: 48px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  animation: fadeIn 0.8s ease-out forwards;
}

.logo-box {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  width: 60px;
  height: 60px;
  border-radius: 16px;
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 24px;
  box-shadow: 0 10px 20px rgba(99, 102, 241, 0.3);
}

.logo-circle {
  width: 30px;
  height: 30px;
  border: 3px solid white;
  border-radius: 50%;
  border-right-color: transparent;
  transform: rotate(45deg);
}

h2 {
  font-size: 28px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
  text-align: center;
}

.subtitle {
  color: var(--text-secondary);
  font-size: 14px;
  margin-bottom: 32px;
  text-align: center;
}

.login-form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: var(--text-secondary);
  margin-left: 4px;
}

input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 14px 16px;
  font-size: 15px;
  color: var(--text-primary);
  transition: all 0.3s ease;
  outline: none;
  font-family: inherit;
}

input:focus {
  border-color: var(--primary-color);
  background: rgba(255, 255, 255, 0.05);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1);
}

input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.primary-btn {
  background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
  color: white;
  border: none;
  border-radius: 12px;
  padding: 14px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 12px;
  display: flex;
  justify-content: center;
  align-items: center;
  box-shadow: 0 10px 20px -5px rgba(99, 102, 241, 0.4);
}

.primary-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 15px 25px -5px rgba(99, 102, 241, 0.5);
}

.primary-btn:active:not(:disabled) {
  transform: translateY(0);
}

.primary-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.error-message {
  margin-top: 20px;
  padding: 12px 16px;
  background: rgba(239, 68, 68, 0.1);
  border-left: 4px solid var(--error-color);
  border-radius: 8px;
  color: var(--error-color);
  font-size: 14px;
  width: 100%;
  animation: slideIn 0.3s ease-out;
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 0.8s linear infinite;
}

.background-elements {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: 1;
}

.blob {
  position: absolute;
  filter: blur(80px);
  border-radius: 50%;
  opacity: 0.5;
  animation: float 10s infinite alternate ease-in-out;
}

.blob-1 {
  background: var(--primary-color);
  width: 400px;
  height: 400px;
  top: -100px;
  right: -100px;
}

.blob-2 {
  background: var(--secondary-color);
  width: 300px;
  height: 300px;
  bottom: -50px;
  left: -100px;
  animation-delay: -5s;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
  from { opacity: 0; transform: translateX(-10px); }
  to { opacity: 1; transform: translateX(0); }
}

@keyframes float {
  0% { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-30px, 30px) scale(1.1); }
}

@media (max-width: 480px) {
  .glass-card {
    padding: 32px 24px;
    border-radius: 16px;
    margin: 20px;
  }
}
</style>
