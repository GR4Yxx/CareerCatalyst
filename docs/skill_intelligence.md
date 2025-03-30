# Skill Intelligence Feature

The Skill Intelligence feature analyzes resumes to extract and categorize professional skills. It uses Google's Gemini AI to provide accurate skill identification and confidence scores.

## Overview

The Skill Intelligence feature:

1. Extracts text from uploaded resumes (PDF, Word, or text files)
2. Uses Gemini AI to analyze the text and identify skills
3. Categorizes skills into:
   - Technical Skills
   - Soft Skills
   - Domain Knowledge
   - Certifications
4. Assigns confidence scores to each identified skill
5. Stores the results in the database for future reference

## Architecture

### Backend Components

- **Models**:

  - `Skill`: Represents an individual skill with name, category, and confidence score
  - `UserSkill`: Contains a collection of skills associated with a user or profile

- **Services**:

  - `skill_service.py`: Handles skill extraction, analysis, and database operations
  - Integration with Google's Gemini AI for advanced skill analysis

- **API Endpoints**:
  - `GET /api/skills/resume/{resume_id}`: Get skills for a specific resume
  - `POST /api/skills/analyze/{resume_id}`: Manually trigger skill analysis for a resume
  - `GET /api/skills/user`: Get all skills for the current user
  - `GET /api/skills/profile/{profile_id}`: Get all skills for a specific profile

### Frontend Components

- **SkillsView.vue**: Main view for displaying and interacting with skills intelligence
- Features:
  - Display of current resume
  - Manual skill analysis triggering
  - Visual representation of skills by category
  - Confidence indicators for each skill

## Setup and Configuration

1. Install the required packages:

   ```
   pip install pypdf2 python-docx google-generativeai
   ```

2. Set up the Gemini API key:

   - Get an API key from [Google AI Studio](https://makersuite.google.com/)
   - Set the environment variable `GEMINI_API_KEY` with your key in the `.env` file:
     ```
     GEMINI_API_KEY=your-api-key
     ```

3. The system has a fallback mechanism if Gemini is not available:
   - Basic pattern matching against common skills
   - Simple categorization based on heuristics

## Testing the Gemini Integration

Two test scripts are provided to verify the Gemini integration:

1. **Direct Resume Analysis Test**:

   ```
   python -m app.scripts.analyze_resume_with_gemini
   ```

   This script:

   - Loads a resume file directly
   - Extracts text from the resume
   - Sends the text to Gemini for analysis
   - Displays the extracted skills by category

2. **API Integration Test**:
   ```
   python -m app.scripts.test_gemini_skill_analysis
   ```
   This script:
   - Authenticates with the API
   - Gets the current resume
   - Triggers skill analysis through the API
   - Verifies the results

### Test Results

In testing with real resumes, Gemini consistently identifies:

- 40-60 distinct professional skills
- Appropriate categorization between technical, soft, and domain skills
- High confidence scores for explicitly mentioned skills
- Lower confidence scores for implied skills

## Usage

### Automatic Skill Analysis

Skills are automatically analyzed when a resume is uploaded (unless disabled).

### Manual Skill Analysis

1. Navigate to the Skills Intelligence page
2. If a resume is already uploaded, click the "Analyze Skills" button
3. View the extracted skills categorized by type

### Skill Categories

- **Technical Skills**: Programming languages, tools, frameworks, and technical abilities
- **Soft Skills**: Interpersonal and transferable skills like communication and leadership
- **Domain Knowledge**: Industry-specific expertise and methodologies
- **Certifications**: Formal qualifications and certified skills

### Confidence Scoring

Each skill is assigned a confidence score from 0.0 to 1.0:

- High confidence (0.9-1.0): Very likely to be a genuine skill
- Medium confidence (0.7-0.9): Probably a genuine skill
- Low confidence (<0.7): Might be a skill, but less certain

## Future Enhancements

1. Skill level assessment (beginner, intermediate, advanced, expert)
2. Skill gap analysis for job listings
3. Skill development recommendations
4. Historical skill tracking over time
5. Industry-specific skill benchmarking
