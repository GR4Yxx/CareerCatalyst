<template>
  <div class="career-path-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Map class="h-7 w-7 mr-3 text-primary" />
      Career Path
    </h1>

    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Career Trajectory Visualization</h2>
        <p class="mb-4">
          Visualize potential career paths based on your current skills and experience. Discover
          what skills you need to develop to reach your career goals.
        </p>
        <p class="mb-4">Set your target role to see a personalized career progression plan.</p>
        <div class="flex items-center space-x-4 mt-4">
          <Input placeholder="Target role (e.g. CTO, Senior Developer)" class="max-w-md" />
          <Button>Set Goal</Button>
        </div>
      </div>
    </div>

    <div class="p-6 bg-card rounded-lg border shadow-sm mb-6">
      <h3 class="text-lg font-semibold mb-6">Your Career Pathway</h3>

      <div class="relative">
        <!-- Career Path Timeline -->
        <div class="absolute left-6 top-0 bottom-0 w-0.5 bg-blue-500"></div>

        <div class="space-y-8">
          <!-- Current Position -->
          <div class="relative pl-14">
            <div
              class="absolute left-0 w-12 h-12 rounded-full bg-blue-500 flex items-center justify-center text-white"
            >
              <User class="h-6 w-6" />
            </div>
            <div>
              <h4 class="text-md font-semibold">Frontend Developer</h4>
              <p class="text-sm text-muted-foreground">Current Position</p>
              <p class="text-sm mt-1">Building web applications with Vue.js and TypeScript.</p>
            </div>
          </div>

          <!-- Next Step -->
          <div class="relative pl-14">
            <div
              class="absolute left-0 w-12 h-12 rounded-full bg-slate-200 border-2 border-blue-500 flex items-center justify-center text-blue-500"
            >
              <Code2 class="h-6 w-6" />
            </div>
            <div>
              <h4 class="text-md font-semibold">Senior Frontend Developer</h4>
              <p class="text-sm text-muted-foreground">1-2 Years</p>
              <p class="text-sm mt-1">Lead frontend development of complex applications.</p>
              <div class="mt-2">
                <h5 class="text-sm font-medium mb-1">Skills to Develop:</h5>
                <div class="flex flex-wrap gap-2">
                  <Badge variant="outline">Team Leadership</Badge>
                  <Badge variant="outline">Architecture Design</Badge>
                  <Badge variant="outline">Performance Optimization</Badge>
                </div>
              </div>
            </div>
          </div>

          <!-- Future Step -->
          <div class="relative pl-14">
            <div
              class="absolute left-0 w-12 h-12 rounded-full bg-slate-200 border-2 border-blue-500 flex items-center justify-center text-blue-500"
            >
              <Users class="h-6 w-6" />
            </div>
            <div>
              <h4 class="text-md font-semibold">Lead Developer</h4>
              <p class="text-sm text-muted-foreground">3-4 Years</p>
              <p class="text-sm mt-1">Oversee development team and technical direction.</p>
              <div class="mt-2">
                <h5 class="text-sm font-medium mb-1">Skills to Develop:</h5>
                <div class="flex flex-wrap gap-2">
                  <Badge variant="outline">Project Management</Badge>
                  <Badge variant="outline">Mentoring</Badge>
                  <Badge variant="outline">Technical Strategy</Badge>
                </div>
              </div>
            </div>
          </div>

          <!-- Target Role -->
          <div class="relative pl-14">
            <div
              class="absolute left-0 w-12 h-12 rounded-full bg-purple-500 flex items-center justify-center text-white"
            >
              <Target class="h-6 w-6" />
            </div>
            <div>
              <h4 class="text-md font-semibold">CTO</h4>
              <p class="text-sm text-muted-foreground">Goal Position</p>
              <p class="text-sm mt-1">
                Lead technical vision and strategy for the entire organization.
              </p>
              <div class="mt-2">
                <h5 class="text-sm font-medium mb-1">Required Skills:</h5>
                <div class="flex flex-wrap gap-2">
                  <Badge variant="outline">Executive Leadership</Badge>
                  <Badge variant="outline">Business Strategy</Badge>
                  <Badge variant="outline">Technical Vision</Badge>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Map, User, Code2, Users, Target } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
</script>
