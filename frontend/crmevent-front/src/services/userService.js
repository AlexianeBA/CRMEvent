import api from "@/api/api"

export const userService = {
  async getUsers() {
    const response = await api.get(
      "/auth/users/options",
    )

    return response.data
  },
}

export default userService
