<template>
  <div class="skills-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Sparkles class="h-7 w-7 mr-3 text-primary" />
      Skills Intelligence
    </h1>

    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Skills Extraction and Analysis</h2>
        <p class="mb-4">
          Extract, categorize, and contextualize skills from your resume. Understand how your skills
          align with job market demands.
        </p>
        <p class="mb-4">
          Upload your resume to get started with a comprehensive analysis of your skillset.
        </p>
        <Button disabled class="mt-2">Upload Resume</Button>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h3 class="text-lg font-semibold mb-3">Technical Skills</h3>
        <p class="text-sm text-muted-foreground mb-4">
          Your technical competencies and hard skills
        </p>
        <div class="flex flex-wrap gap-2">
          <Badge>JavaScript</Badge>
          <Badge>Vue.js</Badge>
          <Badge>TypeScript</Badge>
          <Badge>CSS</Badge>
          <Badge>HTML</Badge>
          <Badge>UI/UX Design</Badge>
          <Badge>Git</Badge>
        </div>
      </div>

      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h3 class="text-lg font-semibold mb-3">Soft Skills</h3>
        <p class="text-sm text-muted-foreground mb-4">Your interpersonal and transferable skills</p>
        <div class="flex flex-wrap gap-2">
          <Badge variant="outline">Communication</Badge>
          <Badge variant="outline">Leadership</Badge>
          <Badge variant="outline">Problem Solving</Badge>
          <Badge variant="outline">Teamwork</Badge>
          <Badge variant="outline">Time Management</Badge>
          <Badge variant="outline">Critical Thinking</Badge>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Sparkles } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
</script>
