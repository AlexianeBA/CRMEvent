<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="440" class="pa-6">
      <h1 class="text-h5 mb-6 text-center">Nouveau mot de passe</h1>

      <v-alert v-if="success" type="success" variant="tonal" class="mb-4">
        Mot de passe modifié. Tu peux maintenant te connecter.
      </v-alert>
      <v-alert v-if="error" type="error" variant="tonal" class="mb-4">{{ error }}</v-alert>

      <v-form v-if="!success" ref="formRef" @submit.prevent="submit">
        <v-text-field v-model="password" label="Nouveau mot de passe" type="password" autocomplete="new-password" hint="8 caractères minimum" :rules="[rules.required, rules.length]" />
        <v-text-field v-model="confirmation" label="Confirmer le mot de passe" type="password" autocomplete="new-password" :rules="[rules.required, rules.confirmation]" />
        <v-btn color="primary" block class="mt-3" type="submit" :loading="loading">
          Modifier le mot de passe
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
import { useRoute } from "vue-router"
import api from "@/api/api"

defineOptions({ name: "ResetPasswordPage" })

const route = useRoute()
const formRef = ref(null)
const password = ref("")
const confirmation = ref("")
const loading = ref(false)
const success = ref(false)
const error = ref("")
const rules = {
  required: (value) => Boolean(value) || "Ce champ est obligatoire",
  length: (value) => String(value ?? "").length >= 8 || "8 caractères minimum",
  confirmation: (value) => value === password.value || "Les mots de passe ne correspondent pas",
}

async function submit() {
  const validation = await formRef.value?.validate()
  if (!validation?.valid) return
  loading.value = true
  error.value = ""
  try {
    await api.post("/auth/reset-password", {
      token: String(route.params.token),
      new_password: password.value,
    })
    success.value = true
  } catch (err) {
    error.value = err.response?.data?.detail ?? "Lien invalide ou expiré"
  } finally {
    loading.value = false
  }
}
</script>
