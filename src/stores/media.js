// src/stores/media.js
import { defineStore } from 'pinia'
import { ref } from 'vue'
import { apiService } from '@/services/apiService' // 导入新的服务

export const useMediaStore = defineStore('media', () => {
  const mediaList = ref([])
  const selectedMediaItem = ref(null) // 用于模态窗口的数据
  const isLoading = ref(false)
  const isDetailLoading = ref(false)
  const error = ref(null)

  async function fetchMedia(searchTerm = '') {
    isLoading.value = true
    error.value = null
    try {
      // 调用真正的 API 服务
      mediaList.value = await apiService.searchMedia(searchTerm)
    } catch (e) {
      error.value = '加载媒体文件失败。'
      console.error(e)
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMediaDetails(id) {
    isDetailLoading.value = true
    try {
      selectedMediaItem.value = await apiService.getMediaDetails(id)
    } catch (e) {
      console.error(e)
      // 可以选择关闭模态窗或显示错误信息
      closeModal()
    } finally {
      isDetailLoading.value = false
    }
  }

  function openModalWithId(id) {
    fetchMediaDetails(id)
  }

  function closeModal() {
    selectedMediaItem.value = null
  }

  return {
    mediaList,
    selectedMediaItem,
    isLoading,
    isDetailLoading,
    error,
    fetchMedia,
    openModalWithId,
    closeModal,
  }
})
