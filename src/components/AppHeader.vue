// src/components/AppHeader.vue

<template>
  <header>
    <div class="container header-content">
      <div class="logo-area">
        <img src="@/assets/logo.svg" alt="BirdTag Logo" class="logo">
        <h1>BirdTag</h1>
      </div>
      <nav v-if="authStore.isAuthenticated">
        <span>{{ authStore.user?.email }}</span>
        <button @click="handleLogout">退出登录</button>
      </nav>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();

function handleLogout() {
  authStore.logout();
}
</script>

<style scoped>
header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  padding: 1rem 0;
  position: sticky;
  top: 0;
  z-index: 10;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-area {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  height: 30px;
}

h1 {
  font-size: 1.5rem;
}

nav {
  display: flex;
  align-items: center;
  gap: 1rem;
}

nav span {
  color: #555;
}
</style>
