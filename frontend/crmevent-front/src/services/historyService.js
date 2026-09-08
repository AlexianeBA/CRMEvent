import api from "@/api/api"

export const historyService = {
  async getHistory(params) {
    const response = await api.get("/history/", { params })
    return response.data
  },
}

export default historyService
