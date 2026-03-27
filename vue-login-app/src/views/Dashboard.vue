<template>
  <div class="dashboard-container">
    <nav class="navbar">
      <div class="logo">
        <span class="logo-text">App Dashboard</span>
      </div>
      <button @click="handleLogout" class="logout-btn">
        Logout
      </button>
    </nav>
    
    <main class="content">
      <div class="welcome-card">
        <h2>Welcome to your Dashboard</h2>
        <p>Logged in as: <span class="user-email">{{ user?.email || 'Loading...' }}</span></p>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { supabase } from '../supabase'

const router = useRouter()
const user = ref(null)

onMounted(async () => {
  const { data: { session } } = await supabase.auth.getSession()
  
  if (session) {
    // Send the access_token to our FastAPI backend to identify the user
    try {
      const response = await fetch("http://localhost:8000/api/user", {
        headers: {
          "Authorization": `Bearer ${session.access_token}`
        }
      })
      
      if (response.ok) {
        const data = await response.json()
        // data.email comes from your Python server
        user.value = { email: data.email }
      } else {
        console.error("Backend error fetching user")
      }
    } catch (error) {
      console.error("Failed to connect to backend", error)
    }
  }
})

const handleLogout = async () => {
  await supabase.auth.signOut()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-container {
  min-height: 100vh;
  background-color: #0b1120;
  color: #ffffff;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
}

.navbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 40px;
  background-color: #1e293b;
  border-bottom: 1px solid #334155;
  box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
}

.logo-text {
  font-size: 20px;
  font-weight: 600;
  color: #818cf8;
}

.logout-btn {
  background: transparent;
  border: 1px solid #475569;
  color: #cbd5e1;
  padding: 6px 16px;
  border-radius: 6px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.logout-btn:hover {
  background: #334155;
  color: #ffffff;
}

.content {
  padding: 40px;
  max-width: 1000px;
  margin: 0 auto;
}

.welcome-card {
  background-color: #1e293b;
  border-radius: 8px;
  padding: 32px 40px;
  border: 1px solid #334155;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3), 0 2px 4px -1px rgba(0, 0, 0, 0.2);
}

.welcome-card h2 {
  font-size: 24px;
  font-weight: 600;
  margin: 0 0 12px 0;
  color: #f8fafc;
}

.welcome-card p {
  font-size: 15px;
  color: #94a3b8;
  margin: 0;
}

.user-email {
  font-weight: 500;
  color: #cbd5e1;
}
</style>
