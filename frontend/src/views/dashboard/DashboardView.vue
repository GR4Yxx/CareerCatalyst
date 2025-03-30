// /src/views/dashboard/DashboardView.vue
<template>
  <div class="user-dashboard">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <LayoutDashboard class="h-7 w-7 mr-3 text-primary" />
      Dashboard
    </h1>

    <!-- Dashboard Overview Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
      <DashboardCard title="Welcome" :count="1">
        <User class="h-8 w-8" />
      </DashboardCard>
      <DashboardCard title="Resumes" :count="resumeCount" :loading="loading">
        <FileText class="h-8 w-8" />
      </DashboardCard>
      <DashboardCard title="Saved Jobs" :count="8">
        <Bookmark class="h-8 w-8" />
      </DashboardCard>
      <DashboardCard title="Applications" :count="5">
        <Send class="h-8 w-8" />
      </DashboardCard>
    </div>

    <!-- Activity and Stats Overview -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
      <!-- Quick Actions -->
      <div class="p-6 bg-card rounded-lg border shadow-sm col-span-1">
        <h2 class="text-xl font-semibold mb-4">Quick Actions</h2>
        <div class="space-y-4">
          <div
            class="p-4 rounded-lg bg-primary/10 hover:bg-primary/20 transition-colors flex items-center space-x-4 cursor-pointer"
            @click="navigateTo('/dashboard/job-finder')"
          >
            <Briefcase class="h-6 w-6 text-primary" />
            <div>
              <h3 class="font-medium">Find Job Matches</h3>
              <p class="text-sm text-muted-foreground">
                Discover opportunities aligned to your skills
              </p>
            </div>
          </div>

          <div
            class="p-4 rounded-lg bg-primary/10 hover:bg-primary/20 transition-colors flex items-center space-x-4 cursor-pointer"
            @click="navigateTo('/dashboard/skills')"
          >
            <Sparkles class="h-6 w-6 text-primary" />
            <div>
              <h3 class="font-medium">Analyze Skills</h3>
              <p class="text-sm text-muted-foreground">Extract skills from your resume</p>
            </div>
          </div>

          <div
            class="p-4 rounded-lg bg-primary/10 hover:bg-primary/20 transition-colors flex items-center space-x-4 cursor-pointer"
            @click="navigateTo('/dashboard/ats-intelligence')"
          >
            <Search class="h-6 w-6 text-primary" />
            <div>
              <h3 class="font-medium">ATS Intelligence</h3>
              <p class="text-sm text-muted-foreground">Optimize your resume for job applications</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Activity -->
      <div class="p-6 bg-card rounded-lg border shadow-sm col-span-1 lg:col-span-2">
        <h2 class="text-xl font-semibold mb-4">Recent Activity</h2>
        <div class="space-y-4">
          <div class="border-b pb-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="p-2 rounded-full bg-green-100 text-green-600">
                  <Sparkles class="h-4 w-4" />
                </div>
                <div>
                  <h3 class="font-medium">Skills Analyzed</h3>
                  <p class="text-sm text-muted-foreground">Resume skills successfully extracted</p>
                </div>
              </div>
              <span class="text-sm text-muted-foreground">2 hours ago</span>
            </div>
          </div>

          <div class="border-b pb-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="p-2 rounded-full bg-blue-100 text-blue-600">
                  <Bookmark class="h-4 w-4" />
                </div>
                <div>
                  <h3 class="font-medium">Job Saved</h3>
                  <p class="text-sm text-muted-foreground">Senior Developer at TechCorp</p>
                </div>
              </div>
              <span class="text-sm text-muted-foreground">Yesterday</span>
            </div>
          </div>

          <div class="border-b pb-4">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="p-2 rounded-full bg-amber-100 text-amber-600">
                  <FileUp class="h-4 w-4" />
                </div>
                <div>
                  <h3 class="font-medium">Resume Updated</h3>
                  <p class="text-sm text-muted-foreground">New version of your resume uploaded</p>
                </div>
              </div>
              <span class="text-sm text-muted-foreground">3 days ago</span>
            </div>
          </div>

          <div>
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-3">
                <div class="p-2 rounded-full bg-purple-100 text-purple-600">
                  <Send class="h-4 w-4" />
                </div>
                <div>
                  <h3 class="font-medium">Application Submitted</h3>
                  <p class="text-sm text-muted-foreground">Software Engineer at InnoTech</p>
                </div>
              </div>
              <span class="text-sm text-muted-foreground">5 days ago</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Skills & Job Matches Overview -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
      <!-- Skills Overview -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Skills Overview</h2>
          <Button variant="outline" size="sm" @click="navigateTo('/dashboard/skills')">
            View All
          </Button>
        </div>

        <div class="space-y-4">
          <div>
            <h3 class="text-sm font-medium text-muted-foreground mb-2">Technical Skills</h3>
            <div class="flex flex-wrap gap-2">
              <Badge>Vue.js</Badge>
              <Badge>TypeScript</Badge>
              <Badge>React</Badge>
              <Badge>Node.js</Badge>
              <Badge>Python</Badge>
            </div>
          </div>

          <div>
            <h3 class="text-sm font-medium text-muted-foreground mb-2">Soft Skills</h3>
            <div class="flex flex-wrap gap-2">
              <Badge variant="outline">Communication</Badge>
              <Badge variant="outline">Team Leadership</Badge>
              <Badge variant="outline">Problem Solving</Badge>
            </div>
          </div>
        </div>
      </div>

      <!-- Job Match Highlights -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-xl font-semibold">Top Job Matches</h2>
          <Button variant="outline" size="sm" @click="navigateTo('/dashboard/job-finder')">
            View All
          </Button>
        </div>

        <div class="space-y-4">
          <div class="flex items-center justify-between p-3 rounded-lg bg-primary/5">
            <div>
              <h3 class="font-medium">Senior Frontend Developer</h3>
              <p class="text-sm text-muted-foreground">TechCorp - Remote</p>
            </div>
            <Badge class="bg-green-500">92% Match</Badge>
          </div>

          <div class="flex items-center justify-between p-3 rounded-lg bg-primary/5">
            <div>
              <h3 class="font-medium">Full Stack Engineer</h3>
              <p class="text-sm text-muted-foreground">InnoTech - San Francisco</p>
            </div>
            <Badge class="bg-green-500">87% Match</Badge>
          </div>

          <div class="flex items-center justify-between p-3 rounded-lg bg-primary/5">
            <div>
              <h3 class="font-medium">UI/UX Developer</h3>
              <p class="text-sm text-muted-foreground">DesignHub - New York</p>
            </div>
            <Badge class="bg-amber-500">76% Match</Badge>
          </div>
        </div>
      </div>
    </div>

    <!-- Career Path Snapshot -->
    <div class="p-6 bg-card rounded-lg border shadow-sm mb-8">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-semibold">Career Progression</h2>
        <Button variant="outline" size="sm" @click="navigateTo('/dashboard/career-path')">
          View Full Path
        </Button>
      </div>

      <div class="relative">
        <div class="absolute left-6 top-0 bottom-0 w-0.5 bg-blue-500"></div>

        <div class="flex items-center mb-6 relative pl-14">
          <div
            class="absolute left-0 w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white"
          >
            <User class="h-6 w-6" />
          </div>
          <div>
            <h3 class="font-medium">Frontend Developer</h3>
            <p class="text-sm text-muted-foreground">Current Position</p>
          </div>
        </div>

        <div class="flex items-center relative pl-14">
          <div
            class="absolute left-0 w-12 h-12 rounded-full bg-slate-200 border-2 border-blue-500 flex items-center justify-center text-blue-500"
          >
            <Target class="h-6 w-6" />
          </div>
          <div>
            <h3 class="font-medium">Senior Developer</h3>
            <p class="text-sm text-muted-foreground">Next Goal (1-2 years)</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  LayoutDashboard,
  User,
  FileText,
  Bookmark,
  Send,
  Briefcase,
  Sparkles,
  Search,
  FileUp,
  Target,
} from 'lucide-vue-next'
import DashboardCard from '@/components/dashboard/DashboardCard.vue'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { resumeService } from '@/services/resumeService'

const resumeCount = ref(0)
const loading = ref(true)
const router = useRouter()

function navigateTo(path) {
  router.push(path)
}

onMounted(async () => {
  try {
    resumeCount.value = await resumeService.getUserResumeCount()
  } catch (error) {
    console.error('Failed to fetch resume count:', error)
  } finally {
    loading.value = false
  }
})
</script>
