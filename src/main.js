// src/main.js

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router' // 路由器在 Pinia 之后使用，但导入顺序没关系

const app = createApp(App)

// 1. 先创建 Pinia 实例
const pinia = createPinia()

// 2. 将 Pinia 插件安装到应用上
app.use(pinia)

// 3. 再安装路由器插件
app.use(router)

app.mount('#app')
