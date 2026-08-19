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
}

export default opportunityService