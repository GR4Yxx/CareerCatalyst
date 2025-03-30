<template>
  <div class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-3xl font-bold tracking-tight">Interview Preparation</h1>
        <p class="text-muted-foreground">
          Practice your interview skills with an AI-powered mock interviewer
        </p>
      </div>
    </div>

    <div class="grid gap-6 md:grid-cols-2">
      <!-- Interview Simulator Card -->
      <Card class="col-span-1">
        <CardHeader>
          <CardTitle>Interview Simulator</CardTitle>
          <CardDescription>
            Practice with a realistic AI-powered interview simulation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div class="grid gap-4">
              <div>
                <Label for="job-description">Job Description</Label>
                <Textarea
                  id="job-description"
                  v-model="jobDescription"
                  placeholder="Paste the job description here..."
                  class="min-h-[100px]"
                />
              </div>
              <div>
                <Label for="resume">Your Resume</Label>
                <Textarea
                  id="resume"
                  v-model="resume"
                  placeholder="Paste your resume content here..."
                  class="min-h-[100px]"
                />
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter>
          <Button class="w-full" @click="startInterview" :disabled="isLoading">
            <Loader2 v-if="isLoading" class="mr-2 h-4 w-4 animate-spin" />
            Start Interview
          </Button>
        </CardFooter>
      </Card>

      <!-- Chat Interface Card (shows after starting interview) -->
      <Card v-if="chatStarted" class="col-span-1">
        <CardHeader>
          <CardTitle>Mock Interview</CardTitle>
          <CardDescription> Answer the questions as you would in a real interview </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4 max-h-[400px] overflow-y-auto p-2">
            <div v-for="(message, index) in chatMessages" :key="index" class="flex flex-col">
              <div
                :class="[
                  'rounded-lg p-3 mb-2 max-w-[80%]',
                  message.role === 'user'
                    ? 'bg-primary text-primary-foreground self-end'
                    : 'bg-muted self-start',
                ]"
              >
                {{ message.content }}
              </div>
            </div>
          </div>
        </CardContent>
        <CardFooter class="flex flex-col space-y-2">
          <div class="relative w-full">
            <Textarea
              v-model="userMessage"
              placeholder="Type your response..."
              class="pr-12 resize-none"
              @keydown.enter.prevent="sendMessage"
            />
            <Button
              variant="ghost"
              size="icon"
              class="absolute right-2 top-3"
              @click="sendMessage"
              :disabled="isLoading || !userMessage.trim()"
            >
              <SendHorizonal class="h-5 w-5" />
            </Button>
          </div>
        </CardFooter>
      </Card>

      <!-- Tips Card -->
      <Card class="col-span-1" :class="{ 'md:col-span-2': !chatStarted }">
        <CardHeader>
          <CardTitle>Interview Tips</CardTitle>
          <CardDescription> Ace your next interview with these professional tips </CardDescription>
        </CardHeader>
        <CardContent>
          <div class="space-y-4">
            <div v-for="(tip, index) in interviewTips" :key="index" class="flex gap-3">
              <div
                class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10"
              >
                <component :is="tip.icon" class="h-4 w-4 text-primary" />
              </div>
              <div class="space-y-1">
                <h4 class="font-medium leading-none">{{ tip.title }}</h4>
                <p class="text-sm text-muted-foreground">{{ tip.description }}</p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import {
  Clock,
  Loader2,
  MessageSquare,
  SendHorizonal,
  UserRound,
  Eye,
  ThumbsUp,
  AlertCircle,
} from 'lucide-vue-next'

const jobDescription = ref('')
const resume = ref('')
const isLoading = ref(false)
const chatStarted = ref(false)
const sessionId = ref('')
const userMessage = ref('')
const chatMessages = ref<{ role: 'user' | 'assistant'; content: string }[]>([])

const interviewTips = [
  {
    icon: Clock,
    title: 'Be Punctual',
    description:
      'Arrive 10-15 minutes early to allow time for unexpected delays and check-in procedures.',
  },
  {
    icon: UserRound,
    title: 'Research the Company',
    description:
      "Understand the company's mission, values, recent news, and the role you're applying for.",
  },
  {
    icon: MessageSquare,
    title: 'Prepare Stories',
    description:
      'Have specific examples ready that demonstrate your skills and experience relevant to the job.',
  },
  {
    icon: Eye,
    title: 'Mind Your Body Language',
    description:
      'Maintain eye contact, sit up straight, and offer a firm handshake to convey confidence.',
  },
  {
    icon: ThumbsUp,
    title: 'Highlight Achievements',
    description:
      "Don't just list responsibilities - emphasize your accomplishments and their impact.",
  },
  {
    icon: AlertCircle,
    title: 'Ask Thoughtful Questions',
    description: 'Prepare questions that show your interest in the role and company.',
  },
]

async function startInterview() {
  if (!jobDescription.value.trim() || !resume.value.trim()) {
    // TODO: Add proper validation and error messaging
    return
  }

  isLoading.value = true

  try {
    // This would normally connect to a backend API
    // Since we're not implementing the actual backend connection yet, we'll simulate it
    await new Promise((resolve) => setTimeout(resolve, 1500))

    // Simulate response from backend
    const initialResponse =
      "Hello! I'm your AI interview assistant. I've reviewed your resume and the job description. Let's begin with a common question: Can you tell me a bit about yourself and why you're interested in this position?"

    sessionId.value = 'mock-session-1' // This would come from the backend
    chatMessages.value = [{ role: 'assistant', content: initialResponse }]
    chatStarted.value = true
  } catch (error) {
    console.error('Error starting interview:', error)
    // TODO: Add proper error handling
  } finally {
    isLoading.value = false
  }
}

async function sendMessage() {
  if (!userMessage.value.trim() || isLoading.value) return

  const message = userMessage.value
  chatMessages.value.push({ role: 'user', content: message })
  userMessage.value = ''
  isLoading.value = true

  try {
    // This would connect to backend API
    // Simulating response for now
    await new Promise((resolve) => setTimeout(resolve, 1000))

    let response = ''
    // Simple mock responses based on the previous message count
    switch (chatMessages.value.length) {
      case 2:
        response =
          "Thank you for sharing that. Could you tell me about a challenging project you've worked on and how you approached it?"
        break
      case 4:
        response =
          "That's impressive. Now, looking at the job description, I see they're looking for experience with [relevant skill]. Can you describe your experience with this?"
        break
      case 6:
        response =
          'Good to know. How do you typically handle tight deadlines or working under pressure?'
        break
      case 8:
        response =
          'Thank you for your answers. Do you have any questions about the role or the company that I could help with?'
        break
      default:
        response =
          "That's valuable insight. Let's move to another topic: How do you stay updated with the latest trends and developments in your field?"
    }

    chatMessages.value.push({ role: 'assistant', content: response })
  } catch (error) {
    console.error('Error sending message:', error)
    // TODO: Add proper error handling
  } finally {
    isLoading.value = false

    // Scroll to bottom of chat
    setTimeout(() => {
      const chatContainer = document.querySelector('.overflow-y-auto')
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight
      }
    }, 100)
  }
}
</script>
