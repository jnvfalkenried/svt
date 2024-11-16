import axios from 'axios'

const ApiService = {
  client: axios.create({
    baseURL: 'http://localhost:80',
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),
}

// Add a request interceptor
ApiService.client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('jwtToken')
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
