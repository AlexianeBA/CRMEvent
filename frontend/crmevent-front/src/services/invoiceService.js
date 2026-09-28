import api from "@/api/api"

export const invoiceService = {
  async getInvoices(params = {}) {
    const response = await api.get("/invoices", { params })
    return response.data
  },

  async getById(id) {
    const response = await api.get(`/invoices/${id}`)
    return response.data
  },

  async createFromQuote(quoteId) {
    const response = await api.post("/invoices/", null, {
      params: { quote_id: quoteId },
    })
    return response.data
  },

  async update(id, invoice) {
    const response = await api.patch(`/invoices/${id}`, invoice)
    return response.data
  },

  async updateStatus(id, status) {
    const response = await api.patch(
      `/invoices/${id}/status`,
      null,
      { params: { status } },
    )
    return response.data
  },

  async getPayments(id) {
    const response = await api.get(`/invoices/${id}/payments`)
    return response.data
  },

  async addPayment(id, payment) {
    const response = await api.post(`/invoices/${id}/payments`, payment)
    return response.data
  },

  async deletePayment(id, paymentId) {
    await api.delete(`/invoices/${id}/payments/${paymentId}`)
  },

  async delete(id) {
    await api.delete(`/invoices/${id}`)
  },
}

export default invoiceService
