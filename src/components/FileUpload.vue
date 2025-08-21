<template>
  <div class="upload-wrapper">
    <!-- Drop Zone Area -->
    <div class="drop-zone" :class="{ 'is-dragover': isDragover }" @dragover.prevent.stop="isDragover = true"
      @dragleave.prevent.stop="isDragover = false" @drop.prevent.stop="handleDrop" @click="triggerFileInput">
      <!-- Hidden File Input -->
      <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*,video/*" hidden />

      <!-- State: No File Selected -->
      <div v-if="!selectedFile" class="initial-state">
        <p>将文件拖拽至此</p>
        <p class="separator">或</p>
        <button type="button" class="browse-btn">选择文件</button>
      </div>

      <!-- State: File Selected, Ready for Upload -->
      <div v-else-if="!isUploading" class="preview-state">
        <img v-if="filePreviewUrl" :src="filePreviewUrl" class="file-preview" alt="Preview" />
        <div class="file-info">
          <strong>{{ selectedFile.name }}</strong>
          <span>({{ (selectedFile.size / 1024).toFixed(2) }} KB)</span>
        </div>
        <div class="actions">
          <button @click.stop="handleUpload" class="upload-btn">开始上传</button>
          <button @click.stop="clearFile" class="clear-btn">取消</button>
        </div>
      </div>

      <!-- State: Uploading -->
      <div v-else class="uploading-state">
        <p>正在上传...</p>
        <div class="progress-bar">
          <div class="progress" :style="{ width: uploadProgress + '%' }"></div>
        </div>
        <span>{{ uploadProgress }}%</span>
      </div>

    </div>

    <!-- State: Upload Status Message -->
    <p v-if="uploadStatus" :class="`status-message ${uploadStatus.type}`">{{ uploadStatus.message }}</p>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue';
import { apiService } from '@/services/apiService'; // ❗️ 1. 导入我们的真实 API 服务

const fileInput = ref(null);
const selectedFile = ref(null);
const filePreviewUrl = ref(null);
const isDragover = ref(false);
const isUploading = ref(false);
const uploadProgress = ref(0);
const uploadStatus = ref(null);

const emit = defineEmits(['upload-complete']);

// --- File Handling ---
function triggerFileInput() {
  fileInput.value.click();
}

function handleFileChange(event) {
  processFile(event.target.files[0]);
}

function handleDrop(event) {
  isDragover.value = false;
  processFile(event.dataTransfer.files[0]);
}

function processFile(file) {
  if (!file) return;
  selectedFile.value = file;
  uploadStatus.value = null;
  if (file.type.startsWith('image/')) {
    filePreviewUrl.value = URL.createObjectURL(file);
  } else {
    filePreviewUrl.value = null; // 非图片文件不预览
  }
}
function clearFile() {
  selectedFile.value = null;
  if (filePreviewUrl.value) {
    URL.revokeObjectURL(filePreviewUrl.value);
    filePreviewUrl.value = null;
  }
}

// --- Upload Logic ---
// --- ❗️❗️❗️ 升级后的真实上传逻辑 ❗️❗️❗️ ---
async function handleUpload() {
  if (!selectedFile.value) return;

  isUploading.value = true;
  uploadProgress.value = 0;
  uploadStatus.value = null;

  try {
    // 2. 调用 apiService 获取真实的预签名 URL
    const { uploadUrl, fileId } = await apiService.getPresignedUploadUrl(
      selectedFile.value.name,
      selectedFile.value.type
    );

    console.log(`[FileUpload] 获取到上传地址: ${uploadUrl}, 文件ID: ${fileId}`);

    // 3. 调用 apiService 将文件上传到 OSS，并传入一个更新进度的回调函数
    await apiService.uploadFileToOSS(uploadUrl, selectedFile.value, (progress) => {
      uploadProgress.value = progress;
    });

    // 4. 上传成功
    uploadStatus.value = { type: 'success', message: '上传成功！文件正在后台进行智能分析...' };
    emit('upload-complete');

  } catch (error) {
    console.error("[FileUpload] 上传流程失败:", error);
    uploadStatus.value = { type: 'error', message: error.message || '上传失败，请重试。' };
  } finally {
    isUploading.value = false;
    // 为了更好的用户体验，成功后延迟一会再清空
    setTimeout(() => {
      clearFile();
      // 只有成功时才清除成功消息，保留错误消息给用户看
      if (uploadStatus.value?.type === 'success') {
        uploadStatus.value = null;
      }
    }, 3000);
  }
}

// Cleanup the object URL to prevent memory leaks
onUnmounted(() => {
  if (filePreviewUrl.value) {
    URL.revokeObjectURL(filePreviewUrl.value);
  }
});
</script>

<style scoped>
/* Main Styles */
.upload-wrapper {
  width: 100%;
  margin-bottom: 2rem;
}

.drop-zone {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 200px;
  padding: 2rem;
  border: 2px dashed #d1d5db;
  border-radius: 12px;
  background-color: #f9fafb;
  color: #6b7280;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s;
}

.drop-zone:hover,
.drop-zone.is-dragover {
  border-color: #42b983;
  background-color: #f0fdf4;
}

/* States */
.initial-state {
  text-align: center;
}

.separator {
  margin: 0.5rem 0;
  font-size: 0.9rem;
}

.browse-btn {
  background-color: #fff;
  color: #42b983;
  border: 1px solid #42b983;
  padding: 8px 20px;
}

.preview-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.file-preview {
  max-height: 100px;
  border-radius: 8px;
}

.file-info {
  text-align: center;
  color: #374151;
}

.file-info span {
  font-size: 0.8rem;
  color: #6b7280;
}

.actions {
  display: flex;
  gap: 1rem;
}

.upload-btn {
  background-color: #42b983;
  color: white;
  border: none;
}

.clear-btn {
  background-color: #ef4444;
  color: white;
  border: none;
}

.uploading-state {
  text-align: center;
  width: 80%;
}

.progress-bar {
  width: 100%;
  background-color: #e5e7eb;
  border-radius: 99px;
  height: 10px;
  margin: 1rem 0;
}

.progress {
  height: 100%;
  background-color: #42b983;
  border-radius: 99px;
  transition: width 0.1s;
}

/* Status Message */
.status-message {
  text-align: center;
  margin-top: 1rem;
  padding: 10px;
  border-radius: 8px;
}

.status-message.success {
  background-color: #dcfce7;
  color: #166534;
}

.status-message.error {
  background-color: #fee2e2;
  color: #991b1b;
}
</style>
