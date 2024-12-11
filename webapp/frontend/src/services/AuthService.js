import axios from 'axios'

const AuthService = {
  client: axios.create({
    // Automatically determine base URL dynamically
    baseURL: `${window.location.origin}/api`,
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),

  register: (username, email, password, roles) => {
    return AuthService.client.post('/register', {
      username,
      email,
      password,
      roles,
    })
  },

  login: (username, password) => {
    return AuthService.client.post('/login', {
      username,
      password,
    })
  },
}

export default AuthService
