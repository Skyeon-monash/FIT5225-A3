<template>
  <div class="modal-backdrop" @click="mediaStore.closeModal">
    <div class="modal-content" @click.stop>
      <button class="close-btn" @click="mediaStore.closeModal">&times;</button>

      <div v-if="mediaStore.isDetailLoading" class="loading">加载中...</div>

      <div v-if="item" class="details-grid">
        <div class="media-viewer">
          <img v-if="item.type === 'image'" :src="item.fullUrl" :alt="item.description">
          <video v-else-if="item.type === 'video'" :src="item.fullUrl" controls autoplay muted loop>
            抱歉，您的浏览器不支持视频播放。
          </video>
        </div>
        <div class="info-panel">
          <h3>详细信息</h3>
          <p class="description">{{ item.description }}</p>
          <h4>识别出的鸟类</h4>
          <div class="tags">
            <span v-for="(count, name) in item.tags" :key="name" class="tag">
              {{ name }}: <strong>{{ count }}</strong> 只
            </span>
          </div>
          <div class="actions">
            <button class="delete-btn">删除文件</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useMediaStore } from '@/stores/media';

const mediaStore = useMediaStore();
const item = computed(() => mediaStore.selectedMediaItem);
</script>

<style scoped>
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 100;
}

.modal-content {
  width: 90%;
  max-width: 1000px;
  max-height: 90vh;
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  position: relative;
  overflow: hidden;
}

.close-btn {
  position: absolute;
  top: 15px;
  right: 20px;
  background: none;
  border: none;
  font-size: 2.5rem;
  color: #666;
  cursor: pointer;
  z-index: 10;
}

.loading {
  padding: 5rem;
  text-align: center;
}

.details-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  height: 90vh;
  max-height: 700px;
  /* Or some fixed height */
}

.media-viewer {
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.media-viewer img,
.media-viewer video {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}

.info-panel {
  padding: 2rem;
  overflow-y: auto;
}

.info-panel h3 {
  margin-bottom: 1rem;
}

.description {
  margin-bottom: 2rem;
  color: #555;
}

.info-panel h4 {
  margin-bottom: 1rem;
  color: #333;
}

.tags {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
  margin-bottom: 2rem;
}

.tag {
  background-color: #f0fdf4;
  padding: 10px;
  border-radius: 8px;
}

.delete-btn {
  background-color: #fee2e2;
  color: #b91c1c;
  border: none;
  width: 100%;
}
</style>
