<!-- views/dashboard/ConnectionsView.vue -->
<template>
  <TooltipProvider>
    <div class="container py-4">
      <!-- Header Section -->
      <div class="mb-6">
        <h1 class="text-2xl font-semibold mb-1">My Network</h1>
        <p class="text-muted-foreground">Manage your professional connections</p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="mb-6 space-y-4">
        <div class="flex flex-wrap gap-4">
          <div class="relative flex-1 min-w-[240px]">
            <Search class="absolute left-2 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              v-model="searchQuery"
              placeholder="Search connections..."
              class="pl-8"
              @input="debounceSearch"
            />
          </div>
          <Select v-model="filterStatus" @update:modelValue="fetchConnections">
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Filter by status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Connections</SelectItem>
              <SelectItem value="accepted">Connected</SelectItem>
              <SelectItem value="pending">Pending</SelectItem>
              <SelectItem value="blocked">Blocked</SelectItem>
            </SelectContent>
          </Select>
          <Select v-model="sortOption" @update:modelValue="fetchConnections">
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="recent">Most Recent</SelectItem>
              <SelectItem value="name_asc">Name (A-Z)</SelectItem>
              <SelectItem value="name_desc">Name (Z-A)</SelectItem>
              <SelectItem value="connections">Most Connections</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="space-y-4">
        <div
          v-for="i in 3"
          :key="i"
          class="flex items-center justify-between p-4 border rounded-lg bg-card"
        >
          <div class="flex items-center gap-4">
            <Skeleton class="h-16 w-16 rounded-full" />
            <div class="space-y-2">
              <Skeleton class="h-4 w-[250px]" />
              <Skeleton class="h-4 w-[150px]" />
            </div>
          </div>
          <div class="flex items-center gap-3">
            <Skeleton class="h-8 w-8 rounded-full" />
            <Skeleton class="h-8 w-8 rounded-full" />
            <Skeleton class="h-8 w-8 rounded-full" />
            <Skeleton class="h-8 w-24" />
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div
        v-else-if="filteredConnections.length === 0"
        class="flex flex-col items-center justify-center rounded-lg border border-dashed p-8 text-center"
      >
        <Users class="mb-4 h-12 w-12 text-muted-foreground" />
        <h3 class="mb-1 text-lg font-medium">No connections found</h3>
        <p class="mb-4 text-sm text-muted-foreground">
          {{ getEmptyStateMessage() }}
        </p>
        <Button @click="resetFilters">Reset Filters</Button>
      </div>

      <!-- Connections List -->
      <div v-else class="space-y-4">
        <div
          v-for="connection in filteredConnections"
          :key="connection.id"
          class="flex flex-col md:flex-row md:items-center justify-between p-4 border rounded-lg bg-card hover:border-primary/50 transition-colors"
        >
          <!-- Connection Info -->
          <div class="flex items-center gap-4 mb-4 md:mb-0">
            <Avatar class="h-16 w-16">
              <AvatarImage :src="connection.avatar ?? ''" :alt="connection.name" />
              <AvatarFallback>{{ connection.initials }}</AvatarFallback>
            </Avatar>
            <div>
              <h3 class="font-semibold">{{ connection.name }}</h3>
              <p class="text-sm text-muted-foreground">
                {{ connection.company_name || 'No company' }}
              </p>
              <Badge :variant="getStatusVariant(connection.status)" class="mt-1">
                {{ getStatusLabel(connection.status) }}
              </Badge>
              <p v-if="connection.connection_source" class="text-xs text-muted-foreground mt-1">
                Connected via: {{ formatSource(connection.connection_source) }}
              </p>
            </div>
          </div>

          <!-- Social Media and Actions -->
          <div class="flex flex-wrap items-center gap-3">
            <!-- Social Icons -->
            <div class="flex gap-2 mr-2">
              <Tooltip v-for="social in connection.socials" :key="social.type">
                <TooltipTrigger asChild>
                  <button
                    class="rounded-full p-2 transition-all duration-200"
                    :class="[getSocialStateClass(social.status), 'hover:opacity-80']"
                    @click="handleSocialClick(social, connection)"
                    @contextmenu.prevent="handleSocialAction(social, connection)"
                  >
                    <component :is="getSocialIcon(social.type)" class="w-5 h-5" />
                  </button>
                </TooltipTrigger>
                <TooltipContent>{{ getSocialTooltip(social) }}</TooltipContent>
              </Tooltip>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-2 mt-3 md:mt-0">
              <!-- Status-specific action buttons -->
              <template v-if="connection.status === 'pending'">
                <Button size="sm" variant="default" @click="acceptConnection(connection)">
                  Accept
                </Button>
                <Button size="sm" variant="outline" @click="declineConnection(connection)">
                  Decline
                </Button>
              </template>

              <template v-else>
                <Button variant="outline" size="sm" @click="handleNotes(connection)">
                  <Pencil class="h-4 w-4 mr-1" />
                  Notes
                </Button>

                <Button
                  v-if="connection.calendly_link"
                  variant="outline"
                  size="sm"
                  @click="handleScheduleMeeting(connection)"
                >
                  <Calendar class="h-4 w-4 mr-1" />
                  Schedule
                </Button>

                <DropdownMenu v-if="connection.status === 'accepted'">
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem @click="exportContact(connection)">
                      <Download class="h-4 w-4 mr-2" />
                      Export Contact
                    </DropdownMenuItem>
                    <DropdownMenuItem @click="blockConnection(connection)">
                      <Ban class="h-4 w-4 mr-2" />
                      Block Contact
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="mt-8 flex items-center justify-center">
        <Pagination
          v-slot="{ page }"
          :items-per-page="itemsPerPage"
          :total="totalItems"
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
                <Button
                  class="w-10 h-10 p-0"
                  :variant="item.value === page ? 'default' : 'outline'"
                >
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
  </TooltipProvider>

  <!-- Notes Dialog -->
  <Dialog v-model:open="showNotesDialog">
    <DialogContent>
      <DialogHeader>
        <DialogTitle>Notes for {{ selectedConnection?.name }}</DialogTitle>
      </DialogHeader>
      <div class="py-4">
        <Textarea
          v-model="connectionNotes"
          placeholder="Add your notes here..."
          class="min-h-[150px]"
        />
      </div>
      <DialogFooter>
        <Button variant="outline" @click="showNotesDialog = false">Cancel</Button>
        <Button @click="saveNotes">Save Notes</Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>

  <!-- Social Connection Dialog -->
  <Dialog v-model:open="showSocialDialog">
    <DialogContent>
      <DialogHeader>
        <DialogTitle
          >Connect with {{ selectedConnection?.name }} on {{ selectedSocial?.type }}</DialogTitle
        >
      </DialogHeader>
      <div class="py-4">
        <p class="text-muted-foreground mb-4">
          Would you like to connect with {{ selectedConnection?.name }} on
          {{ selectedSocial?.type }}?
        </p>
        <p v-if="selectedSocial?.status === 'connected'" class="text-sm bg-muted p-3 rounded mb-4">
          You're already connected with {{ selectedConnection?.name }} on
          {{ selectedSocial?.type }}.
        </p>
      </div>
      <DialogFooter>
        <Button variant="outline" @click="showSocialDialog = false">Cancel</Button>
        <Button :disabled="selectedSocial?.status === 'connected'" @click="connectOnSocial">
          Connect
        </Button>
      </DialogFooter>
    </DialogContent>
  </Dialog>
