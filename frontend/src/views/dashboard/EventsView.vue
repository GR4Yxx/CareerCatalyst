// src/views/dashboard/EventsView.vue

<template>
  <div class="events-view">
    <header class="mb-6">
      <h1 class="text-2xl font-bold">Discover Events</h1>
      <p class="text-muted-foreground">Find and join events that match your interests</p>
    </header>

    <!-- Search and filters -->
    <div class="mb-6 flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
      <div class="search-wrapper flex-1 md:max-w-md">
        <div class="relative">
          <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
          <Input
            v-model="searchQuery"
            type="search"
            placeholder="Search events..."
            class="pl-8"
            @input="debounceSearch"
          />
        </div>
      </div>

      <div class="filters flex flex-wrap items-center gap-2">
        <Select v-model="filters.category" @update:modelValue="applyFilters">
          <SelectTrigger class="w-full md:w-[180px]">
            <SelectValue placeholder="Category" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Categories</SelectItem>
            <SelectItem value="tech">Tech</SelectItem>
            <SelectItem value="business">Business</SelectItem>
            <SelectItem value="marketing">Marketing</SelectItem>
            <SelectItem value="design">Design</SelectItem>
            <SelectItem value="finance">Finance</SelectItem>
            <SelectItem value="healthcare">Healthcare</SelectItem>
            <SelectItem value="education">Education</SelectItem>
            <SelectItem value="networking">Networking</SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="filters.eventType" @update:modelValue="applyFilters">
          <SelectTrigger class="w-full md:w-[180px]">
            <SelectValue placeholder="Event Type" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all_types">All Types</SelectItem>
            <SelectItem value="in_person">In Person</SelectItem>
            <SelectItem value="virtual">Virtual</SelectItem>
            <SelectItem value="hybrid">Hybrid</SelectItem>
          </SelectContent>
        </Select>

        <Select v-model="filters.timeframe" @update:modelValue="applyFilters">
          <SelectTrigger class="w-full md:w-[180px]">
            <SelectValue placeholder="Timeframe" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="any_time">Any Time</SelectItem>
            <SelectItem value="today">Today</SelectItem>
            <SelectItem value="tomorrow">Tomorrow</SelectItem>
            <SelectItem value="this_week">This Week</SelectItem>
            <SelectItem value="weekend">This Weekend</SelectItem>
            <SelectItem value="this_month">This Month</SelectItem>
            <SelectItem value="next_month">Next Month</SelectItem>
            <SelectItem value="upcoming">Upcoming</SelectItem>
          </SelectContent>
        </Select>
      </div>
    </div>

    <!-- Events list -->
    <div v-if="loading" class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
      <div v-for="i in 6" :key="i" class="skeleton-card">
        <div class="h-44 w-full rounded-t-lg bg-muted"></div>
        <div class="p-4">
          <div class="mb-2 h-6 w-3/4 rounded bg-muted"></div>
          <div class="mb-4 h-4 w-1/2 rounded bg-muted"></div>
          <div class="mb-2 h-4 w-full rounded bg-muted"></div>
          <div class="h-4 w-2/3 rounded bg-muted"></div>
        </div>
      </div>
    </div>

    <div
      v-else-if="filteredEvents.length === 0"
      class="flex flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center"
    >
      <CalendarX class="mb-4 h-12 w-12 text-muted-foreground" />
      <h3 class="mb-1 text-lg font-medium">No events found</h3>
      <p class="mb-4 text-sm text-muted-foreground">
        Try adjusting your filters or search terms to find events.
      </p>
      <Button @click="resetFilters">Reset Filters</Button>
    </div>

    <div v-else class="grid grid-cols-1 gap-6 md:grid-cols-2 lg:grid-cols-3">
      <EventCard
        v-for="event in paginatedEvents"
        :key="event.id"
        :event="event"
        @click="navigateToEventDetails(event.id)"
      />
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="mt-8 flex items-center justify-center">
      <Pagination
        v-slot="{ page }"
        :items-per-page="itemsPerPage"
        :total="filteredEvents.length"
        :sibling-count="1"
        show-edges
        :default-page="currentPage"
        @update:page="goToPage"
      >
        <PaginationList v-slot="{ items }" class="flex items-center gap-1">
          <PaginationFirst @click="goToPage(1)" />
          <PaginationPrev @click="previousPage" />
          <template v-for="(item, index) in items">
            <PaginationListItem
              v-if="item.type === 'page'"
              :key="index"
              :value="item.value"
              as-child
            >
              <Button class="w-10 h-10 p-0" :variant="item.value === page ? 'default' : 'outline'">
                {{ item.value }}
              </Button>
            </PaginationListItem>
            <PaginationEllipsis v-else :key="item.type" :index="index" />
          </template>
          <PaginationNext @click="nextPage" />
          <PaginationLast @click="goToPage(totalPages)" />
        </PaginationList>
      </Pagination>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Search, CalendarX } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  Pagination,
  PaginationEllipsis,
  PaginationFirst,
  PaginationLast,
  PaginationList,
  PaginationListItem,
  PaginationNext,
  PaginationPrev,
} from '@/components/ui/pagination'
import EventCard from '@/components/events/EventCard.vue'
import { useEventStore, type Event } from '@/stores/event'
import { useToast } from '@/components/ui/toast'
import { mockEvents } from '@/data/mockEvents'

