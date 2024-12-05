import axios from 'axios'

const ApiService = {
  client: axios.create({
    baseURL: 'http://localhost:8000',
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),

  top_authors: () => {
    return ApiService.client.get('/api/top_authors')
  },

  addHashtag: (hashtag) => {
    return ApiService.client.post('/api/hashtag', { hashtag })
  },

  getActiveHashtags: () => {
    return ApiService.client.get('/api/hashtags')
  },

  getTopPosts: (params) => {
    return ApiService.client.get('/api/posts', { params })
  },

  getPlatformGrowth: (params) => {
    return ApiService.client.get('/api/stats/growth', { params })
  },

  getStats: () => {
    return ApiService.client.get('/api/stats')
  },

  getTopAuthors: (params) => {
    return ApiService.client.get('/api/authors', { params })
  },
}

// Add a request interceptor
ApiService.client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

export default ApiService