</template>

<script setup lang="ts">
import { ref, computed, h, onMounted } from 'vue'
import { Search, Pencil, Calendar, Users, MoreVertical, Download, Ban } from 'lucide-vue-next'
import { Input } from '@/components/ui/input'
import { Skeleton } from '@/components/ui/skeleton'
import { Avatar, AvatarImage, AvatarFallback } from '@/components/ui/avatar'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Tooltip, TooltipTrigger, TooltipContent } from '@/components/ui/tooltip'
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from '@/components/ui/dialog'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
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
import { Textarea } from '@/components/ui/textarea'
import { Twitter, Linkedin, Facebook, Instagram, Youtube, Music4 } from 'lucide-vue-next'
import TooltipProvider from '@/components/ui/tooltip/TooltipProvider.vue'
import { useToast } from '@/components/ui/toast/use-toast'

// Types from your schema
type SocialStatus = 'connected' | 'not_connected' | 'not_available'
type ConnectionStatus = 'accepted' | 'pending' | 'blocked' | 'declined'

interface Social {
  type: 'facebook' | 'twitter' | 'instagram' | 'linkedin' | 'tiktok' | 'threads' | 'youtube'
  status: SocialStatus
}

interface Connection {
  id: number
  name: string
  initials: string
  company_name?: string
  avatar?: string
  calendly_link?: string
  status: ConnectionStatus
  socials: Social[]
  notes?: string
  connection_source?: string
  last_interaction_at?: string
}

// Toast
const { toast } = useToast()

// State
const searchQuery = ref('')
const filterStatus = ref('all')
const sortOption = ref('recent')
const searchTimeout = ref<number | null>(null)
const showNotesDialog = ref(false)
const showSocialDialog = ref(false)
const selectedConnection = ref<Connection | null>(null)
const selectedSocial = ref<Social | null>(null)
const connectionNotes = ref('')
const loading = ref(true)
const currentPage = ref(1)
const totalPages = ref(5) // This would come from your API
const totalItems = ref(50) // Added total items for pagination
const itemsPerPage = ref(10) // This would come from your API or be set by you

