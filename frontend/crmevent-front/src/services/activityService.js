import api from "@/api/api"

export const activityService = {
  async getByOpportunity(opportunityId) {
    const response = await api.get("/activities/", {
      params: { opportunity_id: opportunityId },
    })
    return response.data
  },

  async create(activity) {
    const response = await api.post("/activities/", activity)
    return response.data
  },

  async update(id, activity) {
    const response = await api.patch(`/activities/${id}`, activity)
    return response.data
  },

  async updateStatus(id, status, scheduledAt = null) {
    const response = await api.patch(`/activities/${id}/status`, null, {
      params: {
        status,
        ...(scheduledAt ? { scheduled_at: scheduledAt } : {}),
      },
    })
    return response.data
  },

  async sendEmail(id) {
    const response = await api.post(`/activities/${id}/send-email`)
    return response.data
  },

  async delete(id) {
    await api.delete(`/activities/${id}`)
  },
}

export default activityService
