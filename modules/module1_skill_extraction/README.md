# Module 1: Onboarding & Skill Extraction

## Core Functionality

This module serves as the foundation of the entire system by transforming unstructured resume data into structured, actionable skill profiles.

## Technical Components

### 1. Resume Parser

- **Input Handling**:
  - Support for multiple file formats (PDF, DOCX, TXT, HTML)
  - API endpoint for file upload with validation
  - Basic preprocessing to normalize text
- **Text Extraction**:
  - PDF parsing using PyPDF2 or pdfplumber
  - DOCX parsing using python-docx
  - HTML parsing with BeautifulSoup
  - OCR capability (Tesseract) for image-based PDFs
- **Structural Analysis**:
  - Section identification (experience, education, skills, etc.)
  - Hierarchical parsing (headings, subheadings, bullet points)
  - Temporal data extraction (dates, durations)

### 2. Skills Identification & Extraction

- **Entity Recognition**:
  - Custom NER model trained on resume data
  - Rule-based extraction patterns for common skill formats
  - Context-aware extraction considering surrounding text
- **Skills Taxonomy Integration**:
  - Mapping to standardized skill ontology
  - Hierarchical categorization (technical, soft, domain, tools)
  - Industry-specific skill recognition
- **Implicit Skill Detection**:
  - Inference from job responsibilities
  - Recognition from project descriptions
  - Derivation from tools and technologies mentioned

### 3. Skill Quantification

- **Experience Calculation**:
  - Duration computation from employment dates
  - Recency weighting for relevance scoring
  - Frequency analysis across multiple positions
- **Proficiency Assessment**:
  - Linguistic marker detection (e.g., "expert in," "familiar with")
  - Context-based weighting (leadership roles vs. supporting roles)
  - Self-reported skill levels normalization
- **Confidence Scoring Algorithm**:
  - Weighted formula combining duration, recency, and context
  - Normalization across different skill types
  - Confidence intervals for ambiguous extractions

### 4. Output Generation

- **Structured Data Format**:
  - JSON schema for extracted skills
  - Standardized skill object with properties
- **Metadata Enrichment**:
  - Industry classification of experience
  - Education level mapping
  - Certification validation

## Implementation Approach

### Data Flow

- Resume upload → validation → text extraction
- Section identification → context labeling
- Entity extraction → taxonomy mapping → deduplication
- Experience calculation → confidence scoring
- Structured profile generation → database storage

### Algorithms & Models

- Section Classifier: A supervised model trained to identify resume sections
- Custom NER Model: Fine-tuned on technical and professional vocabulary
- Skill Mapper: Vector similarity-based matching to standardized taxonomy
- Confidence Calculator: Weighted algorithm combining multiple signals

## API Endpoints

- `POST /api/resume/upload`: Upload and process resume
- `GET /api/skills/profile`: Retrieve processed skill profile
- `PUT /api/skills/manual-edit`: Allow manual corrections

## MVP vs. Future Enhancements

### MVP:

- Basic PDF/DOCX parsing
- Extraction of explicit skills
- Simple taxonomy mapping
- Confidence scoring based on frequency

### Post-Hackathon Enhancements:

- Advanced implicit skill detection
- Multi-language support
- Interactive skill confirmation UI
- ML-based improvement from user corrections
- Real-time processing feedback
