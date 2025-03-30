<template>
  <div class="saved-jobs-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <Briefcase class="h-7 w-7 mr-3 text-primary" />
      Saved Jobs
    </h1>

    <!-- Filter and Sort Controls -->
    <div class="mb-6 p-4 bg-card rounded-lg border shadow-sm">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="flex items-center space-x-2">
          <Input placeholder="Search saved jobs..." class="w-72" />
          <Button variant="secondary">
            <Search class="h-4 w-4 mr-2" />
            Search
          </Button>
        </div>

        <div class="flex items-center space-x-2">
          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Job type" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Types</SelectItem>
              <SelectItem value="full-time">Full-time</SelectItem>
              <SelectItem value="part-time">Part-time</SelectItem>
              <SelectItem value="contract">Contract</SelectItem>
              <SelectItem value="remote">Remote</SelectItem>
            </SelectContent>
          </Select>

          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="date-new">Date added (newest)</SelectItem>
              <SelectItem value="date-old">Date added (oldest)</SelectItem>
              <SelectItem value="match-high">Match score (high-low)</SelectItem>
              <SelectItem value="match-low">Match score (low-high)</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>

    <!-- Job List -->
    <div class="space-y-4">
      <!-- Job Card 1 -->
      <div class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex items-start">
            <div class="bg-white p-2 rounded-lg border mr-4">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/thumb/9/95/Vue.js_Logo_2.svg/512px-Vue.js_Logo_2.svg.png"
                alt="Vue.js Logo"
                class="h-12 w-12 object-contain"
              />
            </div>
            <div>
              <div class="flex items-center">
                <h2 class="text-xl font-semibold mr-3">Senior Frontend Developer</h2>
                <Badge variant="success">95% Match</Badge>
                <Badge variant="outline" class="ml-2">Saved 2 days ago</Badge>
              </div>
              <p class="text-muted-foreground mt-1">TechCorp Inc.</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Remote / New York, NY</span>
                </div>
                <div class="flex items-center">
                  <Clock class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Full-time</span>
                </div>
                <div class="flex items-center">
                  <DollarSign class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>$120,000 - $150,000</span>
                </div>
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <Button variant="ghost" size="icon">
              <Bookmark class="h-5 w-5 fill-current" />
            </Button>
          </div>
        </div>

        <div class="mt-4">
          <h3 class="font-medium mb-2">Job Description</h3>
          <p class="text-sm mb-4">
            We're looking for a Senior Frontend Developer with experience in Vue.js, TypeScript, and
            modern web development practices. The ideal candidate will have a strong understanding
            of frontend architecture and be able to mentor junior developers.
          </p>
          <div class="flex flex-wrap gap-2 mb-4">
            <Badge variant="secondary">Vue.js</Badge>
            <Badge variant="secondary">TypeScript</Badge>
            <Badge variant="secondary">JavaScript</Badge>
            <Badge variant="secondary">HTML/CSS</Badge>
            <Badge variant="secondary">Git</Badge>
          </div>
          <div class="flex space-x-2">
            <Button variant="outline" size="sm">
              <ExternalLink class="h-4 w-4 mr-2" />
              View Details
            </Button>
            <Button size="sm">
              <Send class="h-4 w-4 mr-2" />
              Apply Now
            </Button>
          </div>
        </div>
      </div>

      <!-- Job Card 2 -->
      <div class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex items-start">
            <div class="bg-white p-2 rounded-lg border mr-4">
              <img
                src="https://logosandtypes.com/wp-content/uploads/2020/08/google.svg"
                alt="Google Logo"
                class="h-12 w-12 object-contain"
              />
            </div>
            <div>
              <div class="flex items-center">
                <h2 class="text-xl font-semibold mr-3">UI/UX Developer</h2>
                <Badge variant="success">87% Match</Badge>
                <Badge variant="outline" class="ml-2">Saved 1 week ago</Badge>
              </div>
              <p class="text-muted-foreground mt-1">Google</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Mountain View, CA</span>
                </div>
                <div class="flex items-center">
                  <Clock class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Full-time</span>
                </div>
                <div class="flex items-center">
                  <DollarSign class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>$110,000 - $140,000</span>
                </div>
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <Button variant="ghost" size="icon">
              <Bookmark class="h-5 w-5 fill-current" />
            </Button>
          </div>
        </div>

        <div class="mt-4">
          <h3 class="font-medium mb-2">Job Description</h3>
          <p class="text-sm mb-4">
            Join our team as a UI/UX Developer to create beautiful, responsive interfaces that
            delight users. You'll work closely with product managers, designers, and engineers to
            implement engaging user experiences.
          </p>
          <div class="flex flex-wrap gap-2 mb-4">
            <Badge variant="secondary">UI/UX</Badge>
            <Badge variant="secondary">JavaScript</Badge>
            <Badge variant="secondary">CSS</Badge>
            <Badge variant="secondary">Design Systems</Badge>
          </div>
          <div class="flex space-x-2">
            <Button variant="outline" size="sm">
              <ExternalLink class="h-4 w-4 mr-2" />
              View Details
            </Button>
            <Button size="sm">
              <Send class="h-4 w-4 mr-2" />
              Apply Now
            </Button>
          </div>
        </div>
      </div>

      <!-- Job Card 3 -->
      <div class="p-6 bg-card rounded-lg border shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between">
          <div class="flex items-start">
            <div class="bg-white p-2 rounded-lg border mr-4">
              <img
                src="https://upload.wikimedia.org/wikipedia/commons/f/fa/Microsoft_logo.svg"
                alt="Microsoft Logo"
                class="h-12 w-12 object-contain"
              />
            </div>
            <div>
              <div class="flex items-center">
                <h2 class="text-xl font-semibold mr-3">Full Stack Developer</h2>
                <Badge variant="warning">72% Match</Badge>
                <Badge variant="outline" class="ml-2">Saved 2 weeks ago</Badge>
              </div>
              <p class="text-muted-foreground mt-1">Microsoft</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Redmond, WA</span>
                </div>
                <div class="flex items-center">
                  <Clock class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Full-time</span>
                </div>
                <div class="flex items-center">
                  <DollarSign class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>$125,000 - $160,000</span>
                </div>
              </div>
            </div>
          </div>
          <div class="flex items-center">
            <Button variant="ghost" size="icon">
              <Bookmark class="h-5 w-5 fill-current" />
            </Button>
          </div>
        </div>

        <div class="mt-4">
          <h3 class="font-medium mb-2">Job Description</h3>
          <p class="text-sm mb-4">
            We are seeking a Full Stack Developer to join our team and contribute to building
            scalable web applications. The ideal candidate will have experience with both frontend
            and backend technologies.
          </p>
          <div class="flex flex-wrap gap-2 mb-4">
            <Badge variant="secondary">React</Badge>
            <Badge variant="secondary">Node.js</Badge>
            <Badge variant="secondary">C#</Badge>
            <Badge variant="secondary">.NET</Badge>
            <Badge variant="secondary">Azure</Badge>
          </div>
          <div class="flex space-x-2">
            <Button variant="outline" size="sm">
              <ExternalLink class="h-4 w-4 mr-2" />
              View Details
            </Button>
            <Button size="sm">
              <Send class="h-4 w-4 mr-2" />
              Apply Now
            </Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-6 flex items-center justify-between">
      <div class="text-sm text-muted-foreground">
        Showing <span class="font-medium">1-3</span> of <span class="font-medium">12</span> saved
        jobs
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
  </div>
</template>

<script setup lang="ts">
import {
  Briefcase,
  Search,
  Bookmark,
  MapPin,
  Clock,
  DollarSign,
  ExternalLink,
  Send,
  ChevronLeft,
  ChevronRight,
} from 'lucide-vue-next'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Badge } from '@/components/ui/badge'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
</script>
