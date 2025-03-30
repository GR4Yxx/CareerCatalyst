import api from '@/lib/api'
import { AxiosError } from 'axios'

interface AtsAnalysisResult {
  score: number
  suggestions: Array<{
    type: 'success' | 'warning'
    message: string
  }>
  keywordAnalysis: Array<{
    name: string
    found: boolean
  }>
}

interface OptimizedResume {
  latexCode: string
  pdfUrl?: string
}

class AtsService {
  /**
   * Analyze a resume against a job description
   */
  async analyzeResume(resumeId: string, jobDescription: string): Promise<AtsAnalysisResult> {
    try {
      const response = await api.post('/ats/analyze', {
        resumeId,
        jobDescription,
      })
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError) {
        console.error('Error analyzing resume:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
        })

        // Return mock data for now
        return this.getMockAnalysisResult()
      }
      throw error
    }
  }

  /**
   * Generate an optimized resume based on a job description
   */
  async generateOptimizedResume(
    resumeId: string,
    jobDescription: string,
    requiredSkills: string[],
  ): Promise<OptimizedResume> {
    try {
      const response = await api.post('/ats/optimize-resume', {
        resumeId,
        jobDescription,
        requiredSkills,
      })
      return response.data
    } catch (error: unknown) {
      if (error instanceof AxiosError) {
        console.error('Error generating optimized resume:', {
          status: error.response?.status,
          statusText: error.response?.statusText,
          data: error.response?.data,
        })

        // Return mock data
        return {
          latexCode: this.getMockLatexResume('user@example.com', requiredSkills, jobDescription),
        }
      }
      throw error
    }
  }

  /**
   * Convert LaTeX code to PDF
   */
  async convertLatexToPdf(latexCode: string): Promise<Blob> {
    try {
      const response = await api.post(
        '/ats/latex-to-pdf',
        { latex: latexCode },
        { responseType: 'blob' },
      )
      return response.data
    } catch (error) {
      console.error('Error converting LaTeX to PDF:', error)
      // Create a mock PDF blob for development
      return new Blob(['PDF data would be here'], { type: 'application/pdf' })
    }
  }

  /**
   * Get mock analysis result
   */
  private getMockAnalysisResult(): AtsAnalysisResult {
    return {
      score: 72,
      suggestions: [
        {
          type: 'warning',
          message: 'Add more specific technical skills relevant to the job description',
        },
        {
          type: 'warning',
          message: 'Use more industry standard terminology in your experience section',
        },
        {
          type: 'success',
          message: 'Your resume format is ATS-friendly',
        },
      ],
      keywordAnalysis: [
        { name: 'Vue.js', found: true },
        { name: 'TypeScript', found: true },
        { name: 'CI/CD Experience', found: false },
        { name: 'Agile Development', found: true },
      ],
    }
  }

  /**
   * Get mock LaTeX resume
   */
  private getMockLatexResume(email: string, requiredSkills: string[], jobDesc: string): string {
    // Using the same template as in the component
    return `%-------------------------
% Resume in Latex
% Author : Joshua
% License : MIT
%------------------------

\\documentclass[letterpaper,11pt]{article}

\\usepackage{latexsym}
\\usepackage[empty]{fullpage}
\\usepackage{titlesec}
\\usepackage{marvosym}
\\usepackage[usenames,dvipsnames]{color}
\\usepackage{verbatim}
\\usepackage{enumitem}
\\usepackage[pdftex]{hyperref}
\\usepackage{fancyhdr}
\\usepackage{multirow}

\\pagestyle{fancy}
\\fancyhf{} % clear all header and footer fields
\\fancyfoot{}
\\renewcommand{\\headrulewidth}{0pt}
\\renewcommand{\\footrulewidth}{0pt}

% Adjust margins
\\addtolength{\\oddsidemargin}{-0.375in}
\\addtolength{\\evensidemargin}{-0.375in}
\\addtolength{\\textwidth}{1in}
\\addtolength{\\topmargin}{-.5in}
\\addtolength{\\textheight}{1.0in}

\\urlstyle{same}

\\raggedbottom
\\raggedright
\\setlength{\\tabcolsep}{0in}

% Sections formatting
\\titleformat{\\section}{
  \\vspace{-4pt}\\scshape\\raggedright\\large
}{}{0em}{}[\\color{black}\\titlerule \\vspace{-5pt}]

%-------------------------
% Custom commands
\\newcommand{\\resumeItem}[2]{
  \\item\\small{
    \\textbf{#1}{: #2 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeItemNH}[1]{
  \\item\\small{
    {#1 \\vspace{-2pt}}
  }
}

\\newcommand{\\resumeSubheading}[4]{
  \\vspace{-1pt}\\item
    \\begin{tabular*}{0.97\\textwidth}{l@{\\extracolsep{\\fill}}r}
      \\textbf{#1} & #2 \\\\
      \\textit{\\small#3} & \\textit{\\small #4} \\\\
    \\end{tabular*}\\vspace{-5pt}
}

\\newcommand{\\resumeSubItem}[2]{\\resumeItem{#1}{#2}\\vspace{-4pt}}

\\renewcommand{\\labelitemii}{$\\circ$}

\\newcommand{\\resumeSubHeadingListStart}{\\begin{itemize}[leftmargin=*,label={}]}
\\newcommand{\\resumeSubHeadingListStartBullets}{\\begin{itemize}[leftmargin=*]}
\\newcommand{\\resumeSubHeadingListEnd}{\\end{itemize}}
\\newcommand{\\resumeItemListStart}{\\begin{itemize}}
\\newcommand{\\resumeItemListEnd}{\\end{itemize}}

\\usepackage{array}
\\makeatletter
\\newcommand\\HUGE{\\@setfontsize\\Huge{38}{47}}
\\newcolumntype{L}{>{\hb@xt@\\z@\\bgroup}l<{\\hss\\egroup}}
\\newcolumntype{C}{>{\centering\\arraybackslash}c}
\\newcolumntype{R}{>{\hb@xt@\\z@\\bgroup\\hss}r<{\\egroup}}
\\makeatother

%-------------------------------------------
%%%%%%  CV STARTS HERE  %%%%%%%%%%%%%%%%%%%%%%%%%%%%

\\begin{document}

%----------HEADING-----------------
\\begin{tabular*}{\\textwidth}{L@{\\extracolsep{\\fill}}C@{\\extracolsep{\\fill}}R}
  \\href{mailto:${email}}{${email}} &
  \\multirow{3}{*}{\\Huge \\textbf{Joshua Dsouza}} &
  \\href{https://linkedin.com/in/xjosh}{linkedin.com/in/xjosh} \\\\
  (602) 312-3744 & & \\href{https://bit.ly/joshd}{personal website}
\\end{tabular*}

%-----------EDUCATION-----------------
\\section{Education}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {Arizona State University}{Expected May 2026}
      {Master's in Software Engineering}{Tempe, Arizona}
    \\resumeSubheading
      {St. Francis Institute of Technology (SFIT)}{May 2022}
      {Bachelor's of Engineering in Information Technology, GPA: 3.33/4}{Mumbai, Maharashtra}
  \\resumeSubHeadingListEnd

%-----------EXPERIENCE-----------------
\\section{Professional Experience}
  \\resumeSubHeadingListStart
    \\resumeSubheading
      {Fourth Signal}{November 2022 - July 2024}
      {Cloud Web Developer}{Mumbai}
      \\resumeItemListStart
        \\resumeItemNH{Led the migration from Angular to Angular 2 and PHP to Laravel while conducting a codebase audit, completing the transition in under a month, improving code efficiency by 30\\% and readability by 23\\%.}
        \\resumeItemNH{Directed a team of 4 to transform a monolithic architecture into a Micro-service structure by designing a modular framework and implementing RESTful APIs, improving application scalability and boosted efficiency by 70\\%.}
        \\resumeItemNH{Adopted Docker containers to virtualize development environments, enabling parallel development workflows and reducing deployment time by 25\\%, while also standardizing development standards across the team.}
        \\resumeItemNH{Designed an Azure ecosystem for seamless application deployment and implemented Azure DevOps CI/CD pipelines, eliminating manual builds and achieving 100\\% automated releases.}
        \\resumeItemNH{Developed and deployed FS Databridge, an iOS and Android application, increasing user engagement by 35\\% and enhanced the platform's mobile experience.}
        \\resumeItemNH{Established UI/UX standards by developing a comprehensive UI kit with Angular2, SCSS, and Tailwind, building custom reusable widgets to ensure design consistency and reduce development time for new features by 40\\%.}
        \\resumeItemNH{Integrated ESLint into development workflows and added branch protection rules in Azure Repos, establishing a two-step validation process for code reviews, increasing code quality by 30\\% and diminished code-related errors by 25\\%.}
        \\resumeItemNH{Constructed algorithms to replicate and automate real-life financial instruments, enabling top MNCs to simulate market scenarios and boost strategic decision-making processes.}
        \\resumeItemNH{Introduced JIRA to streamline task management and project tracking, training team members on best practices for agile workflow, leading to a 30\\% increase in productivity and a 20\\% improvement in deadline adherence.}
        \\resumeItemNH{Interviewed and mentored new hires, guiding mentees in the development and maintenance of applications. Enhanced documentation and training resources, cutting down onboarding time by 12\\%.}
      \\resumeItemListEnd
      \\resumeSubheading
{Meteor Labs}{Present}
{Unity Game Developer}{Scottsdale, AZ}
\\resumeItemListStart
  \\resumeItemNH{Developing a virtual reality (VR) experience for Scottsdale Water Treatment facility using Unity, implementing custom scripts for GameObject behaviors and interactive elements}
  \\resumeItemNH{Creating and managing timeline sequences for seamless integration of animations, models, and sound effects developed by cross-functional teams}
  \\resumeItemNH{Collaborating with design and animation teams to integrate 3D models, animations, and audio assets into the VR environment}
 \\resumeItemNH{Testing VR experience design while considering accessibility and usability for the water treatment facility's various user groups}

\\resumeItemListEnd
\\resumeSubheading
{Future Wave}{Summer 2022}
{Mobile App Development Intern}{Mumbai}
\\resumeItemListStart
 \\resumeItemNH{Developed backend infrastructure using Laravel with Sanctum authentication for secure user management}
 \\resumeItemNH{Built responsive frontend using Vue.js and Shadcn components, implementing state management with Pinia and API integration using Axios}
\\resumeItemListEnd

%-----------PROJECTS-----------------
\\section{Academic Projects / Personal Projects}
  \\resumeSubHeadingListStartBullets
    \\resumeSubItem{Virtual College Tour (Unreal Engine, Blender)}
      {Created a college campus (SFIT) tour in 3D using Blender and imported it into Unreal Engine 5 to add elements, movement, and virtual reality (VR) capabilities. Published and presented an IEEE paper titled \`\`A Framework for Development of a Virtual Campus Tour," detailing the development process and techniques leveraged.}
    \\resumeSubItem{Colloquium 2d Scavenger Hunt (Unity3d, C\\#)}
      {Spearheaded a team of 3 to develop an immersive 2D treasure hunt experience for the IT Tech fest at college using Unity3D, incorporating open-source tiles and characters to create a unique 2D platformer with game-themed objectives. Achieved over 200 registrations and 145 participants, with the game receiving an average review score of 4.6/5.}
      \\resumeSubItem{Google Meet Automation (Python, Android)}
      {Developed an Android app with a Python backend using Selenium to automate Google Meet sessions, featuring scheduled logins, custom meeting code support, and chat interaction capabilities.}
    \\resumeSubItem{Technago (Full Stack Web Development)}
      {Developed a website using HTML, CSS, PHP, and JavaScript to promote Indian products and support the Make in India Movement, implementing a responsive design and database integration for product management.}
    \\resumeSubItem{College ERP System (Java, SQL)}
      {Engineered a comprehensive Java-based ERP system with SQL database integration, featuring automated attendance tracking and academic performance management modules.}
  \\resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------------
\\section{Technical Skills}
  \\resumeSubHeadingListStart
    \\resumeSubItem{Programming Languages}{Java, Python, C++, C\\#, JS, TS}
    \\resumeSubItem{Mobile Development}{Flutter, Kotlin, Dart}
    \\resumeSubItem{Database Management}{MySQL, AzureDB, MongoDB}
    \\resumeSubItem{Cloud Technologies}{Azure (ACR, DevOps, App Service, Functions), AWS}
    \\resumeSubItem{Web Development}{Angular, React, Vue.js, Next.js, Laravel, PHP, WordPress}
    \\resumeSubItem{Game Development}{Unreal Engine, Unity3d, Blender}
    \\resumeSubItem{Software / Tools}{Adobe Master Collection, Microsoft 365, Filmora, VirtualBox, VS Code, Figma, Jira}${requiredSkills.length > 0 ? `\n    \\resumeSubItem{Additional Skills}{${requiredSkills.join(', ')}}` : ''}
  \\resumeSubHeadingListEnd

%-----------EXTRACURRICULAR-----------------
\\section{Extra Curricular Activities}
  \\resumeSubHeadingListStartBullets
    \\resumeSubItem{Information Technology Students' Association}
      {President (June 2022 - January 2024). Managed a team of 22, and organized 9 events in the span of 1 year. Organized technical and extracurricular workshops, collaborating with leading tech firms to bridge academia-industry gaps, resulting in a 30\\% increase in placement chances for participating students.}
  \\resumeSubHeadingListEnd

%-----------HONORS \\& AWARDS-----------------
\\section{Honors \\& Awards}
  \\resumeSubHeadingListStartBullets
    \\resumeSubItem{Spotlight Award}{Fourth Signal, For introducing new changes and making an impact in UI/UX design and functionality.}
    \\resumeSubItem{Judge}{IT Department, St Francis Institute of Technology, for evaluating projects based on innovation and technical proficiency.}
    \\resumeSubItem{2nd Place}{Tech fest Colloquium, for the Virtual College Tour Project.}
    \\resumeSubItem{3rd Place}{College Blind coding competition.}
  \\resumeSubHeadingListEnd

%-----------PUBLICATIONS-----------------
\\section{Publications}
  \\resumeSubHeadingListStart
    \\resumeItemNH{J. Dsouza, S. Ger, L. Wilson, N. Lobo, and N. Rai, \`\`A Framework for Development of a Virtual Campus Tour," 2023 International Conference on Communication System, Computing and IT Applications (CSCITA), Mumbai, India, 2023, pp. 225-230, doi: 10.1109/CSCITA55725.2023.10104840.}
  \\resumeSubHeadingListEnd

%-------------------------------------------
\\end{document}`
  }
}

export const atsService = new AtsService()
