import api from "@/api/api"

export const eventService = {
  async create(event) {
    const response = await api.post(
      "/events/",
      event,
    )

    return response.data
  },
  async getEvents() {
    const response = await api.get("/events")

    return response.data
  },

  async getById(id) {
    const response = await api.get(
      `/events/${id}`,
    )

    return response.data
  },

  async update(id, event) {
    const response = await api.patch(
      `/events/${id}`,
      event,
    )

    return response.data
  },

  async delete(id) {
    await api.delete(`/events/${id}`)
  },
}

export default eventService