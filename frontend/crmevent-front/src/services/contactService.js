import api from "@/api/api"

export default {

    async getContacts(){

        const response = await api.get("/contacts")

        return response.data

    }

}