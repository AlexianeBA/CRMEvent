import api from "@/api/api"

export const searchService = {
  async search(query, limit = 5) {
    const response = await api.get("/search/", { params: { q: query, limit } })
    return response.data.results
  },
}

export default searchService
