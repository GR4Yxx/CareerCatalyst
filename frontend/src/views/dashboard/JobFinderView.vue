<template>
  <div class="job-finder-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Briefcase class="h-7 w-7 mr-3 text-primary" />
      Job Finder
    </h1>

    <div class="mb-8">
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <h2 class="text-xl font-semibold mb-4">Job Recommendations</h2>
        <p class="mb-4">
          Discover job opportunities matched to your skills and experience. Our recommendation
          engine takes into account both direct matches and adjacent skill sets.
        </p>
        <div class="flex items-center space-x-4 mt-4">
          <Input placeholder="Search jobs..." class="max-w-md" />
          <Button>Search</Button>
        </div>
      </div>
    </div>

    <div class="space-y-4">
      <div class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">Senior Frontend Developer</h3>
          <Badge>95% Match</Badge>
        </div>
        <p class="text-sm mb-2"><strong>Company:</strong> TechCorp Inc.</p>
        <p class="text-sm mb-2"><strong>Location:</strong> Remote / New York, NY</p>
        <p class="text-sm mb-4"><strong>Salary:</strong> $120,000 - $150,000</p>
        <p class="text-sm text-muted-foreground mb-4">
          We're looking for a Senior Frontend Developer with experience in Vue.js, TypeScript, and
          modern web development practices...
        </p>
        <div class="flex flex-wrap gap-2 mb-4">
          <Badge variant="secondary">Vue.js</Badge>
          <Badge variant="secondary">TypeScript</Badge>
          <Badge variant="secondary">JavaScript</Badge>
          <Badge variant="secondary">HTML/CSS</Badge>
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm">View Details</Button>
          <Button size="sm">Apply Now</Button>
        </div>
      </div>

      <div class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold">UI/UX Developer</h3>
          <Badge>87% Match</Badge>
        </div>
        <p class="text-sm mb-2"><strong>Company:</strong> DesignWave Studio</p>
        <p class="text-sm mb-2"><strong>Location:</strong> Remote / San Francisco, CA</p>
        <p class="text-sm mb-4"><strong>Salary:</strong> $100,000 - $130,000</p>
        <p class="text-sm text-muted-foreground mb-4">
          Join our team as a UI/UX Developer to create beautiful, responsive interfaces that delight
          users...
        </p>
        <div class="flex flex-wrap gap-2 mb-4">
          <Badge variant="secondary">UI/UX</Badge>
          <Badge variant="secondary">JavaScript</Badge>
          <Badge variant="secondary">CSS</Badge>
          <Badge variant="secondary">Design Systems</Badge>
        </div>
        <div class="flex space-x-2">
          <Button variant="outline" size="sm">View Details</Button>
          <Button size="sm">Apply Now</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Briefcase } from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Input } from '@/components/ui/input'
</script>
