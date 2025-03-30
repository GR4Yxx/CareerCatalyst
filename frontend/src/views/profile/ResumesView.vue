<template>
  <div class="resumes-view">
    <h1 class="text-2xl font-bold mb-6 flex items-center">
      <FileText class="h-7 w-7 mr-3 text-primary" />
      My Resumes
    </h1>

    <div class="grid grid-cols-1 gap-6">
      <!-- Upload Section -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Upload Resume</h2>
        </div>

        <div
          class="border-2 border-dashed border-slate-300 dark:border-slate-700 rounded-lg p-8 text-center"
        >
          <div class="mx-auto flex flex-col items-center justify-center">
            <Upload class="h-10 w-10 text-muted-foreground mb-4" />
            <h3 class="font-medium mb-1">Drag & drop your resume</h3>
            <p class="text-sm text-muted-foreground mb-4">
              Support for PDF, DOCX, or TXT file formats
            </p>
            <Button>
              <Plus class="h-4 w-4 mr-2" />
              Select File
            </Button>
          </div>
        </div>
      </div>

      <!-- Resume List -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">My Resumes</h2>
          <div class="flex items-center space-x-2">
            <Input placeholder="Search resumes..." class="w-60" />
            <Select>
              <SelectTrigger class="w-40">
                <SelectValue placeholder="Sort by" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="date-new">Newest first</SelectItem>
                <SelectItem value="date-old">Oldest first</SelectItem>
                <SelectItem value="name-asc">Name (A-Z)</SelectItem>
                <SelectItem value="name-desc">Name (Z-A)</SelectItem>
              </SelectContent>
            </Select>
          </div>
        </div>

        <div class="space-y-4">
          <!-- Resume Item 1 -->
          <div class="border rounded-lg p-4 hover:border-primary transition-colors">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="p-2 bg-blue-100 dark:bg-blue-900 rounded-lg mr-4">
                  <FileText class="h-6 w-6 text-blue-600 dark:text-blue-400" />
                </div>
                <div>
                  <h3 class="font-medium">Software_Developer_Resume.pdf</h3>
                  <div class="flex items-center text-xs text-muted-foreground mt-1">
                    <span>PDF • 256KB</span>
                    <Circle class="h-1 w-1 mx-2 fill-current" />
                    <span>Uploaded 2 days ago</span>
                    <Badge class="ml-2" variant="success">Primary</Badge>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-1">
                <Button variant="ghost" size="icon">
                  <Eye class="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <Download class="h-4 w-4" />
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <FileEdit class="h-4 w-4 mr-2" />
                      Rename
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Check class="h-4 w-4 mr-2" />
                      Set as primary
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem class="text-red-600">
                      <Trash class="h-4 w-4 mr-2" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>

            <div class="mt-4 space-y-1">
              <div class="flex justify-between text-sm">
                <span>ATS Score</span>
                <span class="font-medium">78/100</span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
                <div class="bg-blue-600 h-1.5 rounded-full" style="width: 78%"></div>
              </div>
            </div>
          </div>

          <!-- Resume Item 2 -->
          <div class="border rounded-lg p-4 hover:border-primary transition-colors">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="p-2 bg-green-100 dark:bg-green-900 rounded-lg mr-4">
                  <FileText class="h-6 w-6 text-green-600 dark:text-green-400" />
                </div>
                <div>
                  <h3 class="font-medium">Frontend_Developer_Resume.docx</h3>
                  <div class="flex items-center text-xs text-muted-foreground mt-1">
                    <span>DOCX • 124KB</span>
                    <Circle class="h-1 w-1 mx-2 fill-current" />
                    <span>Uploaded 2 weeks ago</span>
                  </div>
                </div>
              </div>
              <div class="flex items-center space-x-1">
                <Button variant="ghost" size="icon">
                  <Eye class="h-4 w-4" />
                </Button>
                <Button variant="ghost" size="icon">
                  <Download class="h-4 w-4" />
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <MoreVertical class="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem>
                      <FileEdit class="h-4 w-4 mr-2" />
                      Rename
                    </DropdownMenuItem>
                    <DropdownMenuItem>
                      <Check class="h-4 w-4 mr-2" />
                      Set as primary
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem class="text-red-600">
                      <Trash class="h-4 w-4 mr-2" />
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>

            <div class="mt-4 space-y-1">
              <div class="flex justify-between text-sm">
                <span>ATS Score</span>
                <span class="font-medium">65/100</span>
              </div>
              <div class="w-full bg-slate-200 dark:bg-slate-700 rounded-full h-1.5">
                <div class="bg-amber-500 h-1.5 rounded-full" style="width: 65%"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Resume Stats -->
      <div class="p-6 bg-card rounded-lg border shadow-sm">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-semibold">Resume Analytics</h2>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Top Skills</h3>
            <div class="space-y-1.5">
              <div class="flex justify-between text-sm">
                <span>Vue.js</span>
                <span class="font-medium">Advanced</span>
              </div>
              <div class="flex justify-between text-sm">
                <span>TypeScript</span>
                <span class="font-medium">Intermediate</span>
              </div>
              <div class="flex justify-between text-sm">
                <span>UI/UX Design</span>
                <span class="font-medium">Intermediate</span>
              </div>
            </div>
          </div>

          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Skills Gaps</h3>
            <div class="space-y-1.5">
              <div class="flex justify-between text-sm">
                <span>React.js</span>
                <span class="text-amber-500">Missing</span>
              </div>
              <div class="flex justify-between text-sm">
                <span>CI/CD</span>
                <span class="text-amber-500">Missing</span>
              </div>
              <div class="flex justify-between text-sm">
                <span>Node.js</span>
                <span class="text-amber-500">Missing</span>
              </div>
            </div>
          </div>

          <div class="p-4 border rounded-lg">
            <h3 class="text-lg font-medium mb-2">Improvement Tips</h3>
            <ul class="space-y-1.5 text-sm">
              <li class="flex items-start">
                <ArrowRight class="h-4 w-4 mr-1 mt-0.5 text-blue-500" />
                <span>Add quantifiable achievements</span>
              </li>
              <li class="flex items-start">
                <ArrowRight class="h-4 w-4 mr-1 mt-0.5 text-blue-500" />
                <span>Update work experience dates</span>
              </li>
              <li class="flex items-start">
                <ArrowRight class="h-4 w-4 mr-1 mt-0.5 text-blue-500" />
                <span>Add a personal summary</span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {
  FileText,
  Upload,
  Plus,
  Eye,
  Download,
  MoreVertical,
  FileEdit,
  Check,
  Trash,
  Circle,
  ArrowRight,
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
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'
</script>
