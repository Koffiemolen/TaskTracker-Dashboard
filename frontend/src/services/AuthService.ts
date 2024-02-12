// src/services/AuthService.ts
import axios from 'axios'

const API_URL = 'http://127.0.0.1:8000/users/login' // Adjust this URL to your backend endpoint

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
    if (response.data.accessToken) {
      localStorage.setItem('user', JSON.stringify(response.data))
    }
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
