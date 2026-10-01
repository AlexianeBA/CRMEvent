import api from "@/api/api"

export const userService = {
  async getUsers() {
    const response = await api.get(
      "/auth/users/options",
    )

    return response.data
  },

  async getAllUsers() {
    const response = await api.get("/auth/users/list")
    return response.data
  },
}

export default userService
