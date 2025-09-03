import { create } from 'zustand'
import axios from 'axios'

type AuthState = {
  loggedIn: boolean
  login: (email: string, password: string) => Promise<boolean>
  logout: () => Promise<void>
}

export const useAuth = create<AuthState>((set) => ({
  loggedIn: false,
  async login(email, password) {
    try {
      await axios.post(import.meta.env.VITE_API_BASE + '/auth/login', { email, password }, { withCredentials: true })
      set({ loggedIn: true })
      return true
    } catch (e) {
      return false
    }
  },
  async logout() {
    await axios.post(import.meta.env.VITE_API_BASE + '/auth/logout', {}, { withCredentials: true })
    set({ loggedIn: false })
  }
}))
