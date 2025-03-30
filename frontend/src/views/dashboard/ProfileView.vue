<!-- src/views/dashboard/ProfileView.vue -->
<template>
  <div class="container py-6 mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-slate-200">Your Profile</h1>
      <p class="text-slate-400">Manage your personal information and social connections</p>
    </div>

    <div class="grid gap-6 md:grid-cols-[250px_1fr] lg:grid-cols-[280px_1fr]">
      <!-- Profile Navigation Sidebar -->
      <ProfileSidebar
        :sections="profileSections"
        :active-section="activeSection"
        @update:section="activeSection = $event"
      />

      <!-- Profile Content Area -->
      <div class="bg-slate-800/50 rounded-lg p-6">
        <div v-if="profileStore.isLoading || isLoading" class="flex justify-center py-8">
          <div
            class="animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-indigo-500"
          ></div>
        </div>

        <template v-else>
          <PersonalInfoSection v-if="activeSection === 'personal'" />
          <ContactInfoSection
            v-if="activeSection === 'contact'"
            @add-email="showAddEmailModal = true"
          />
          <SocialProfilesSection
            v-if="activeSection === 'social'"
            ref="socialProfilesRef"
            @show-social-modal="openSocialModal"
            @add-profile="showAddProfileModal = true"
            @delete-profile="handleDeleteProfile"
          />
          <PrivacySettingsSection v-if="activeSection === 'privacy'" />
          <SecuritySettingsSection v-if="activeSection === 'security'" />
        </template>
      </div>
    </div>

    <!-- Modals -->
    <AddEmailModal
      :show="showAddEmailModal"
      @close="showAddEmailModal = false"
      @add-email="addEmailAddress"
    />

    <AddSocialModal
      :show="showSocialModal"
      :social-type="currentSocial"
      :profile-id="selectedProfileId || undefined"
      @close="showSocialModal = false"
      @add-social="addSocialProfile"
    />

    <AddProfileModal
      :show="showAddProfileModal"
      @close="showAddProfileModal = false"
      @profile-created="handleProfileCreated"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useProfileStore } from '@/stores/profile'
import { useToast } from '@/components/ui/toast'
import { User, Mail, Globe, Settings, Shield } from 'lucide-vue-next'

// Components
import ProfileSidebar from '@/components/profile/ProfileSidebar.vue'
import PersonalInfoSection from '@/components/profile/PersonalInfoSection.vue'
import ContactInfoSection from '@/components/profile/ContactInfoSection.vue'
import SocialProfilesSection from '@/components/profile/SocialProfilesSection.vue'
import PrivacySettingsSection from '@/components/profile/PrivacySettingsSection.vue'
import SecuritySettingsSection from '@/components/profile/SecuritySettingsSection.vue'
import AddEmailModal from '@/components/profile/AddEmailModal.vue'
import AddSocialModal from '@/components/profile/AddSocialModal.vue'
import AddProfileModal from '@/components/profile/AddProfileModal.vue'

// Store and utilities
const profileStore = useProfileStore()
const { toast } = useToast()

// Component state
const isLoading = ref(true)
const activeSection = ref('personal')
const showAddEmailModal = ref(false)
const showSocialModal = ref(false)
const showAddProfileModal = ref(false)
const currentSocial = ref('')
const selectedProfileId = ref<number | null>(null)
const socialProfilesRef = ref(null)
const profilesLoaded = ref(false)

// Navigation sections
const profileSections = [
  { id: 'personal', name: 'Personal Information', icon: User },
  { id: 'contact', name: 'Contact Information', icon: Mail },
  { id: 'social', name: 'Social Profiles', icon: Globe },
  { id: 'privacy', name: 'Privacy & Settings', icon: Settings },
  { id: 'security', name: 'Security', icon: Shield },
]

// Watch profiles and show add profile modal if empty
watch(
  () => profileStore.additionalProfiles,
  (profiles) => {
    // Only trigger if we've confirmed profiles have been loaded
    if (profilesLoaded.value && profiles.length === 0 && !showAddProfileModal.value) {
      // User has no profiles, show the add profile modal
      showAddProfileModal.value = true
    }
  },
  { immediate: false },
)

