<template>
  <div class="details-grid">
    <DetailsCard
      title="Identité"
      icon="mdi-account-outline"
      :item="contact"
      :fields="identityFields"
    />

    <DetailsCard
      title="Coordonnées"
      icon="mdi-card-account-details-outline"
      :item="contact"
      :fields="contactFields"
    >
      <template #field-email="{ value }">
        <a
          v-if="value"
          :href="`mailto:${value}`"
        >
          {{ value }}
        </a>

        <strong v-else>—</strong>
      </template>

      <template #field-phone_number="{ value }">
        <a
          v-if="value"
          :href="`tel:${value}`"
        >
          {{ value }}
        </a>

        <strong v-else>—</strong>
      </template>
      <template #field-company="{ value, item }">
        <RouterLink
            v-if="item.company?.id"
            :to="{
            name: 'CompanyView',
            params: {
                id: item.company.id,
            },
            }"
            class="company-link"
        >
            <v-icon
            icon="mdi-domain"
            size="18"
            />

            {{ value }}
        </RouterLink>

        <strong v-else>
            Aucune
        </strong>
        </template>
    </DetailsCard>
  </div>
</template>

<script setup>
import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({
  contact: {
    type: Object,
    required: true,
  },
})

const identityFields = [
  {
    key: "first_name",
    label: "Prénom",
  },
  {
    key: "last_name",
    label: "Nom",
  },
]

const contactFields = [
  {
    key: "email",
    label: "Adresse email",
  },
  {
    key: "phone_number",
    label: "Téléphone",
  },
  {
    key: "company",
    label: "Entreprise",
    value: (contact) =>
        contact.company?.name ?? "Aucune",
  },
]
</script>

<style scoped>
.details-grid {
  display: grid;
  grid-template-columns:
    repeat(2, minmax(0, 1fr));
  gap: 24px;
}

a {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

@media (max-width: 900px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>