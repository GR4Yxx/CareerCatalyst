<template>
  <div class="applications-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <ClipboardCheck class="h-7 w-7 mr-3 text-primary" />
      My Applications
    </h1>

    <!-- Filter and Sort Controls -->
    <div class="mb-6 p-4 bg-card rounded-lg border shadow-sm">
      <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
        <div class="flex items-center space-x-2">
          <Input placeholder="Search applications..." class="w-72" />
          <Button variant="secondary">
            <Search class="h-4 w-4 mr-2" />
            Search
          </Button>
        </div>

        <div class="flex items-center space-x-2">
          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Status" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Statuses</SelectItem>
              <SelectItem value="applied">Applied</SelectItem>
              <SelectItem value="screening">Screening</SelectItem>
              <SelectItem value="interview">Interview</SelectItem>
              <SelectItem value="offer">Offer</SelectItem>
              <SelectItem value="rejected">Rejected</SelectItem>
            </SelectContent>
          </Select>

          <Select>
            <SelectTrigger class="w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="date-new">Date applied (newest)</SelectItem>
              <SelectItem value="date-old">Date applied (oldest)</SelectItem>
              <SelectItem value="company-asc">Company (A-Z)</SelectItem>
              <SelectItem value="company-desc">Company (Z-A)</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>

    <!-- Applications List -->
    <div class="space-y-4">
      <!-- Application 1: Interview Stage -->
      <div
        class="p-6 bg-card rounded-lg border border-l-4 border-l-blue-500 shadow-sm hover:shadow-md transition-shadow"
      >
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
                <Badge class="bg-blue-500">Interview</Badge>
              </div>
              <p class="text-muted-foreground mt-1">TechCorp Inc.</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Remote / New York, NY</span>
                </div>
                <div class="flex items-center">
                  <Calendar class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Applied on Sep 15, 2023</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4">
          <div class="relative">
            <div class="absolute left-0 top-0 h-full w-0.5 bg-slate-200 dark:bg-slate-700"></div>

            <div class="ml-6 space-y-6">
              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Application Submitted</h3>
                <p class="text-sm text-muted-foreground">Sep 15, 2023</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Resume Screened</h3>
                <p class="text-sm text-muted-foreground">Sep 18, 2023</p>
                <p class="text-sm mt-1">Your resume passed the initial screening.</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-blue-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Technical Interview</h3>
                <p class="text-sm text-muted-foreground">Scheduled for Sep 28, 2023</p>
                <div class="flex mt-2 space-x-2">
                  <Button size="sm" variant="outline">
                    <Calendar class="h-4 w-4 mr-2" />
                    Add to Calendar
                  </Button>
                  <Button size="sm" variant="outline">
                    <FileText class="h-4 w-4 mr-2" />
                    View Details
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Application 2: Rejected -->
      <div
        class="p-6 bg-card rounded-lg border border-l-4 border-l-red-500 shadow-sm hover:shadow-md transition-shadow"
      >
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
                <Badge variant="destructive">Rejected</Badge>
              </div>
              <p class="text-muted-foreground mt-1">Microsoft</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Redmond, WA</span>
                </div>
                <div class="flex items-center">
                  <Calendar class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Applied on Aug 28, 2023</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4">
          <div class="relative">
            <div class="absolute left-0 top-0 h-full w-0.5 bg-slate-200 dark:bg-slate-700"></div>

            <div class="ml-6 space-y-6">
              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Application Submitted</h3>
                <p class="text-sm text-muted-foreground">Aug 28, 2023</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-red-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Application Rejected</h3>
                <p class="text-sm text-muted-foreground">Sep 10, 2023</p>
                <p class="text-sm mt-1">
                  Thank you for your interest. We've decided to proceed with other candidates.
                </p>
                <div
                  class="p-3 bg-red-50 dark:bg-red-950/20 border border-red-200 dark:border-red-900 rounded-md mt-2"
                >
                  <h4 class="text-sm font-medium text-red-800 dark:text-red-300">Feedback</h4>
                  <p class="text-sm text-red-700 dark:text-red-400 mt-1">
                    Your experience with .NET framework appears limited compared to our
                    requirements. Consider gaining more experience with C# and Azure cloud services
                    for future applications.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Application 3: Offer -->
      <div
        class="p-6 bg-card rounded-lg border border-l-4 border-l-green-500 shadow-sm hover:shadow-md transition-shadow"
      >
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
                <Badge className="bg-green-500 text-white">Offer</Badge>
              </div>
              <p class="text-muted-foreground mt-1">Google</p>
              <div class="flex items-center text-sm mt-2 space-x-4">
                <div class="flex items-center">
                  <MapPin class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Mountain View, CA</span>
                </div>
                <div class="flex items-center">
                  <Calendar class="h-4 w-4 mr-1 text-muted-foreground" />
                  <span>Applied on Aug 10, 2023</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="mt-4">
          <div class="relative">
            <div class="absolute left-0 top-0 h-full w-0.5 bg-slate-200 dark:bg-slate-700"></div>

            <div class="ml-6 space-y-6">
              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Application Submitted</h3>
                <p class="text-sm text-muted-foreground">Aug 10, 2023</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Phone Screening</h3>
                <p class="text-sm text-muted-foreground">Aug 15, 2023</p>
                <p class="text-sm mt-1">Initial screening with HR completed successfully.</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Technical Interview</h3>
                <p class="text-sm text-muted-foreground">Aug 22, 2023</p>
                <p class="text-sm mt-1">You passed the technical interview round.</p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Final Round</h3>
                <p class="text-sm text-muted-foreground">Sep 5, 2023</p>
                <p class="text-sm mt-1">
                  Successfully completed the final interview with the team lead.
                </p>
              </div>

              <div class="relative">
                <div
                  class="absolute -left-[25px] w-5 h-5 rounded-full bg-green-500 border-2 border-background flex items-center justify-center"
                ></div>
                <h3 class="font-medium">Offer Received</h3>
                <p class="text-sm text-muted-foreground">Sep 12, 2023</p>
                <div
                  class="p-3 bg-green-50 dark:bg-green-950/20 border border-green-200 dark:border-green-900 rounded-md mt-2"
                >
                  <h4 class="text-sm font-medium text-green-800 dark:text-green-300">
                    Offer Details
                  </h4>
                  <p class="text-sm text-green-700 dark:text-green-400 mt-1">
                    Base Salary: $120,000/year<br />
                    Equity: RSUs worth $40,000 vesting over 4 years<br />
                    Signing Bonus: $10,000<br />
                    Start Date: October 15, 2023
                  </p>
                </div>
                <div class="flex mt-3 space-x-2">
                  <Button size="sm" variant="default">
                    <Check class="h-4 w-4 mr-2" />
                    Accept Offer
                  </Button>
                  <Button size="sm" variant="outline">
                    <FileText class="h-4 w-4 mr-2" />
                    View Details
                  </Button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Application Stats -->
    <div class="mt-6 p-6 bg-card rounded-lg border shadow-sm">
      <h2 class="text-xl font-semibold mb-4">Application Statistics</h2>

      <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="p-4 border rounded-lg">
          <h3 class="text-sm font-medium text-muted-foreground mb-1">Total Applications</h3>
          <p class="text-2xl font-bold">15</p>
        </div>

        <div class="p-4 border rounded-lg">
          <h3 class="text-sm font-medium text-muted-foreground mb-1">Interviews</h3>
          <p class="text-2xl font-bold">5</p>
          <p class="text-xs text-muted-foreground">33% interview rate</p>
        </div>

        <div class="p-4 border rounded-lg">
          <h3 class="text-sm font-medium text-muted-foreground mb-1">Offers</h3>
          <p class="text-2xl font-bold text-green-500">2</p>
          <p class="text-xs text-muted-foreground">13% offer rate</p>
        </div>

        <div class="p-4 border rounded-lg">
          <h3 class="text-sm font-medium text-muted-foreground mb-1">Average Response Time</h3>
          <p class="text-2xl font-bold">5.2 <span class="text-base font-normal">days</span></p>
        </div>
      </div>

      <div class="mt-4">
        <Button variant="outline" size="sm">
          <FileText class="h-4 w-4 mr-2" />
          View Detailed Report
        </Button>
      </div>
    </div>

    <!-- Pagination -->
    <div class="mt-6 flex items-center justify-between">
      <div class="text-sm text-muted-foreground">
        Showing <span class="font-medium">1-3</span> of
        <span class="font-medium">15</span> applications
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
  ClipboardCheck,
  Search,
  MapPin,
  Calendar,
  FileText,
  Check,
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
