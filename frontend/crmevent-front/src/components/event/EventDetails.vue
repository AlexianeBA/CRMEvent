<template>
  <div class="details-grid">
    <DetailsCard
      title="Événement"
      icon="mdi-calendar-star"
      :item="event"
      :fields="generalFields"
    />

    <DetailsCard
      title="Organisation"
      icon="mdi-account-group-outline"
      :item="event"
      :fields="organizationFields"
    >
      <template #field-company="{ value }">
        <RouterLink
          :to="{
            name: 'CompanyView',
            params: { id: value.id },
          }"
          class="detail-link"
        >
          {{ value.name }}
        </RouterLink>
      </template>

      <template #field-contact="{ value }">
        <RouterLink
          v-if="value"
          :to="{
            name: 'ContactView',
            params: { id: value.id },
          }"
          class="detail-link"
        >
          {{ value.first_name }} {{ value.last_name }}
        </RouterLink>

        <strong v-else>—</strong>
      </template>

      <template #field-opportunity="{ value }">
        <RouterLink :to="{ name: 'OpportunityView', params: { id: value.id } }" class="detail-link">
          {{ value.title }}
        </RouterLink>
      </template>
    </DetailsCard>

    <DetailsCard
      title="Description"
      icon="mdi-text"
      :item="event"
      :fields="descriptionFields"
      class="full-width"
    />
  </div>
</template>

<script setup>
import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({
  event: {
    type: Object,
    required: true,
  },
})

const typeLabels = {
  webinar: "Webinaire",
  workshop: "Atelier",
  conference: "Conférence",
}

const statusLabels = {
  draft: "Brouillon",
  scheduled: "Planifié",
  held: "Terminé",
  canceled: "Annulé",
  locked: "Verrouillé",
}

const generalFields = [
  {
    key: "title",
    label: "Titre",
  },
  {
    key: "type",
    label: "Type",
    formatter: (value) =>
      typeLabels[value] ?? value,
  },
  {
    key: "date",
    label: "Date",
  },
  {
    key: "duration",
    label: "Durée",
    formatter: (value) =>
      value ? `${value} minutes` : "—",
  },
  {
    key: "location",
    label: "Localisation",
  },
  {
    key: "status",
    label: "Statut",
    formatter: (value) =>
      statusLabels[value] ?? value,
  },
]

const organizationFields = [
  {
    key: "company",
    label: "Entreprise",
  },
  {
    key: "contact",
    label: "Contact",
  },
  {
    key: "opportunity",
    label: "Opportunité",
  },
  {
    key: "assigned_user",
    label: "Utilisateur assigné",
    formatter: (value) => value?.email ?? "—",
  },
]

const descriptionFields = [
  {
    key: "description",
    label: "Description",
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

.full-width {
  grid-column: 1 / -1;
}

.detail-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
}

.detail-link:hover {
  text-decoration: underline;
}

@media (max-width: 900px) {
  .details-grid {
    grid-template-columns: 1fr;
  }

  .full-width {
    grid-column: auto;
  }
}
</style>
