import axios from 'axios'

const AuthService = {
  client: axios.create({
    baseURL: 'http://localhost:80',
    timeout: 1000,
    headers: {
      'Content-Type': 'application/json',
    },
  }),

  register: (username, email, password) => {
    return AuthService.client.post('/register', {
      username,
      email,
      password,
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