// Router
const router = useRouter()
const { toast } = useToast()

// Event store
const eventStore = useEventStore()

// Data
const allEvents = ref<Event[]>([])
const loading = ref(true)
const currentPage = ref(1)
const itemsPerPage = ref(9)
const searchQuery = ref('')
const searchTimeout = ref<number | null>(null)

// Filters
const filters = ref({
  category: 'all',
  eventType: 'all_types',
  timeframe: 'any_time',
})

// Computed
const filteredEvents = computed(() => {
  let result = [...allEvents.value]

  // Filter by search query
  if (searchQuery.value.trim()) {
    const searchLower = searchQuery.value.toLowerCase()
    result = result.filter(
      (event) =>
        event.title.toLowerCase().includes(searchLower) ||
        event.description?.toLowerCase().includes(searchLower) ||
        false ||
        event.location.toLowerCase().includes(searchLower),
    )
  }

  // Filter by category
  if (filters.value.category !== 'all') {
    result = result.filter((event) => event.category === filters.value.category)
  }

  // Filter by event type
  if (filters.value.eventType !== 'all_types') {
    result = result.filter((event) => event.event_type === filters.value.eventType)
  }

  // Filter by timeframe
  if (filters.value.timeframe !== 'any_time') {
    const now = new Date()
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const tomorrow = new Date(today)
    tomorrow.setDate(tomorrow.getDate() + 1)

    const nextWeek = new Date(today)
    nextWeek.setDate(today.getDate() + 7)

    const thisMonth = new Date(today)
    thisMonth.setMonth(today.getMonth() + 1)

    const nextMonth = new Date(today)
    nextMonth.setMonth(today.getMonth() + 2)

    switch (filters.value.timeframe) {
      case 'today':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          return eventDate >= today && eventDate < tomorrow
        })
        break
      case 'tomorrow':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          const nextDay = new Date(tomorrow)
          nextDay.setDate(tomorrow.getDate() + 1)
          return eventDate >= tomorrow && eventDate < nextDay
        })
        break
      case 'this_week':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          return eventDate >= today && eventDate < nextWeek
        })
        break
      case 'weekend':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          const dayOfWeek = eventDate.getDay() // 0 is Sunday, 6 is Saturday
          return (dayOfWeek === 0 || dayOfWeek === 6) && eventDate >= today && eventDate < nextWeek
        })
        break
      case 'this_month':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          return eventDate >= today && eventDate < thisMonth
        })
        break
      case 'next_month':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          return eventDate >= thisMonth && eventDate < nextMonth
        })
        break
      case 'upcoming':
        result = result.filter((event) => {
          const eventDate = new Date(event.start_time)
          return eventDate >= today
        })
        break
    }
  }

  return result
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredEvents.value.length / itemsPerPage.value))
})

const paginatedEvents = computed(() => {
  const startIndex = (currentPage.value - 1) * itemsPerPage.value
  const endIndex = startIndex + itemsPerPage.value
  return filteredEvents.value.slice(startIndex, endIndex)
})

// Watch for filter changes that would invalidate the current page
watch([filteredEvents], () => {
  if (currentPage.value > totalPages.value && totalPages.value > 0) {
    currentPage.value = totalPages.value
  }
})

// Methods
const fetchEvents = async () => {
  loading.value = true

  try {
    // Use the event store to fetch published events
    const events = await eventStore.fetchPublishedEvents()

    // Apply default image to events without cover photos
    allEvents.value = events.map((event: Event) => ({
      ...event,
      cover_image_path:
        event.cover_image_path ||
        'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=600&h=400&auto=format&fit=crop',
    }))
  } catch (error) {
    console.error('Error fetching events:', error)
    toast({
      title: 'Error',
      description: 'Failed to load events. Please try again later.',
      variant: 'destructive',
    })

    // Use mock data from the separate file
    allEvents.value = mockEvents
  } finally {
    loading.value = false
  }
}
const debounceSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
  }, 300) as unknown as number
}

const applyFilters = () => {
  currentPage.value = 1
}

const navigateToEventDetails = (id: number) => {
  router.push(`/dashboard/event/${id}`)
}

const resetFilters = () => {
  searchQuery.value = ''
  filters.value = {
    category: 'all',
    eventType: 'all_types',
    timeframe: 'any_time',
  }
  currentPage.value = 1
}

const goToPage = (page: number) => {
  currentPage.value = page
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchEvents()
})
</script>