// Mock data - replace with API call
const connections = ref<Connection[]>([
  {
    id: 1,
    name: 'Janet Doe',
    initials: 'JD',
    company_name: 'Tech Corp',
    status: 'accepted',
    connection_source: 'linkedin',
    last_interaction_at: '2025-03-20T14:30:00Z',
    socials: [
      { type: 'facebook', status: 'not_available' },
      { type: 'linkedin', status: 'connected' },
      { type: 'twitter', status: 'connected' },
      { type: 'instagram', status: 'not_connected' },
    ],
  },
  {
    id: 2,
    name: 'Michael Smith',
    initials: 'MS',
    company_name: 'Innovation Labs',
    status: 'pending',
    connection_source: 'event',
    socials: [
      { type: 'linkedin', status: 'connected' },
      { type: 'twitter', status: 'not_connected' },
      { type: 'youtube', status: 'not_available' },
    ],
    calendly_link: 'https://calendly.com/michael',
  },
  {
    id: 3,
    name: 'Sarah Johnson',
    initials: 'SJ',
    company_name: 'Digital Solutions',
    status: 'accepted',
    connection_source: 'tech_meetup_2025',
    last_interaction_at: '2025-03-15T09:20:00Z',
    socials: [
      { type: 'linkedin', status: 'connected' },
      { type: 'instagram', status: 'connected' },
      { type: 'threads', status: 'connected' },
      { type: 'twitter', status: 'not_connected' },
    ],
    calendly_link: 'https://calendly.com/sarah',
  },
  {
    id: 4,
    name: 'David Wilson',
    initials: 'DW',
    company_name: 'StartUp Inc',
    status: 'blocked',
    connection_source: 'manual',
    socials: [
      { type: 'linkedin', status: 'not_connected' },
      { type: 'twitter', status: 'not_available' },
      { type: 'facebook', status: 'not_available' },
    ],
  },
  {
    id: 5,
    name: 'Emily Chen',
    initials: 'EC',
    company_name: 'Growth Ventures',
    status: 'accepted',
    connection_source: 'referral',
    last_interaction_at: '2025-03-10T16:45:00Z',
    socials: [
      { type: 'linkedin', status: 'connected' },
      { type: 'twitter', status: 'connected' },
      { type: 'instagram', status: 'connected' },
      { type: 'youtube', status: 'connected' },
    ],
    calendly_link: 'https://calendly.com/emily',
  },
])

// Computed
const filteredConnections = computed(() => {
  return connections.value.filter((connection) => {
    const matchesSearch =
      connection.name.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      connection.company_name?.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      false
    const matchesFilter = filterStatus.value === 'all' || connection.status === filterStatus.value
    return matchesSearch && matchesFilter
  })
})

// Helpers
const getSocialIcon = (type: Social['type']) => {
  const icons = {
    facebook: Facebook,
    twitter: Twitter,
    instagram: Instagram,
    linkedin: Linkedin,
    tiktok: Music4,
    threads: () => h('div', { class: 'w-5 h-5' }, '@'),
    youtube: Youtube,
  }
  return icons[type]
}

const getSocialStateClass = (status: string) => {
  switch (status) {
    case 'connected':
      return 'bg-primary/15 text-primary hover:bg-primary/25'
    case 'not_connected':
      return 'bg-slate-100 text-slate-500 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-400 dark:hover:bg-slate-700'
    case 'not_available':
      return 'bg-muted/30 text-muted-foreground/50 cursor-not-allowed'
    default:
      return 'bg-muted text-muted-foreground'
  }
}

const getSocialTooltip = (social: Social) => {
  switch (social.status) {
    case 'connected':
      return `Connected on ${social.type}`
    case 'not_connected':
      return `Connect on ${social.type}`
    case 'not_available':
      return `${social.type} not available`
  }
}

const getStatusVariant = (status: ConnectionStatus) => {
  switch (status) {
    case 'accepted':
      return 'default'
    case 'pending':
      return 'secondary'
    case 'blocked':
      return 'destructive'
    case 'declined':
      return 'outline'
  }
}

const getStatusLabel = (status: ConnectionStatus) => {
  switch (status) {
    case 'accepted':
      return 'Connected'
    case 'pending':
      return 'Pending'
    case 'blocked':
      return 'Blocked'
    case 'declined':
      return 'Declined'
  }
}

const formatSource = (source: string) => {
  if (source === 'linkedin') return 'LinkedIn'
  if (source === 'event') return 'Event'
  if (source === 'manual') return 'Manual'
  if (source === 'referral') return 'Referral'
  if (source.startsWith('tech_')) return 'Tech Meetup'
  return source.charAt(0).toUpperCase() + source.slice(1).replace(/_/g, ' ')
}

