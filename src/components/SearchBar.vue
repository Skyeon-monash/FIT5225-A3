<template>
  <form class="search-bar" @submit.prevent="performSearch">
    <input type="text" v-model="searchTerm" placeholder="按鸟类名称搜索 (例如: crow, owl)..." />
    <button type="submit">搜索</button>
  </form>
</template>

<script setup>
import { ref } from 'vue';
const searchTerm = ref('');
const emit = defineEmits(['search']);

function performSearch() {
  emit('search', searchTerm.value);
}
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 10px;
  margin-bottom: 2rem;
}

.search-bar input {
  flex-grow: 1;
  padding: 12px 15px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
}
</style>
