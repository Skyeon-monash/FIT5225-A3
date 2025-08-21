<template>
  <div class="media-card" @click="$emit('open')">
    <div class="image-container">
      <img :src="item.thumbnailUrl" :alt="altText" loading="lazy">
      <div v-if="item.type === 'video'" class="play-icon">▶</div>
    </div>
    <div class="card-footer">
      <span v-for="(count, name) in item.tags" :key="name" class="tag">
        {{ name }}: {{ count }}
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
const props = defineProps({
  item: { type: Object, required: true }
});
const altText = computed(() => Object.keys(props.item.tags).join(', '));
defineEmits(['open']);
</script>

<style scoped>
.media-card {
  cursor: pointer;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  overflow: hidden;
  transition: transform 0.2s, box-shadow 0.2s;
}

.media-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

.image-container {
  position: relative;
  aspect-ratio: 1 / 1;
}

img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-icon {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  font-size: 40px;
  color: white;
  text-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
}

.card-footer {
  padding: 15px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  background-color: #eef7f4;
  color: #42b983;
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}
</style>
