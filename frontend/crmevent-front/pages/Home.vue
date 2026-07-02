<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="600" class="pa-8 text-center">
      <h1 class="text-h4 mb-4">CRMEvent</h1>

      <p class="mb-6">
        Votre CRM pour gérer vos clients, opportunités, événements, devis et factures.
      </p>

      <v-list class="mb-6">
        <v-list-item>✔ Gestion des contacts</v-list-item>
        <v-list-item>✔ Pipeline commercial</v-list-item>
        <v-list-item>✔ Événements</v-list-item>
        <v-list-item>✔ Devis & facturation</v-list-item>
      </v-list>

      <div class="d-flex justify-center ga-3">
        <v-btn color="primary" to="/login">
          Se connecter
        </v-btn>

        <v-btn variant="outlined" to="/register">
          Créer un compte
        </v-btn>
      </div>
    </v-card>
  </v-container>
</template>