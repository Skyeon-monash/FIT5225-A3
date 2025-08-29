// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { auth } from '@/firebase' // 导入我们配置好的 auth
import {
  createUserWithEmailAndPassword,
  signInWithEmailAndPassword,
  signOut,
  onAuthStateChanged, // 这是一个非常重要的监听器！
} from 'firebase/auth'
import { useRouter } from 'vue-router'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const router = useRouter()
  const loading = ref(true) // 添加一个加载状态

  // 监听 Firebase 的认证状态变化
  // 这是保持用户登录状态持久化的关键
  function init() {
    onAuthStateChanged(auth, (firebaseUser) => {
      if (firebaseUser) {
        // 用户已登录
        user.value = {
          uid: firebaseUser.uid,
          email: firebaseUser.email,
        }
      } else {
        // 用户未登录
        user.value = null
      }
      loading.value = false // 监听器设置完毕，加载完成
    })
  }

  const isAuthenticated = computed(() => !!user.value)

  async function signup(email, password) {
    loading.value = true
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password)
      user.value = { uid: userCredential.user.uid, email: userCredential.user.email }
    } finally {
      loading.value = false
    }
  }

  async function login(email, password) {
    loading.value = true
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password)
      user.value = { uid: userCredential.user.uid, email: userCredential.user.email }
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    loading.value = true
    try {
      await signOut(auth)
      user.value = null
      router.push('/login') // 登出后跳转到登录页
    } finally {
      loading.value = false
    }
  }

  return { user, loading, isAuthenticated, init, signup, login, logout }
})
