<template>
  <div class="ats-intelligence-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <FileSearch class="h-7 w-7 mr-3 text-primary" />
      ATS Intelligence
    </h1>

    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Resume Optimization</h2>
        <p class="mb-4">
          Tailor your resume to increase visibility with Applicant Tracking Systems. Our ATS
          intelligence system helps you optimize your resume for each job application.
        </p>
        <div class="flex items-center space-x-4 mt-4">
          <Input placeholder="Paste job description..." class="max-w-md" />
          <Button>Analyze</Button>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h3 class="text-lg font-semibold mb-3">ATS Compatibility Score</h3>
        <div class="flex items-center mb-4">
          <div
            class="w-16 h-16 rounded-full bg-blue-500 flex items-center justify-center text-white font-bold text-2xl"
          >
            72%
          </div>
          <div class="ml-4">
            <p class="text-sm text-muted-foreground">Your resume is somewhat optimized for ATS</p>
          </div>
        </div>
        <h4 class="font-medium mb-2">Suggested Improvements:</h4>
        <ul class="space-y-2 text-sm">
          <li class="flex items-start">
            <AlertCircle class="h-4 w-4 mr-2 text-red-500 mt-0.5" />
            <span>Add more specific technical skills relevant to the job description</span>
          </li>
          <li class="flex items-start">
            <AlertCircle class="h-4 w-4 mr-2 text-red-500 mt-0.5" />
            <span>Use more industry standard terminology in your experience section</span>
          </li>
          <li class="flex items-start">
            <CheckCircle2 class="h-4 w-4 mr-2 text-green-500 mt-0.5" />
            <span>Your resume format is ATS-friendly</span>
          </li>
        </ul>
      </div>

      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h3 class="text-lg font-semibold mb-3">Keyword Analysis</h3>
        <p class="text-sm text-muted-foreground mb-4">
          Keywords found in the job description vs. your resume
        </p>
        <div class="space-y-3">
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span>Vue.js</span>
              <span class="text-green-500">Found</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
              <div class="bg-green-500 h-2 rounded-full" style="width: 100%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span>TypeScript</span>
              <span class="text-green-500">Found</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
              <div class="bg-green-500 h-2 rounded-full" style="width: 100%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span>CI/CD Experience</span>
              <span class="text-red-500">Missing</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
              <div class="bg-red-500 h-2 rounded-full" style="width: 0%"></div>
            </div>
          </div>
          <div>
            <div class="flex justify-between text-sm mb-1">
              <span>Agile Development</span>
              <span class="text-amber-500">Partial</span>
            </div>
            <div class="w-full bg-slate-200 rounded-full h-2">
              <div class="bg-amber-500 h-2 rounded-full" style="width: 60%"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { FileSearch, AlertCircle, CheckCircle2 } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
</script>
