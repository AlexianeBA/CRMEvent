import api from "@/api/api"

export const adminService = {
  async getUsers() {
    const response = await api.get("/auth/users/list")
    return response.data
  },

  async createUser(user) {
    const response = await api.post("/auth/users", user)
    return response.data
  },

  async updateUser(id, changes) {
    const response = await api.patch(`/auth/users/${id}`, changes)
    return response.data
  },

  async resetPassword(id, password) {
    await api.post(`/auth/users/${id}/reset-password`, { password })
  },
}

export default adminService
