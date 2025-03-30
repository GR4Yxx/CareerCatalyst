<template>
  <div class="min-h-screen">
    <main class="container py-6 px-4 md:px-6">
      <div class="max-w-4xl mx-auto bg-card rounded-lg shadow-sm border">
        <!-- Chat header -->
        <div class="p-4 border-b flex items-center justify-between">
          <div class="flex items-center gap-3">
            <div class="w-10 h-10 rounded-full bg-muted flex items-center justify-center">
              <UserIcon class="h-5 w-5" />
            </div>
            <div>
              <h3 class="font-medium">John Smith</h3>
              <p class="text-xs text-muted-foreground">Online</p>
            </div>
          </div>
          <Button variant="ghost" size="icon">
            <MoreHorizontalIcon class="h-5 w-5" />
          </Button>
        </div>

        <!-- Chat messages -->
        <div class="h-[400px] overflow-y-auto p-4 flex flex-col gap-4" ref="messagesContainer">
          <div
            v-for="(message, index) in messages"
            :key="index"
            :class="[
              'max-w-[80%] p-3 rounded-lg',
              message.sent ? 'ml-auto bg-primary text-primary-foreground' : 'bg-muted',
            ]"
          >
            {{ message.text }}
            <div
              :class="[
                'text-xs mt-1',
                message.sent ? 'text-primary-foreground/70' : 'text-muted-foreground',
              ]"
            >
              {{ message.time }}
            </div>
          </div>
        </div>

        <!-- Chat input -->
        <div class="p-4 border-t">
          <form @submit.prevent="sendMessage" class="flex gap-2">
            <Input v-model="newMessage" placeholder="Type a message..." class="flex-1" />
            <Button type="submit" :disabled="!newMessage.trim()">
              <SendIcon class="h-4 w-4 mr-2" />
              Send
            </Button>
          </form>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import Navbar from '@/components/navigation/NavBar.vue'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { UserIcon, SendIcon, MoreHorizontalIcon } from 'lucide-vue-next'

interface ChatMessage {
  text: string
  sent: boolean
  time: string
}

const newMessage = ref('')
const messagesContainer = ref<HTMLElement | null>(null)

// Sample messages
const messages = ref<ChatMessage[]>([
  {
    text: 'Hi there! How can I help you today?',
    sent: false,
    time: '10:05 AM',
  },
  {
    text: "I'm trying to connect with other attendees from the AI conference last week.",
    sent: true,
    time: '10:06 AM',
  },
  {
    text: 'Sure! I can show you the attendee list from that event. Would you like to filter by interests?',
    sent: false,
    time: '10:07 AM',
  },
  {
    text: 'Yes, please filter for people interested in machine learning.',
    sent: true,
    time: '10:08 AM',
  },
  {
    text: 'I found 12 attendees with machine learning interests. Would you like me to show their profiles?',
    sent: false,
    time: '10:09 AM',
  },
])

const sendMessage = () => {
  if (newMessage.value.trim()) {
    const now = new Date()
    const hours = now.getHours() % 12 || 12
    const minutes = now.getMinutes().toString().padStart(2, '0')
    const ampm = now.getHours() >= 12 ? 'PM' : 'AM'

    messages.value.push({
      text: newMessage.value,
      sent: true,
      time: `${hours}:${minutes} ${ampm}`,
    })

    newMessage.value = ''

    // Simulate reply after 1 second
    setTimeout(() => {
      messages.value.push({
        text: 'Thanks for your message! This is a dummy response.',
        sent: false,
        time: `${hours}:${minutes} ${ampm}`,
      })
      scrollToBottom()
    }, 1000)
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

onMounted(() => {
  scrollToBottom()
})
</script>
