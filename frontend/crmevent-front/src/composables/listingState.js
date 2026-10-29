import { computed, onScopeDispose, reactive, ref, toValue, watch } from 'vue'
import { downloadResponse } from '../utils/download.js'

const keys = [
  'q',
  'status',
  'company_id',
  'commercial_id',
  'date_from',
  'date_to',
  'sort_by',
  'sort_order',
  'page',
  'page_size',
]
const scalar = (value) => (Array.isArray(value) ? value[0] : value)
const positive = (value, fallback, max = Number.MAX_SAFE_INTEGER) => {
  const number = Number(scalar(value))
  return Number.isSafeInteger(number) && number > 0 ? Math.min(number, max) : fallback
}

export function createListing(resource, { route, router, client, scope = {}, prefix = '' }) {
  const items = ref([])
  const total = ref(0)
  const pages = ref(0)
  const loading = ref(false)
  const exporting = ref(false)
  const error = ref('')
  const meta = ref({ statuses: [], sortable: [] })
  const options = ref({ companies: [], commercials: [] })
  const revision = ref(0)
  const fixedFilters = computed(() => Object.keys(toValue(scope)))
  const urlKey = (key) => `${toValue(prefix)}${key}`
  let disposed = false
  let metadataController

  const params = computed(() => {
    const read = (key) => scalar(route.query[urlKey(key)])
    const result = {
      page: positive(read('page'), 1),
      page_size: positive(read('page_size'), 20, 100),
      sort_by: read('sort_by') || 'id',
      sort_order: read('sort_order') === 'asc' ? 'asc' : 'desc',
    }
    for (const key of keys.slice(0, 6)) {
      const value = read(key)
      if (value !== undefined && value !== '') result[key] = value
    }
    return { ...result, ...toValue(scope) }
  })

  function update(changes, resetPage = true) {
    const query = { ...route.query }
    if (resetPage) query[urlKey('page')] = '1'
    for (const [key, value] of Object.entries(changes)) {
      if (value == null || value === '') delete query[urlKey(key)]
      else query[urlKey(key)] = String(value)
    }
    return router.push({ query })
  }

  function reset() {
    const query = { ...route.query }
    for (const key of keys) delete query[urlKey(key)]
    return router.push({ query })
  }

  function sort(key) {
    return update({
      sort_by: key,
      sort_order:
        params.value.sort_by === key && params.value.sort_order === 'asc' ? 'desc' : 'asc',
    })
  }

  const reload = () => {
    revision.value += 1
  }

  watch(
    () => toValue(resource),
    async (name) => {
      metadataController?.abort()
      if (!name) return
      const controller = new AbortController()
      metadataController = controller
      try {
        const [metadata, choices] = await Promise.all([
          client.get(`/lists/${name}/meta`, { signal: controller.signal }),
          client.get('/lists/options', { signal: controller.signal }),
        ])
        if (disposed || controller.signal.aborted) return
        meta.value = metadata.data
        options.value = choices.data
      } catch {
        if (!disposed && !controller.signal.aborted)
          error.value = 'Impossible de charger les filtres.'
      }
    },
    { immediate: true },
  )

  watch(
    [() => toValue(resource), params, revision],
    async ([name, current], _, onCleanup) => {
      if (!name) return
      const controller = new AbortController()
      onCleanup(() => controller.abort())
      loading.value = true
      error.value = ''
      try {
        const { data } = await client.get(`/lists/${name}/`, {
          params: current,
          signal: controller.signal,
        })
        if (controller.signal.aborted || disposed) return
        const lastPage = Math.max(1, data.pages)
        if (current.page > lastPage) {
          await update({ page: lastPage }, false)
          return
        }
        items.value = data.items
        total.value = data.total
        pages.value = data.pages
      } catch (err) {
        if (controller.signal.aborted || disposed) return
        items.value = []
        total.value = 0
        pages.value = 0
        const detail = err.response?.data?.detail
        error.value =
          typeof detail === 'string'
            ? detail
            : 'Impossible de charger la liste. Vérifie les filtres.'
      } finally {
        if (!controller.signal.aborted && !disposed) loading.value = false
      }
    },
    { immediate: true },
  )

  async function exportFile(format) {
    exporting.value = true
    error.value = ''
    try {
      const filters = { ...params.value }
      delete filters.page
      delete filters.page_size
      const response = await client.get(`/lists/${toValue(resource)}/export`, {
        params: { ...filters, format },
        responseType: 'blob',
      })
      downloadResponse(response, `${toValue(resource)}.${format}`)
    } catch {
      error.value = 'Impossible d’exporter la liste.'
    } finally {
      exporting.value = false
    }
  }

  onScopeDispose(() => {
    disposed = true
    metadataController?.abort()
  })

  return reactive({
    items,
    total,
    pages,
    loading,
    exporting,
    error,
    meta,
    options,
    params,
    fixedFilters,
    update,
    reset,
    sort,
    reload,
    exportFile,
  })
}
