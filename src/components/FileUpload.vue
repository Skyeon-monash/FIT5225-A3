<template>
  <div class="upload-wrapper">
    <div
      class="drop-zone"
      :class="{ 'is-dragover': isDragover }"
      @dragover.prevent.stop="isDragover = true"
      @dragleave.prevent.stop="isDragover = false"
      @drop.prevent.stop="handleDrop"
      @click="triggerFileInput"
    >
      <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*,video/*" hidden />

      <div v-if="!selectedFile" class="initial-state">
        <p>将文件拖拽至此</p>
        <p class="separator">或</p>
        <button type="button" class="browse-btn">选择文件</button>
      </div>

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

      <div v-else class="uploading-state">
        <p>正在上传...</p>
        <div class="progress-bar">
          <div class="progress" :style="{ width: uploadProgress + '%' }"></div>
        </div>
        <span>{{ uploadProgress }}%</span>
      </div>
    </div>

    <p v-if="uploadStatus" :class="`status-message ${uploadStatus.type}`">
      {{ uploadStatus.message }}
      <template v-if="uploadStatus.type === 'success' && previewUrl">
        <a :href="previewUrl" target="_blank" style="margin-left:8px;">预览文件</a>
      </template>
    </p>
  </div>
</template>

<script setup>
import { ref, onUnmounted } from 'vue'
import { apiService } from '@/services/apiService'

const fileInput = ref(null)
const selectedFile = ref(null)
const filePreviewUrl = ref(null)
const isDragover = ref(false)
const isUploading = ref(false)
const uploadProgress = ref(0)
const uploadStatus = ref(null)
const previewUrl = ref('') // 新增：上传成功后的短期可访问链接

const emit = defineEmits(['upload-complete'])

function triggerFileInput() {
  fileInput.value.click()
}
function handleFileChange(e) {
  processFile(e.target.files[0])
}
function handleDrop(e) {
  isDragover.value = false
  processFile(e.dataTransfer.files[0])
}
function processFile(file) {
  if (!file) return
  selectedFile.value = file
  uploadStatus.value = null
  previewUrl.value = ''
  if (file.type?.startsWith('image/')) {
    filePreviewUrl.value = URL.createObjectURL(file)
  } else {
    filePreviewUrl.value = null
  }
}
function clearFile() {
  selectedFile.value = null
  if (filePreviewUrl.value) {
    URL.revokeObjectURL(filePreviewUrl.value)
    filePreviewUrl.value = null
  }
}

// ---- 上传主流程 ----
async function handleUpload() {
  if (!selectedFile.value) return

  isUploading.value = true
  uploadProgress.value = 0
  uploadStatus.value = null

  try {
    // 1) 向 FastAPI 请求预签名 URL
    const presign = await apiService.getPresignedUploadUrl(
      selectedFile.value.name,
      selectedFile.value.type
    )
    // presign: { uploadUrl, key, getUrl, contentType, viaSTS }
    const { uploadUrl, getUrl, contentType } = presign

    // 2) PUT 直传到 OSS，Content-Type 必须与签名一致
    await apiService.uploadFileToOSS(uploadUrl, selectedFile.value, (p) => {
      uploadProgress.value = p
    }, contentType)

    // 3) 成功
    previewUrl.value = getUrl || ''
    uploadStatus.value = { type: 'success', message: '上传成功！文件正在后台进行智能分析...' }
    emit('upload-complete')
  } catch (err) {
    console.error('[FileUpload] 上传流程失败:', err)
    uploadStatus.value = { type: 'error', message: err.message || '上传失败，请重试。' }
  } finally {
    isUploading.value = false
    setTimeout(() => {
      clearFile()
      if (uploadStatus.value?.type === 'success') uploadStatus.value = null
    }, 3000)
  }
}

onUnmounted(() => {
  if (filePreviewUrl.value) URL.revokeObjectURL(filePreviewUrl.value)
})
</script>

<style scoped>
/* 保留你的样式 */
.upload-wrapper { width: 100%; margin-bottom: 2rem; }
.drop-zone { display:flex; flex-direction:column; justify-content:center; align-items:center;
  min-height:200px; padding:2rem; border:2px dashed #d1d5db; border-radius:12px; background:#f9fafb;
  color:#6b7280; cursor:pointer; transition:background-color .2s,border-color .2s; }
.drop-zone:hover,.drop-zone.is-dragover{ border-color:#42b983; background:#f0fdf4; }
.initial-state{text-align:center;} .separator{margin:.5rem 0;font-size:.9rem;}
.browse-btn{ background:#fff; color:#42b983; border:1px solid #42b983; padding:8px 20px; }
.preview-state{ display:flex; flex-direction:column; align-items:center; gap:1rem; }
.file-preview{ max-height:100px; border-radius:8px; }
.file-info{text-align:center; color:#374151;} .file-info span{ font-size:.8rem; color:#6b7280; }
.actions{ display:flex; gap:1rem; }
.upload-btn{ background:#42b983; color:#fff; border:none; }
.clear-btn{ background:#ef4444; color:#fff; border:none; }
.uploading-state{text-align:center; width:80%;}
.progress-bar{ width:100%; background:#e5e7eb; border-radius:99px; height:10px; margin:1rem 0; }
.progress{ height:100%; background:#42b983; border-radius:99px; transition:width .1s; }
.status-message{ text-align:center; margin-top:1rem; padding:10px; border-radius:8px; }
.status-message.success{ background:#dcfce7; color:#166534; }
.status-message.error{ background:#fee2e2; color:#991b1b; }
</style>
