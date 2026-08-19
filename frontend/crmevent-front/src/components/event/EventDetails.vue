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
      <template #field-company_id="{ value }">
        <RouterLink
          :to="{
            name: 'CompanyView',
            params: { id: value },
          }"
          class="detail-link"
        >
          Entreprise n°{{ value }}
        </RouterLink>
      </template>

      <template #field-contact_id="{ value }">
        <RouterLink
          v-if="value"
          :to="{
            name: 'ContactView',
            params: { id: value },
          }"
          class="detail-link"
        >
          Contact n°{{ value }}
        </RouterLink>

        <strong v-else>—</strong>
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
    key: "company_id",
    label: "Entreprise",
  },
  {
    key: "contact_id",
    label: "Contact",
  },
  {
    key: "opportunity_id",
    label: "Opportunité",
    formatter: (value) =>
      `Opportunité n°${value}`,
  },
  {
    key: "assigned_user_id",
    label: "Utilisateur assigné",
    formatter: (value) =>
      `Utilisateur n°${value}`,
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