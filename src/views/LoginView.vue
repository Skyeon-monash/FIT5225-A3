<template>
  <div class="auth-page">
    <div class="form-container">
      <div class="form-header">
        <img src="@/assets/logo.svg" alt="BirdTag Logo" class="logo">
        <h2>{{ isLoginMode ? '欢迎回来' : '创建新账户' }}</h2>
        <p>{{ isLoginMode ? '登录以继续' : '加入 BirdTag 社区' }}</p>
      </div>

      <form @submit.prevent="handleSubmit">
        <div class="input-group">
          <input type="email" v-model="email" placeholder="邮箱地址" required />
        </div>
        <div class="input-group">
          <input type="password" v-model="password" placeholder="密码" required />
        </div>
        <div v-if="!isLoginMode" class="input-group">
          <input type="password" v-model="confirmPassword" placeholder="确认密码" required />
        </div>

        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>

        <button type="submit" :disabled="isLoading">
          <span v-if="isLoading">处理中...</span>
          <span v-else>{{ isLoginMode ? '登录' : '注册' }}</span>
        </button>
      </form>

      <div class="form-footer">
        <p>
          {{ isLoginMode ? '还没有账户？' : '已经有账户了？' }}
          <a href="#" @click.prevent="toggleMode">{{ isLoginMode ? '立即注册' : '点击登录' }}</a>
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const isLoginMode = ref(true);
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const errorMessage = ref(null);
const isLoading = ref(false);

const router = useRouter();
const authStore = useAuthStore();

function toggleMode() {
  isLoginMode.value = !isLoginMode.value;
  errorMessage.value = null;
}

async function handleSubmit() {
  errorMessage.value = null;
  isLoading.value = true;

  if (!isLoginMode.value && password.value !== confirmPassword.value) {
    errorMessage.value = '两次输入的密码不一致！';
    isLoading.value = false;
    return;
  }

  try {
    if (isLoginMode.value) {
      await authStore.login(email.value, password.value);
    } else {
      await authStore.signup(email.value, password.value);
    }
    router.push('/dashboard');
  } catch (error) {
    // 处理 Firebase 返回的错误
    switch (error.code) {
      case 'auth/invalid-email':
        errorMessage.value = '无效的邮箱格式。';
        break;
      case 'auth/user-not-found':
      case 'auth/wrong-password':
        errorMessage.value = '邮箱或密码错误。';
        break;
      case 'auth/email-already-in-use':
        errorMessage.value = '该邮箱已被注册。';
        break;
      case 'auth/weak-password':
        errorMessage.value = '密码太弱，至少需要6位字符。';
        break;
      default:
        errorMessage.value = '发生未知错误，请稍后再试。';
    }
    console.error("Authentication error:", error);
  } finally {
    isLoading.value = false;
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.form-container {
  width: 100%;
  max-width: 400px;
  padding: 40px;
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.form-header .logo {
  width: 60px;
  margin-bottom: 20px;
}

.form-header h2 {
  font-size: 24px;
  margin-bottom: 8px;
  color: #333;
}

.form-header p {
  color: #666;
  margin-bottom: 30px;
}

.input-group {
  margin-bottom: 20px;
  position: relative;
}

.input-group input {
  width: 100%;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s;
}

.input-group input:focus {
  outline: none;
  border-color: #42b983;
}

.error-message {
  color: #e74c3c;
  margin-bottom: 15px;
  font-size: 14px;
}

button {
  width: 100%;
  padding: 12px;
  border: none;
  border-radius: 8px;
  font-size: 16px;
  font-weight: bold;
}

.form-footer {
  margin-top: 25px;
  font-size: 14px;
  color: #666;
}

.form-footer a {
  color: #42b983;
  text-decoration: none;
  font-weight: bold;
}

.form-footer a:hover {
  text-decoration: underline;
}
</style>
