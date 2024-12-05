import axios from 'axios';

const ApiService = {
  client: axios.create({
    // Automatically detect base URL
    baseURL: `${window.location.origin}/api`,
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),

  top_authors: () => {
    return ApiService.client.get('/top_authors');
  },

  addHashtag: (hashtag) => {
    return ApiService.client.post('/hashtag', { hashtag });
  },

  getActiveHashtags: () => {
    return ApiService.client.get('/hashtags');
  },

  getTopPosts: (params) => {
    return ApiService.client.get('/posts', { params });
  },

  getPlatformGrowth: (params) => {
    return ApiService.client.get('/stats/growth', { params });
  },

  getStats: () => {
    return ApiService.client.get('/stats');
  },

  getTopAuthors: (params) => {
    return ApiService.client.get('/authors', { params });
  },
};

// Add a request interceptor
ApiService.client.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

export default ApiService;
