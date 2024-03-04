// src/services/AuthService.ts
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/users/login'

class AuthService {
  async login (username: string, password: string) {
    const response = await axios.post(API_URL, {
      username,
      password
    }, {
      headers: {
        accept: 'application/json',
        'Content-Type': 'application/json'
      }
    })
    console.log('access_token:', response.data.access_token)
    console.log('accessToken:', response.data.accessToken)
    if (response.data.access_token) {
      localStorage.setItem('user', JSON.stringify(response.data))
    }
    console.log('Response:', response.data)
    return response.data
  }

  logout () {
    localStorage.removeItem('user')
  }

  getCurrentUser () {
    const user = localStorage.getItem('user')
    return user ? JSON.parse(user) : null
  }
}

export default new AuthService()
