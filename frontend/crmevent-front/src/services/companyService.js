import api from "@/api/api"

export const companyService = {

    async getCompanies(){

        const response = await api.get("/companies")

        return response.data

    },

    async getById(id) {
        const response = await api.get(`/companies/${id}`)

        return response.data
    },

    async create(company) {
        const response = await api.post("/companies/", company)

        return response.data
    },

    async update(id, company) {
        const response = await api.patch(`/companies/${id}`, company)

        return response.data
    },

    async delete(id) {
        await api.delete(`/companies/${id}`)
    },

}

export default companyService
