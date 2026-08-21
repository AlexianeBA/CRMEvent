import api from "@/api/api"

export const opportunityService = {
  async getOpportunities() {
    const response = await api.get(
      "/opportunities",
      {
        params: {
          limit: 100,
        },
      },
    )

    return response.data
  },

  async getById(id) {
    const response = await api.get(`/opportunities/${id}`)
    return response.data
  },

  async create(opportunity) {
    const response = await api.post("/opportunities/", opportunity)
    return response.data
  },

  async update(id, opportunity) {
    const response = await api.patch(`/opportunities/${id}`, opportunity)
    return response.data
  },

  async updateStatus(id, status) {
    const response = await api.patch(
      `/opportunities/${id}/status`,
      null,
      { params: { status } },
    )
    return response.data
  },

  async delete(id) {
    await api.delete(`/opportunities/${id}`)
  },
}

export default opportunityService
