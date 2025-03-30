<template>
  <div class="notifications-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Bell class="h-7 w-7 mr-3 text-primary" />
      Notifications
    </h1>

    <!-- Filter and Actions -->
    <div class="mb-6 p-4 bg-card rounded-lg border shadow-sm">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="flex items-center space-x-2">
          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Filter by type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Notifications</SelectItem>
              <SelectItem value="job">Job Matches</SelectItem>
              <SelectItem value="application">Applications</SelectItem>
              <SelectItem value="system">System</SelectItem>
            </SelectContent>
          </Select>

          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="newest">Newest first</SelectItem>
              <SelectItem value="oldest">Oldest first</SelectItem>
              <SelectItem value="unread">Unread first</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div class="flex items-center space-x-2">
          <Button variant="outline" size="sm">
            <CheckSquare class="h-4 w-4 mr-2" />
            Mark all as read
          </Button>
          <Button variant="ghost" size="sm" class="text-red-500 hover:text-red-600">
            <Trash2 class="h-4 w-4 mr-2" />
            Clear all
          </Button>
        </div>
      </div>
    </div>

    <!-- Notifications List -->
    <div class="space-y-3">
      <!-- Today Section -->
      <h2 class="text-sm font-medium text-muted-foreground px-2 mb-1">Today</h2>

      <!-- Job Match Notification - Unread -->
      <div
        class="p-4 bg-card rounded-lg border border-l-4 border-l-blue-500 shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center"
            >
              <Briefcase class="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">New Job Match: Frontend Developer at TechCorp</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  We found a new job that matches your profile with a 95% match score!
                </p>
              </div>
              <div class="ml-4 flex items-center space-x-1">
                <div class="h-2 w-2 rounded-full bg-blue-500 mr-2"></div>
                <div class="text-xs text-muted-foreground">2 hours ago</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="default">
                <Eye class="h-4 w-4 mr-2" />
                View Job
              </Button>
              <Button size="sm" variant="ghost">
                <Check class="h-4 w-4 mr-2" />
                Mark as read
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Application Update Notification - Unread -->
      <div
        class="p-4 bg-card rounded-lg border border-l-4 border-l-green-500 shadow-sm hover:shadow-md transition-shadow"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-green-100 dark:bg-green-900 flex items-center justify-center"
            >
              <ClipboardCheck class="h-5 w-5 text-green-600 dark:text-green-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">UI/UX Developer at Google: Interview Invitation</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  Your application has moved to the interview stage. Please confirm your
                  availability.
                </p>
              </div>
              <div class="ml-4 flex items-center space-x-1">
                <div class="h-2 w-2 rounded-full bg-blue-500 mr-2"></div>
                <div class="text-xs text-muted-foreground">5 hours ago</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="default">
                <Calendar class="h-4 w-4 mr-2" />
                Schedule Interview
              </Button>
              <Button size="sm" variant="ghost">
                <Check class="h-4 w-4 mr-2" />
                Mark as read
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Yesterday Section -->
      <h2 class="text-sm font-medium text-muted-foreground px-2 mb-1 mt-6">Yesterday</h2>

      <!-- System Notification - Read -->
      <div
        class="p-4 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow opacity-80"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-purple-100 dark:bg-purple-900 flex items-center justify-center"
            >
              <BellRing class="h-5 w-5 text-purple-600 dark:text-purple-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">Resume Analysis Complete</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  We've analyzed your resume. View your ATS score and optimization tips.
                </p>
              </div>
              <div class="ml-4 flex items-center">
                <div class="text-xs text-muted-foreground">Yesterday</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="outline">
                <FileText class="h-4 w-4 mr-2" />
                View Analysis
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Match Notification - Read -->
      <div
        class="p-4 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow opacity-80"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-blue-100 dark:bg-blue-900 flex items-center justify-center"
            >
              <Briefcase class="h-5 w-5 text-blue-600 dark:text-blue-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">New Job Match: Backend Developer at DataCorp</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  We found a new job that matches your profile with an 82% match score.
                </p>
              </div>
              <div class="ml-4 flex items-center">
                <div class="text-xs text-muted-foreground">Yesterday</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="outline">
                <Eye class="h-4 w-4 mr-2" />
                View Job
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- This Week Section -->
      <h2 class="text-sm font-medium text-muted-foreground px-2 mb-1 mt-6">This Week</h2>

      <!-- Application Update Notification - Read -->
      <div
        class="p-4 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow opacity-80"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-red-100 dark:bg-red-900 flex items-center justify-center"
            >
              <XCircle class="h-5 w-5 text-red-600 dark:text-red-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">Application Update: Full Stack Developer at Microsoft</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  Thank you for your interest, unfortunately we have decided to move forward with
                  other candidates.
                </p>
              </div>
              <div class="ml-4 flex items-center">
                <div class="text-xs text-muted-foreground">2 days ago</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="outline">
                <MessageSquare class="h-4 w-4 mr-2" />
                View Feedback
              </Button>
            </div>
          </div>
        </div>
      </div>

      <!-- Skill Development Notification - Read -->
      <div
        class="p-4 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow opacity-80"
      >
        <div class="flex">
          <div class="shrink-0 mr-4">
            <div
              class="h-10 w-10 rounded-full bg-amber-100 dark:bg-amber-900 flex items-center justify-center"
            >
              <Lightbulb class="h-5 w-5 text-amber-600 dark:text-amber-400" />
            </div>
          </div>
          <div class="flex-grow">
            <div class="flex items-center justify-between">
              <div>
                <h3 class="font-medium">Skill Gap Alert: React.js</h3>
                <p class="text-sm text-muted-foreground mt-1">
                  We noticed React.js is frequently requested in jobs matching your profile.
                  Consider adding this skill.
                </p>
              </div>
              <div class="ml-4 flex items-center">
                <div class="text-xs text-muted-foreground">3 days ago</div>
              </div>
            </div>
            <div class="mt-2 flex items-center space-x-2">
              <Button size="sm" variant="outline">
                <BookOpen class="h-4 w-4 mr-2" />
                View Resources
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-6 flex items-center justify-between">
      <div class="text-sm text-muted-foreground">
        Showing <span class="font-medium">1-6</span> of
        <span class="font-medium">12</span> notifications
      </div>
      <div class="flex items-center space-x-2">
        <Button variant="outline" size="sm" disabled>
          <ChevronLeft class="h-4 w-4 mr-1" />
          Previous
        </Button>
        <Button variant="outline" size="sm">
          Next
          <ChevronRight class="h-4 w-4 ml-1" />
        </Button>
      </div>
    </div>

    <!-- Settings Link -->
    <div class="mt-6 p-4 bg-slate-50 dark:bg-slate-900 rounded-lg text-center">
      <p class="text-sm text-muted-foreground">
        Want to customize your notification preferences?
        <RouterLink to="/dashboard/settings" class="text-primary font-medium hover:underline">
          Go to Settings
        </RouterLink>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  Bell,
  BellRing,
  Briefcase,
  ClipboardCheck,
  Calendar,
  FileText,
  Check,
  CheckSquare,
  Trash2,
  Eye,
  MessageSquare,
  XCircle,
  Lightbulb,
  BookOpen,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { RouterLink } from 'vue-router'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
</script>
