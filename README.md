# CareerCatalyst: AI-Powered Career Navigation System

## Project Vision

CareerCatalyst reimagines career development by transforming passive job searching into an interactive, data-driven journey. By combining resume analysis, skill mapping, and job market intelligence, we create a comprehensive platform that guides users from their current position to their career aspirations through actionable insights and personalized recommendations.

## Problem Statement

Today's job market presents three critical challenges:

1. **Skills Mismatch**: Job seekers struggle to identify and articulate their transferable skills
2. **Career Path Ambiguity**: Professionals lack visibility into viable career trajectories
3. **ATS Barriers**: Qualified candidates get filtered out by automated screening systems

CareerCatalyst addresses these challenges by providing an end-to-end solution that bridges the gap between a user's current skills and potential opportunities.

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Node.js and npm (for local development)
- MongoDB (for local development without Docker)

### Environment Setup

1. Clone the repository

```bash
git clone https://github.com/yourusername/CareerCatalyst.git
cd CareerCatalyst
```

2. Create a `.env` file based on the provided `.env.example` template

```bash
cp .env.example .env
```

3. Update the `.env` file with your API keys:

   - `GEMINI_API_KEY`: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - `JSEARCH_API_KEY`: Get from [RapidAPI JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch)
   - `GOOGLE_API_KEY`: If using other Google services

4. Start the application with Docker Compose

```bash
cd docker
docker-compose up -d
```

5. Access the application at http://localhost

## Core Value Proposition

- **Skills Intelligence**: Extract, categorize, and contextualize skills from resumes
- **Opportunity Discovery**: Match users to jobs based on direct and adjacent skill sets
- **Career Pathing**: Visualize potential career trajectories and skill development needs
- **Application Optimization**: Tailor resumes to increase visibility with ATS systems

## System Architecture

CareerCatalyst consists of five integrated modules:

1. **Onboarding & Skill Extraction**: Resume parsing and skill extraction system
2. **Job Finder & Recommendation Engine**: Job sourcing and matching system
3. **ATS Intelligence System**: Resume optimization for ATS compatibility
4. **Career Path Visualization**: Interactive career trajectory visualization
5. **Interactive Frontend Experience**: User interface and experience layer

## Hackathon Information

This project is being developed for DevHacks (March 29-30, 2025) under the following tracks:

- Best use of AI
- Best beginner hack

## Team

- Joshua Dsouza (SER): App dev, web dev, game dev
- Krish Patil (SER): Data engineer, database
- Pratham (SER): Sales and marketing, documentation, product design
- Prajwal: Data science, Streamlit

## Future Expansion Potential

Post-hackathon, CareerCatalyst could evolve to include:

- **Learning Path Integration**: Direct connections to relevant courses and certifications
- **Networking Recommendations**: Identification of valuable professional connections
- **Salary Negotiation Guidance**: Data-driven compensation insights
- **Industry-Specific Modules**: Tailored features for tech, healthcare, finance, etc.

## Impact & Vision

CareerCatalyst aims to democratize career development by providing sophisticated insights previously available only through expensive career coaches or recruiters. By empowering professionals to make data-informed career decisions, we help bridge skills gaps in the workforce and enable more fulfilling career journeys.
