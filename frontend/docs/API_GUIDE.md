# API Conventions Guide

## Base URL Structure

Our API uses a consistent base URL structure to communicate with the backend:

```
http://localhost/api
```

This base URL is configured in the `.env` file via the `VITE_API_URL` environment variable.

## Endpoint Convention

When making API calls, **do not** include the `/api` prefix in your endpoint paths as it's already included in the base URL.

### Correct Usage:

```typescript
// ✅ Correct - The /api prefix is already in the base URL
await api.get('/auth/me')
await api.post('/jobs/search', searchData)
```

### Incorrect Usage:

```typescript
// ❌ Incorrect - Creates a duplicate /api prefix
await api.get('/api/auth/me') // Will be converted to http://localhost/api/api/auth/me
await api.post('/api/jobs/search', searchData)
```

## Automatic Fix

Our API client in `src/lib/api.ts` has been configured to automatically strip the leading `/api` prefix from URLs to prevent duplication. However, for code consistency and clarity, please follow the convention of not including the `/api` prefix in your endpoint paths.

## Authentication

Bearer token authentication is handled automatically by the API client. The token is stored in localStorage and added to all requests via the Authorization header.

## API Categories

Our backend API is organized into these main categories:

- `/auth` - Authentication and user management
- `/resume` - Resume processing and management
- `/skills` - Skills extraction and profile management
- `/jobs` - Job search and application
- `/ats` - ATS intelligence and resume optimization
- `/career` - Career path analysis and recommendations
