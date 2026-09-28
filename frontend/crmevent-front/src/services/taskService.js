import api from "@/api/api"

export const taskService = {
  async list(params = {}) {
    const response = await api.get("/tasks/", { params })
    return response.data
  },
  async getById(id) {
    const response = await api.get(`/tasks/${id}`)
    return response.data
  },
  async create(task) {
    const response = await api.post("/tasks/", task)
    return response.data
  },
  async update(id, task) {
    const response = await api.patch(`/tasks/${id}`, task)
    return response.data
  },
  async delete(id) {
    await api.delete(`/tasks/${id}`)
  },
}

export default taskService
