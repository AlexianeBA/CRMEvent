import api from "@/api/api"

export const quoteService = {
    async getQuotes() {
        const response = await api.get("/quotes")
        return response.data
    },

    async create(quote) {
        const response = await api.post("/quotes/", quote)
        return response.data
    },

    async getById(id) {
        const response = await api.get(`/quotes/${id}`)
        return response.data
    },

    async update(id, quote) {
        const response = await api.patch(`/quotes/${id}`, quote)
        return response.data
    },

    async updateStatus(id, status) {
        const response = await api.patch(
            `/quotes/${id}/status`,
            null,
            { params: { status } },
        )
        return response.data
    },
    async updateStatus(id, status) {
        const response = await api.patch(
        `/quotes/${id}/status`,
        null,
        {
            params: {
            status,
            },
        },
        )

        return response.data
    },

    async accept(id, userId) {
        const response = await api.post(
        `/quotes/${id}/accept`,
        null,
        {
            params: {
            user_id: userId,
            },
        },
        )

        return response.data
    },


    async delete(id) {
        await api.delete(`/quotes/${id}`)
    },
}

export default quoteService
