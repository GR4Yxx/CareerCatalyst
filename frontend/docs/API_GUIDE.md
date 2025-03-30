# API Conventions Guide

## Base URL Structure

Our API uses a consistent base URL structure to communicate with the backend:

```
http://localhost/api
```

This base URL is configured in the `.env` file via the `VITE_API_URL` environment variable.

## Endpoint Convention

When making API calls, you should **not** include the `/api` prefix in your endpoint paths as it's already included in the base URL.

### Correct Usage:

```typescript
// ✅ Correct - The /api prefix is in the base URL
await api.get('/auth/me')
await api.post('/jobs/search', searchData)
```

### Incorrect Usage:

```typescript
// ❌ Incorrect - Creates a duplicate /api prefix
await api.get('/api/auth/me') // Will be converted to http://localhost/api/api/auth/me
await api.post('/api/jobs/search', searchData)
```

## Architecture Overview

Our API architecture is designed with these components:

1. **Frontend**: Sets base URL to `http://localhost/api` and uses endpoint paths without `/api` prefix
2. **Nginx**: Routes requests from `/api/` to the backend without the `/api/` prefix
3. **Backend**: Routes are defined without `/api` prefix since Nginx handles that part

This clean architecture avoids redundancy while maintaining proper separation of concerns.

## Authentication

Bearer token authentication is handled automatically by the API client. The token is stored in localStorage and added to all requests via the Authorization header.

## API Categories

Our backend API is organized into these main categories:

- `/auth` - Authentication and user management
- `/user` - User profile management
- `/resume` - Resume processing and management
- `/skills` - Skills extraction and profile management
- `/jobs` - Job search and application
- `/ats` - ATS intelligence and resume optimization
- `/career` - Career path analysis and recommendations

## User Profile Endpoints

The user profile API provides endpoints for managing user profiles, education, experience, skills, and uploads.

### Profile Endpoints

#### Get User Profile

```
GET /user/profile
```

Response:

```json
{
  "id": "uuid-string",
  "user_id": "user-uuid-string",
  "headline": "Full Stack Developer",
  "summary": "Experienced developer with 5+ years...",
  "location": "San Francisco, CA",
  "education": [...],
  "experience": [...],
  "skills": [...],
  "avatar_url": "https://example.com/avatars/user.jpg",
  "resume_url": "https://example.com/resumes/user.pdf"
}
```

#### Create Profile

```
POST /user/profile
```

Request:

```json
{
  "user_id": "user-uuid-string",
  "headline": "Full Stack Developer",
  "summary": "Experienced developer with 5+ years...",
  "location": "San Francisco, CA"
}
```

#### Update Profile

```
PUT /user/profile
```

Request:

```json
{
  "headline": "Senior Full Stack Developer",
  "summary": "Updated summary text...",
  "location": "New York, NY"
}
```

### Education Endpoints

#### Add Education

```
POST /user/education
```

Request:

```json
{
  "institution": "University of California",
  "degree": "Bachelor of Science",
  "field_of_study": "Computer Science",
  "start_date": "2015-09-01",
  "end_date": "2019-06-01",
  "description": "Studied algorithms, data structures..."
}
```

#### Update Education

```
PUT /user/education/{id}
```

Request:

```json
{
  "institution": "University of California",
  "degree": "Master of Science",
  "field_of_study": "Computer Science",
  "start_date": "2019-09-01",
  "end_date": "2021-06-01",
  "description": "Focused on machine learning..."
}
```

#### Delete Education

```
DELETE /user/education/{id}
```

### Experience Endpoints

#### Add Experience

```
POST /user/experience
```

Request:

```json
{
  "company": "Tech Solutions Inc.",
  "position": "Frontend Developer",
  "start_date": "2019-07-01",
  "current": true,
  "description": "Developed modern web applications...",
  "skills": ["JavaScript", "Vue.js", "TypeScript"]
}
```

#### Update Experience

```
PUT /user/experience/{id}
```

Request:

```json
{
  "company": "Tech Solutions Inc.",
  "position": "Senior Frontend Developer",
  "start_date": "2019-07-01",
  "current": true,
  "description": "Updated job description...",
  "skills": ["JavaScript", "Vue.js", "TypeScript", "React"]
}
```

#### Delete Experience

```
DELETE /user/experience/{id}
```

### Skills Endpoints

#### Add Skill

```
POST /user/skill
```

Request:

```json
{
  "name": "JavaScript",
  "level": "advanced",
  "category": "Programming Languages"
}
```

#### Update Skill

```
PUT /user/skill/{id}
```

Request:

```json
{
  "name": "JavaScript",
  "level": "expert",
  "category": "Programming Languages"
}
```

#### Delete Skill

```
DELETE /user/skill/{id}
```

### Upload Endpoints

#### Upload Avatar

```
POST /user/avatar
```

Request:

- Content-Type: multipart/form-data
- Form field: `avatar` (file)

Response:

```json
{
  "avatar_url": "https://example.com/avatars/user.jpg"
}
```

#### Upload Resume

```
POST /user/resume
```

Request:

- Content-Type: multipart/form-data
- Form field: `resume` (file)

Response:

```json
{
  "resume_url": "https://example.com/resumes/user.pdf"
}
```