// Make sure to reset any global navigation state when this component mounts
onMounted(() => {
  // If you have a navigation store, reset the active item
  // Example: navigationStore.setActive('profile')

  // Load profile data
  loadProfileData()
})

async function loadProfileData() {
  try {
    isLoading.value = true
    await profileStore.fetchUserProfiles()
    profilesLoaded.value = true

    // After profiles are loaded, check if we need to show the modal
    if (profileStore.additionalProfiles.length === 0 && !showAddProfileModal.value) {
      showAddProfileModal.value = true
    }
  } catch (error) {
    console.error('Error loading profile data:', error)
    toast({
      variant: 'destructive',
      title: 'Error',
      description: 'Failed to load profile data',
    })
  } finally {
    isLoading.value = false
  }
}

async function handleProfileCreated(profile: { id: number }) {
  // Just refresh the profiles list
  await profileStore.fetchUserProfiles()

  // Select the newly created profile
  if (
    socialProfilesRef.value &&
    socialProfilesRef.value !== null &&
    typeof socialProfilesRef.value === 'object' &&
    'handleProfileSelect' in socialProfilesRef.value
  ) {
    // Use type assertion to call the method
    ;(socialProfilesRef.value as { handleProfileSelect: (id: number) => void }).handleProfileSelect(
      profile.id,
    )
  }

  // Show a toast suggesting to add social connections
  toast({
    title: 'Profile Created',
    description: 'Your new profile has been created. You can now add social connections to it.',
  })
}

async function handleDeleteProfile(profileId: number) {
  try {
    isLoading.value = true
    await profileStore.deleteUserProfile(profileId)

    toast({
      title: 'Success',
      description: 'Profile deleted successfully.',
    })

    // Refresh the profiles list
    await profileStore.fetchUserProfiles()

    // Refresh the social profiles section
    if (
      socialProfilesRef.value &&
      socialProfilesRef.value !== null &&
      typeof socialProfilesRef.value === 'object' &&
      'refreshSocialProfiles' in socialProfilesRef.value
    ) {
      // Use type assertion to call the method
      ;(socialProfilesRef.value as { refreshSocialProfiles: () => void }).refreshSocialProfiles()
    }
  } catch (error: unknown) {
    const errorMessage =
      error instanceof Error ? error.message : 'Failed to delete profile. Please try again.'
    console.error('Error deleting profile:', error)
    toast({
      variant: 'destructive',
      title: 'Error',
      description: errorMessage,
    })
  } finally {
    isLoading.value = false
  }
}

function openSocialModal(socialType: string, profileId: number | null) {
  currentSocial.value = socialType
  selectedProfileId.value = profileId
  showSocialModal.value = true
}
async function addEmailAddress(data: { email: string; isPrimary?: boolean }) {
  try {
    await profileStore.addUserProfile({
      email: data.email,
      profile_visibility: true,
      notification_preferences: {},
      display_name: undefined,
    })
    showAddEmailModal.value = false
    toast({
      title: 'Success',
      description: 'Email address added successfully.',
    })
  } catch (error: unknown) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to add email address.'
    toast({
      variant: 'destructive',
      title: 'Error',
      description: errorMessage,
    })
  }
}
async function addSocialProfile(data: Record<string, unknown>) {
  try {
    await profileStore.addSocialProfileToProfile(selectedProfileId.value, {
      social_type: data.social_type as string,
      social_handle: data.social_handle as string | undefined,
      social_url: data.social_url as string | undefined,
      visibility: (data.visibility as boolean) || true,
    })
    showSocialModal.value = false
    toast({
      title: 'Success',
      description: `Social profile connected successfully.`,
    })

    // Refresh the displayed social profiles
    if (
      socialProfilesRef.value &&
      socialProfilesRef.value !== null &&
      typeof socialProfilesRef.value === 'object' &&
      'refreshSocialProfiles' in socialProfilesRef.value
    ) {
      // Use type assertion to call the method
      ;(socialProfilesRef.value as { refreshSocialProfiles: () => void }).refreshSocialProfiles()
    }
  } catch (error: unknown) {
    const errorMessage =
      error instanceof Error ? error.message : 'Failed to connect social profile.'
    toast({
      variant: 'destructive',
      title: 'Error',
      description: errorMessage,
    })
  }
}
</script>
