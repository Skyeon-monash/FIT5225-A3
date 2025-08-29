<template>
  <div id="app-wrapper">
    <RouterView />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { RouterView } from 'vue-router';
import { useAuthStore } from './stores/auth';

const authStore = useAuthStore();

onMounted(() => {
  // 当应用挂载时，初始化 Firebase auth 状态监听器
  authStore.init();
});
</script>

<style>
/*
  在这里写全局 CSS 样式。
  这些样式会应用到整个项目的所有组件中。
  注意：这里的 <style> 标签没有 "scoped" 属性。
*/

/* 一个好的实践是进行 CSS Reset */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen,
    Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif;
  line-height: 1.6;
  background-color: #f9f9f9;
  color: #333;
}

#app-wrapper {
  /* 如果需要，可以设置整个应用的最大宽度等 */
  max-width: 1200px;
  margin: 0 auto;
}

button {
  cursor: pointer;
  padding: 8px 16px;
  border-radius: 4px;
  border: 1px solid #42b983;
  background-color: #42b983;
  color: white;
  font-size: 1rem;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #36a473;
}

button:disabled {
  background-color: #ccc;
  border-color: #ccc;
  cursor: not-allowed;
}
</style>
