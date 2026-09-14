import api from "@/api/api"

export const notificationService = {
  async list(params = {}) {
    const response = await api.get("/notifications/", { params })
    return response.data
  },

  async count() {
    const response = await api.get("/notifications/count")
    return response.data
  },

  async sync() {
    const response = await api.post("/notifications/sync")
    return response.data
  },

  async markAsRead(id) {
    const response = await api.patch(`/notifications/${id}/read`)
    return response.data
  },

  async markAsUnread(id) {
    const response = await api.patch(`/notifications/${id}/unread`)
    return response.data
  },

  async markAllAsRead() {
    const response = await api.patch("/notifications/read-all")
    return response.data
  },

  async archive(id) {
    await api.delete(`/notifications/${id}`)
  },
}

export default notificationService
