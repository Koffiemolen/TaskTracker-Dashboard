import { defineStore } from 'pinia'
import AuthService from '../services/AuthService'

export const useUserStore = defineStore('user', {
  state: () => ({
    user: null
  }),
  actions: {
    async login (username: string, password: string) {
      const user = await AuthService.login(username, password)
      this.user = user
      return user
    },
    logout () {
      AuthService.logout()
      this.user = null
    }
  },
  getters: {
    isLoggedIn: (state) => !!state.user
  }
})
