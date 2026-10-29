import { useRoute, useRouter } from 'vue-router'
import api from '@/api/api'
import { createListing } from './listingState'

export function useListing(resource, options = {}) {
  return createListing(resource, {
    ...options,
    route: useRoute(),
    router: useRouter(),
    client: api,
  })
}
