import api from "@/api/api"

export default {

    async getQuotes(){

        const response = await api.get("/quotes")

        return response.data

    }

}