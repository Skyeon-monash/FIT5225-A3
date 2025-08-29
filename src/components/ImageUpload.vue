<template>
  <div class="upload-area">
    <h3>上传新的媒体文件</h3>
    <input type="file" @change="onFileSelected" accept="image/*,video/*">
    <button @click="onUpload" :disabled="!selectedFile || isUploading">
      {{ isUploading ? '上传中...' : '开始上传' }}
    </button>
    <div v-if="uploadProgress > 0 && uploadProgress < 100">
      进度: {{ uploadProgress.toFixed(2) }}%
    </div>
    <div v-if="uploadSuccess">上传成功！</div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const selectedFile = ref(null);
const isUploading = ref(false);
const uploadProgress = ref(0);
const uploadSuccess = ref(false);

function onFileSelected(event) {
  selectedFile.value = event.target.files[0];
  uploadSuccess.value = false;
  uploadProgress.value = 0;
}

async function onUpload() {
  if (!selectedFile.value) return;

  isUploading.value = true;
  uploadSuccess.value = false;

  // --- 关键上传逻辑 ---
  // 1. 从我们的后端获取一个预签名的 OSS 上传 URL
  // const response = await apiService.getPresignedUploadUrl(selectedFile.value.name, selectedFile.value.type);
  // const presignedUrl = response.data.url;

  // --- 模拟阶段 ---
  console.log('模拟：从后端获取到上传地址...');
  const presignedUrl = 'https://mock-oss-bucket.oss-cn-hangzhou.aliyuncs.com/mock-upload-path';

  // 2. 使用 fetch 或 axios 直接将文件 PUT 到获取到的 URL
  // 注意：这里需要处理 XMLHttpRequest 来获取上传进度
  // 为了简化，我们用一个 setTimeout 模拟上传过程
  console.log(`模拟：将文件 ${selectedFile.value.name} 上传到 OSS...`);
  const simulateUpload = new Promise(resolve => {
    let progress = 0;
    const interval = setInterval(() => {
      progress += 10;
      uploadProgress.value = progress;
      if (progress >= 100) {
        clearInterval(interval);
        resolve();
      }
    }, 200);
  });

  await simulateUpload;

  console.log('模拟：上传完成!');
  isUploading.value = false;
  uploadSuccess.value = true;
  selectedFile.value = null;

  // 可以在这里触发一个事件，通知父组件刷新图片列表
}
</script>
