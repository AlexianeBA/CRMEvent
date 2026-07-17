<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="400" class="pa-6">
      <h2 class="text-h5 mb-6 text-center">Créer un compte</h2>

      <v-form @submit.prevent="register">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          required
        />

        <v-text-field
          v-model="password"
          label="Mot de passe"
          type="password"
          required
        />

        <v-text-field
          v-model="confirmPassword"
          label="Confirmer le mot de passe"
          type="password"
          required
        />

        <v-btn
          color="primary"
          block
          class="mt-4"
          type="submit"
        >
          Créer le compte
        </v-btn>
      </v-form>

      <p class="text-center mt-4">
        Déjà un compte ?
        <router-link to="/login">Se connecter</router-link>
      </p>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import api from "../api/api";
import { useRouter } from "vue-router";

const router = useRouter();

const email = ref("");
const password = ref("");
const confirmPassword = ref("");

const register = async () => {
  if (password.value !== confirmPassword.value) {
    alert("Les mots de passe ne correspondent pas");
    return;
  }

  try {
    await api.post("/auth/register", {
      email: email.value,
      password: password.value,
    });

    alert("Compte créé avec succès");
    router.push("/login");
  } catch (err) {
  const detail = err?.response?.data?.detail;

  if (Array.isArray(detail)) {
    const messages = detail.map((item) => item.msg).join(", ");
    alert(messages);
  } else {
    alert(detail || "Erreur lors de la création du compte");
  }
  }
};
</script>