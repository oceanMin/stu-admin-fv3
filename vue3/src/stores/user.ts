import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('token') || '',
    username: localStorage.getItem('username') || ''
  }),
  actions: {
    setUser(data) {
      this.token = data.token
      this.username = data.username
      localStorage.setItem('token', data.token)
      localStorage.setItem('username', data.username)
    },
    logout() {
      this.token = ''
      this.username = ''
      localStorage.clear()
    }
  }
})