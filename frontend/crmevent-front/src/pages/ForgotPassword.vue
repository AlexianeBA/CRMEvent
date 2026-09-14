<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="440" class="pa-6">
      <h1 class="text-h5 mb-2 text-center">Mot de passe oublié</h1>
      <p class="text-body-2 text-medium-emphasis mb-6 text-center">
        Indique ton adresse email pour recevoir un lien de réinitialisation.
      </p>

      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">{{ success }}</v-alert>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

      <v-form v-if="!success" @submit.prevent="submit">
        <v-text-field v-model="email" label="Email" type="email" autocomplete="email" required />
        <v-btn color="primary" block class="mt-3" type="submit" :loading="loading">
          Envoyer le lien
        </v-btn>
      </v-form>

      <div class="text-center mt-5">
        <router-link to="/login">Retour à la connexion</router-link>
      </div>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue"
import api from "@/api/api"

defineOptions({ name: "ForgotPasswordPage" })

const email = ref("")
const loading = ref(false)
const success = ref("")
const error = ref("")

async function submit() {
  if (!email.value.trim()) return
  loading.value = true
  error.value = ""
  try {
    const response = await api.post("/auth/forgot-password", { email: email.value.trim() })
    success.value = response.data.detail
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Impossible d'envoyer la demande"
  } finally {
    loading.value = false
  }
}
</script>
