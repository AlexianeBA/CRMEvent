import api from "@/api/api"

export const contactService = {
  async getContacts() {
    const response = await api.get("/contacts")

    return response.data
  },

  async create(contact) {
    const response = await api.post(
      "/contacts/",
      contact,
    )

    return response.data
  },
  async update(id, contact) {
        const response = await api.patch(`/contacts/${id}`, contact)

        return response.data
  },
  async getById(id) {
        const response = await api.get(`/contacts/${id}`)

        return response.data
  },
  async delete(id) {
        await api.delete(`/contacts/${id}`)
  },

}

export default contactService