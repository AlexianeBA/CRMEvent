import { defineStore } from "pinia"
import api from "@/api/api"

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null,
    loading: false,
    initialized: false,
  }),

  getters: {
    isAuthenticated: (state) => Boolean(state.user),
    isAdmin: (state) => state.user?.role === "admin",
    canManageCrm: (state) => ["admin", "manager", "commercial"].includes(state.user?.role),
    canDeleteCrm: (state) => ["admin", "manager"].includes(state.user?.role),
    canManageInvoices: (state) => ["admin", "manager", "comptable"].includes(state.user?.role),
  },

  actions: {
    async login(email, password) {
      const formData = new URLSearchParams()
      formData.append("username", email)
      formData.append("password", password)

      const response = await api.post("/auth/login", formData)
      localStorage.setItem("token", response.data.access_token)
      await this.fetchMe()
    },

    async fetchMe() {
      const token = localStorage.getItem("token")
      if (!token) {
        this.user = null
        this.initialized = true
        return null
      }

      this.loading = true
      try {
        const response = await api.get("/auth/me")
        this.user = response.data
        return this.user
      } catch (error) {
        this.logout(false)
        throw error
      } finally {
        this.loading = false
        this.initialized = true
      }
    },

    logout(redirect = true) {
      localStorage.removeItem("token")
      this.user = null
      this.initialized = true
      if (redirect && window.location.pathname !== "/login") {
        window.location.assign("/login")
      }
    },
  },
})
