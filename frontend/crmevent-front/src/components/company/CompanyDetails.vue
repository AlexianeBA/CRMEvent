<template>
  <div class="details-grid">
    <DetailsCard
      title="Informations générales"
      icon="mdi-domain"
      :item="company"
      :fields="generalFields"
    />

    <div class="contacts-card">
      <div class="contacts-header">
        <div class="contacts-title">
          <v-icon icon="mdi-account-multiple-outline" />
          <h2>Contacts</h2>
        </div>

        <v-chip
          color="primary"
          variant="tonal"
          size="small"
        >
          {{ company.contacts?.length || 0 }}
        </v-chip>
      </div>

      <div
        v-if="company.contacts?.length"
        class="contacts-list"
      >
        <article
          v-for="contact in company.contacts"
          :key="contact.id"
          class="contact-card"
        >
          <v-avatar
            color="primary"
            size="46"
          >
            <span class="contact-initials">
              {{ getInitials(contact) }}
            </span>
          </v-avatar>

          <div class="contact-content">
            <div class="contact-top">
              <div>
                <strong class="contact-name">
                  {{ contact.first_name }} {{ contact.last_name }}
                </strong>

                <span class="contact-label">
                  Contact entreprise
                </span>
              </div>

              <v-btn
                icon="mdi-eye-outline"
                variant="text"
                size="small"
                title="Voir le contact"
                @click="viewContact(contact)"
              />
            </div>

            <div class="contact-details">
              <a
                v-if="contact.email"
                :href="`mailto:${contact.email}`"
              >
                <v-icon
                  icon="mdi-email-outline"
                  size="17"
                />

                {{ contact.email }}
              </a>

              <a
                v-if="contact.phone_number"
                :href="`tel:${contact.phone_number}`"
              >
                <v-icon
                  icon="mdi-phone-outline"
                  size="17"
                />

                {{ contact.phone_number }}
              </a>
            </div>
          </div>
        </article>
      </div>

      <div
        v-else
        class="empty-contact"
      >
        <v-icon
          icon="mdi-account-off-outline"
          size="38"
        />

        <p>Aucun contact rattaché</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router"

import DetailsCard from "@/components/common/DetailsCard.vue"

defineProps({
  company: {
    type: Object,
    required: true,
  },
})

const router = useRouter()

const generalFields = [
  { key: "name", label: "Nom" },
  { key: "address", label: "Adresse" },
  { key: "city", label: "Ville" },
]

function getInitials(contact) {
  return `${contact.first_name?.[0] ?? ""}${contact.last_name?.[0] ?? ""}`
    .toUpperCase()
}

function viewContact(contact) {
  router.push({
    name: "ContactView",
    params: {
      id: contact.id,
    },
  })
}
</script>

<style scoped>
.details-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.contacts-card {
  padding: 24px;
  background: white;
  border-radius: 14px;
}

.contacts-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 22px;
}

.contacts-title {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contacts-title h2 {
  margin: 0;
  font-size: 18px;
}

.contacts-list {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.contact-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 16px;
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  transition:
    box-shadow 0.2s ease,
    transform 0.2s ease;
}

.contact-card:hover {
  box-shadow: 0 6px 18px rgb(15 23 42 / 8%);
  transform: translateY(-1px);
}

.contact-initials {
  color: white;
  font-size: 14px;
  font-weight: 700;
}

.contact-content {
  min-width: 0;
  flex: 1;
}

.contact-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.contact-name {
  display: block;
  color: #111827;
  font-size: 15px;
}

.contact-label {
  display: block;
  margin-top: 2px;
  color: #9ca3af;
  font-size: 12px;
}

.contact-details {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
  margin-top: 12px;
}

.contact-details a {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: #8b644b;
  font-size: 14px;
  text-decoration: none;
}

.contact-details a:hover {
  text-decoration: underline;
}

.empty-contact {
  display: flex;
  min-height: 150px;
  align-items: center;
  justify-content: center;
  flex-direction: column;
  color: #9ca3af;
}

.empty-contact p {
  margin: 10px 0 0;
}

@media (max-width: 900px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>