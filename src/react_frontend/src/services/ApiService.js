import axios from 'axios'

const ApiService = {
  client: axios.create({
    baseURL: 'http://localhost:80',
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),

  authors: () => {
    return ApiService.client.get('/authors')
  },

  top_authors: () => {
    return ApiService.client.get('/top_authors')
  },

  addHashtag: (hashtag) => {
    return ApiService.client.post('/hashtag', { hashtag })
  },

  getActiveHashtags: () => {
    return ApiService.client.get('/hashtags')
  },

  getTopPosts: (params) => {
    return ApiService.client.get('/posts', { params })
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
