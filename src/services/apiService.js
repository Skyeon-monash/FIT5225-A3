// src/services/apiService.js

import axios from 'axios'

// --- ❗️❗️❗️ 关键配置 ❗️❗️❗️ ---
// 将这里替换成你部署成功后，Serverless Devs 输出的 system_url
const API_BASE_URL = 'https://birdtag-backend-ezkuyfuwhm.cn-hongkong.fcapp.run'

// 创建一个 Axios 实例，用于与我们的后端 API 通信
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// --- 模拟数据部分 (暂时保留) ---
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
  // ... 其他模拟数据
]

const simulateNetwork = (delay = 800) => new Promise((res) => setTimeout(res, delay))

// --- 导出的 API 服务对象 ---
export const apiService = {
  // --- 媒体列表和详情 (暂时使用模拟数据) ---
  async searchMedia(searchTerm = '') {
    await simulateNetwork()
    console.log(`[API Service] (Mock) Searching for: "${searchTerm}"`)
    if (searchTerm) {
      const lowerCaseSearch = searchTerm.toLowerCase()
      return mockDatabase.filter((item) =>
        Object.keys(item.tags).some((tag) => tag.includes(lowerCaseSearch)),
      )
    }
    return mockDatabase
  },

  async getMediaDetails(id) {
    await simulateNetwork(500)
    console.log(`[API Service] (Mock) Fetching details for ID: ${id}`)
    const item = mockDatabase.find((item) => item.id === id)
    if (item) {
      return item
    }
    throw new Error('Media not found')
  },

  // --- 预签名 URL 获取 (❗️已升级为真实 API 调用❗️) ---
  async getPresignedUploadUrl(fileName, fileType) {
    console.log(`[API Service] (Real) Requesting upload URL for ${fileName}`);
    try {
      // apiClient 会自动将下面的 JS 对象转换成 JSON 字符串
      const response = await apiClient.post('/', {
        fileName: fileName,
        contentType: fileType,
      });
      return response.data;
    } catch (error) {
      console.error('Failed to get presigned URL from backend', error.response ? error.response.data : error.message);
      // ❗️ 改进错误提示，如果后端有返回错误信息，就显示出来
      const backendError = error.response ? error.response.data.error : null;
      throw new Error(backendError || '无法从服务器获取上传地址，请检查网络或联系管理员。');
    }
  },

  // --- 文件上传到 OSS (❗️新增的真实上传逻辑❗️) ---
  async uploadFileToOSS(uploadUrl, file, onProgress) {
    console.log(`[API Service] (Real) Uploading file to OSS...`)
    try {
      // 直接向 OSS 返回的预签名 URL 发送 PUT 请求
      const response = await axios.put(uploadUrl, file, {
        headers: {
          'Content-Type': file.type,
        },
        // Axios 的上传进度回调
        onUploadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
            onProgress(percentCompleted)
          }
        },
      })
      return response
    } catch (error) {
      console.error('Failed to upload file directly to OSS', error)
      throw new Error('文件上传至云存储失败，请重试。')
    }
  },

  // --- 删除媒体 (暂时保留模拟) ---
  async deleteMedia(id) {
    await simulateNetwork()
    console.log(`[API Service] (Mock) Deleting media with ID: ${id}`)
    return { success: true }
  },
}