const getEmptyStateMessage = () => {
  if (searchQuery.value && filterStatus.value !== 'all') {
    return `No ${filterStatus.value} connections matching "${searchQuery.value}"`
  } else if (searchQuery.value) {
    return `No connections matching "${searchQuery.value}"`
  } else if (filterStatus.value !== 'all') {
    return `No ${filterStatus.value} connections found`
  }
  return "You don't have any connections yet"
}

// Event handlers
const debounceSearch = () => {
  if (searchTimeout.value) {
    clearTimeout(searchTimeout.value)
  }

  searchTimeout.value = setTimeout(() => {
    currentPage.value = 1
    fetchConnections()
  }, 300) as unknown as number
}

const fetchConnections = async () => {
  loading.value = true

  try {
    // In a real implementation, you would fetch from the API
    // const params = new URLSearchParams()
    // params.append('page', currentPage.value.toString())
    // params.append('perPage', itemsPerPage.value.toString())
    // params.append('status', filterStatus.value)
    // params.append('search', searchQuery.value)
    // params.append('sort', sortOption.value)

    // const response = await fetch(`/api/connections?${params.toString()}`)
    // const data = await response.json()
    // connections.value = data.data
    // totalPages.value = data.meta.total_pages
    // totalItems.value = data.meta.total

    // Simulate API delay
    await new Promise((resolve) => setTimeout(resolve, 500))

    // For now, just use the mock data
    // This would normally come from the API
  } catch (error) {
    toast({
      variant: 'destructive',
      title: 'Error fetching connections',
      description: 'Please try again later',
    })
    console.error('Error fetching connections:', error)
  } finally {
    loading.value = false
  }
}

const handleSocialClick = (social: Social, connection: Connection) => {
  if (social.status === 'not_connected') {
    selectedConnection.value = connection
    selectedSocial.value = social
    showSocialDialog.value = true
  }
}

const handleSocialAction = (social: Social, connection: Connection) => {
  if (social.status === 'connected') {
    selectedConnection.value = connection
    selectedSocial.value = social
    showSocialDialog.value = true
  }
}

const connectOnSocial = () => {
  if (selectedConnection.value && selectedSocial.value) {
    // In a real implementation, this would call an API
    const socialToUpdate = selectedConnection.value.socials.find(
      (s) => s.type === selectedSocial.value?.type,
    )

    if (socialToUpdate) {
      socialToUpdate.status = 'connected'
      toast({
        title: 'Social connection updated',
        description: `You're now connected with ${selectedConnection.value.name} on ${selectedSocial.value.type}`,
      })
    }

    showSocialDialog.value = false
  }
}

const handleNotes = (connection: Connection) => {
  selectedConnection.value = connection
  connectionNotes.value = connection.notes || ''
  showNotesDialog.value = true
}

const saveNotes = () => {
  if (selectedConnection.value) {
    // In a real implementation, this would call an API
    selectedConnection.value.notes = connectionNotes.value

    toast({
      title: 'Notes saved',
      description: 'Your notes have been saved successfully',
    })

    showNotesDialog.value = false
  }
}

const handleScheduleMeeting = (connection: Connection) => {
  if (connection.calendly_link) {
    window.open(connection.calendly_link, '_blank')
  }
}

const acceptConnection = (connection: Connection) => {
  // In a real implementation, this would call an API
  connection.status = 'accepted'

  toast({
    title: 'Connection accepted',
    description: `You are now connected with ${connection.name}`,
  })
}

const declineConnection = (connection: Connection) => {
  // In a real implementation, this would call an API
  connection.status = 'declined'

  toast({
    title: 'Connection declined',
    description: `You have declined the connection with ${connection.name}`,
  })
}

const blockConnection = (connection: Connection) => {
  // In a real implementation, this would call an API
  connection.status = 'blocked'

  toast({
    variant: 'destructive',
    title: 'Connection blocked',
    description: `You have blocked ${connection.name}`,
  })
}

const exportContact = (connection: Connection) => {
  // In a real implementation, this would generate a vCard or similar
  toast({
    title: 'Contact exported',
    description: `Contact information for ${connection.name} has been downloaded`,
  })
}

const resetFilters = () => {
  searchQuery.value = ''
  filterStatus.value = 'all'
  sortOption.value = 'recent'
  currentPage.value = 1
  fetchConnections()
}

const goToPage = (page: number) => {
  currentPage.value = page
  fetchConnections()
}

const previousPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--
    fetchConnections()
  }
}

const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++
    fetchConnections()
  }
}

// Lifecycle hooks
onMounted(() => {
  fetchConnections()
})
</script>
