import api from "@/api/api"

export default {

    async getCompanies(){

        const response = await api.get("/companies")

        return response.data

    }

}