// src/firebase.js
import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'

// ❗️❗️❗️ 将这里替换成你自己的 Firebase 项目配置 ❗️❗️❗️
const firebaseConfig = {
  apiKey: 'AIzaSyCO8dyRLxbpj21BfYfMiUvHRTgBxwIatr0',
  authDomain: 'final-project-c99e6.firebaseapp.com',
  projectId: 'final-project-c99e6',
  storageBucket: 'final-project-c99e6.firebasestorage.app',
  messagingSenderId: '801034452476',
  appId: '1:801034452476:web:03c220d3098f8dec3bc679',
}

// 初始化 Firebase
const app = initializeApp(firebaseConfig)

// 导出我们需要的 Firebase 服务
// 我们在这里只需要 auth 服务
export const auth = getAuth(app)
