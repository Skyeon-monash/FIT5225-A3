<template>
  <div class="dashboard">
    <AppHeader />
    <main class="main-content">
      <div class="container">

        <!-- 使用我们全新的上传组件 -->
        <FileUpload @upload-complete="handleUploadComplete" />

        <SearchBar @search="handleSearch" />

        <h2 class="gallery-title">媒体库</h2>

        <div v-if="mediaStore.isLoading" class="loading-state">
          <!-- 我们可以用一个更漂亮的加载动画 -->
          <p>正在加载媒体库...</p>
        </div>
        <div v-else-if="mediaStore.error" class="error-state">
          {{ mediaStore.error }}
        </div>
        <div v-else-if="mediaStore.mediaList.length === 0" class="empty-state">
          <h3>未找到任何媒体文件</h3>
          <p>尝试不同的搜索词或上传你的第一个文件。</p>
        </div>
        <div v-else class="media-gallery">
          <MediaCard v-for="item in mediaStore.mediaList" :key="item.id" :item="item"
            @open="mediaStore.openModalWithId(item.id)" />
        </div>
      </div>
    </main>
    <MediaDetailModal v-if="mediaStore.selectedMediaItem || mediaStore.isDetailLoading" />
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useMediaStore } from '@/stores/media';
import AppHeader from '@/components/AppHeader.vue';
import FileUpload from '@/components/FileUpload.vue'; // 导入新组件
import SearchBar from '@/components/SearchBar.vue';
import MediaCard from '@/components/MediaCard.vue';
import MediaDetailModal from '@/components/MediaDetailModal.vue';

const mediaStore = useMediaStore();

onMounted(() => {
  mediaStore.fetchMedia();
});

function handleSearch(searchTerm) {
  mediaStore.fetchMedia(searchTerm);
}

// 当上传完成后，这个函数会被调用
function handleUploadComplete() {
  console.log("Dashboard: 检测到上传完成，正在刷新媒体列表...");
  // 延迟一小段时间再刷新，给后端一点处理时间
  setTimeout(() => {
    mediaStore.fetchMedia();
  }, 1000); // 1秒后刷新
}
</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.main-content {
  flex-grow: 1;
  background-color: #f8f9fa;
  padding: 2rem 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 1rem;
}

/* 临时上传区域样式 */
.upload-section {
  padding: 2rem;
  border: 2px dashed #ddd;
  border-radius: 12px;
  text-align: center;
  margin-bottom: 2rem;
  background-color: #fff;
}

.upload-section h2 {
  margin-bottom: 0.5rem;
}

.upload-section p {
  color: #666;
}


.media-gallery {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 1.5rem;
}

.loading-state,
.error-state,
.empty-state {
  text-align: center;
  padding: 4rem;
  color: #666;
}

.error-state {
  color: #e74c3c;
}

.gallery-title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
  padding-bottom: 0.5rem;
}
</style>
