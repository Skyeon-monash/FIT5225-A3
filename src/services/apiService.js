// src/services/apiService.js
import axios from 'axios'

// FastAPI 的地址
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const DEFAULT_CT = 'application/octet-stream'

// 与后端交互的 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { 'Content-Type': 'application/json' },
})

// 模拟数据（保留你现有逻辑，如不需要可删）
const mockDatabase = [
  {
    id: 'img_01',
    type: 'image',
    thumbnailUrl: 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=400',
    fullUrl: 'https://images.unsplash.com/photo-1552728089-57bdde30beb3?w=1200',
    tags: { crow: 2 },
    description: '两只乌鸦栖息在树枝上。',
  },
  {
    id: 'img_02',
    type: 'image',
    thumbnailUrl: 'https://images.unsplash.com/photo-1516233758811-9f9675458428?w=400',
    fullUrl: 'https://images.unsplash.com/photo-1516233758811-9f9675458428?w=1200',
    tags: { kingfisher: 1 },
    description: '一只翠鸟正准备捕鱼。',
  },
]

const simulateNetwork = (delay = 800) => new Promise((res) => setTimeout(res, delay))

export const apiService = {
  // 保留模拟接口
  async searchMedia(searchTerm = '') {
    await simulateNetwork()
    if (searchTerm) {
      const s = searchTerm.toLowerCase()
      return mockDatabase.filter((item) =>
        Object.keys(item.tags).some((t) => t.includes(s)),
      )
    }
    return mockDatabase
  },

  async getMediaDetails(id) {
    await simulateNetwork(500)
    const item = mockDatabase.find((it) => it.id === id)
    if (item) return item
    throw new Error('Media not found')
  },

  // ====== 真正获取预签名 URL（调用 FastAPI） ======
  async getPresignedUploadUrl(fileName, fileType) {
    const contentType = fileType || DEFAULT_CT
    try {
      const { data } = await apiClient.post('/presign', { fileName, contentType })
      // data: { uploadUrl, key, getUrl, contentType, viaSTS }
      return data
    } catch (err) {
      const msg = err?.response?.data?.detail || err?.message || '获取预签名地址失败'
      throw new Error(msg)
    }
  },

  // ====== 直传到 OSS（PUT 预签名 URL） ======
  async uploadFileToOSS(uploadUrl, file, onProgress, forcedContentType) {
    const ct = forcedContentType || (file && file.type) || DEFAULT_CT
    return axios.put(uploadUrl, file, {
      headers: { 'Content-Type': ct },
      onUploadProgress: (e) => {
        if (e.total && typeof onProgress === 'function') {
          onProgress(Math.round((e.loaded * 100) / e.total))
        }
      },
    })
  },

  // 保留
  async deleteMedia(id) {
    await simulateNetwork()
    return { success: true }
  },
}
