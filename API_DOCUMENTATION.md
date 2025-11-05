# JobBuddy API Documentation

This document provides comprehensive documentation for the JobBuddy REST API.

## Base URL

```
http://localhost:5000/api/v1
```

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <access_token>
```

## Response Format

All responses are in JSON format:

### Success Response
```json
{
  "message": "Success message",
  "data": {}
}
```

### Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Error message"
  }
}
```

## Endpoints

### Authentication

#### Register
- **Method:** POST
- **Path:** `/auth/register`
- **Public:** Yes
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123",
    "name": "John Doe"
  }
  ```
- **Response:** User object and access token

#### Login
- **Method:** POST
- **Path:** `/auth/login`
- **Public:** Yes
- **Request Body:**
  ```json
  {
    "email": "user@example.com",
    "password": "SecurePass123"
  }
  ```
- **Response:** User object and access token

#### Logout
- **Method:** POST
- **Path:** `/auth/logout`
- **Protected:** Yes
- **Response:** Success message

#### Password Recovery
- **Method:** POST
- **Path:** `/auth/password-recovery`
- **Public:** Yes
- **Request Body:**
  ```json
  {
    "email": "user@example.com"
  }
  ```
- **Response:** Success message

### Profile

#### Get Profile
- **Method:** GET
- **Path:** `/profile`
- **Protected:** Yes
- **Response:** User profile with statistics

#### Update Profile
- **Method:** PUT
- **Path:** `/profile`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "name": "New Name",
    "dream_milestone": "Become a Tech Lead"
  }
  ```
- **Response:** Updated user profile

#### Change Password
- **Method:** PUT
- **Path:** `/profile/password`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "current_password": "OldPass123",
    "new_password": "NewPass123"
  }
  ```
- **Response:** Success message

#### Delete Account
- **Method:** DELETE
- **Path:** `/profile`
- **Protected:** Yes
- **Response:** Success message

### Onboarding

#### Create/Update Onboarding
- **Method:** POST
- **Path:** `/onboarding`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "target_role": "Software Engineer",
    "target_industry": "Technology",
    "experience_level": "Mid",
    "dream_milestone": "Become a Tech Lead",
    "skills": ["Python", "React", "AWS"],
    "preferred_locations": ["San Francisco", "New York"],
    "availability": "Immediate"
  }
  ```
- **Response:** Onboarding data

#### Get Onboarding
- **Method:** GET
- **Path:** `/onboarding`
- **Protected:** Yes
- **Response:** Onboarding data

### Companies

#### List Companies
- **Method:** GET
- **Path:** `/companies`
- **Protected:** Yes
- **Query Parameters:**
  - `search`: Search by company name
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
- **Response:** List of companies with pagination

#### Create Company
- **Method:** POST
- **Path:** `/companies`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "name": "Google",
    "website": "https://google.com",
    "location": "Mountain View, CA",
    "industry": "Technology",
    "notes": "Dream company"
  }
  ```
- **Response:** Created company object

#### Get Company
- **Method:** GET
- **Path:** `/companies/<id>`
- **Protected:** Yes
- **Response:** Company object with contacts

#### Update Company
- **Method:** PUT
- **Path:** `/companies/<id>`
- **Protected:** Yes
- **Request Body:** Same as create
- **Response:** Updated company object

#### Delete Company
- **Method:** DELETE
- **Path:** `/companies/<id>`
- **Protected:** Yes
- **Response:** Success message

### Contacts

#### List Contacts
- **Method:** GET
- **Path:** `/contacts`
- **Protected:** Yes
- **Query Parameters:**
  - `company_id`: Filter by company
  - `search`: Search by name or email
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
- **Response:** List of contacts with pagination

#### Create Contact
- **Method:** POST
- **Path:** `/contacts`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "company_id": 1,
    "name": "John Doe",
    "email": "john@google.com",
    "linkedin_url": "https://linkedin.com/in/johndoe",
    "role": "Engineering Manager"
  }
  ```
- **Response:** Created contact object

#### Discover Contacts (Hunter.io)
- **Method:** POST
- **Path:** `/contacts/discover`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "company_id": 1,
    "company_domain": "google.com"
  }
  ```
- **Response:** List of discovered contacts

#### Update Contact
- **Method:** PUT
- **Path:** `/contacts/<id>`
- **Protected:** Yes
- **Request Body:** Same as create
- **Response:** Updated contact object

#### Delete Contact
- **Method:** DELETE
- **Path:** `/contacts/<id>`
- **Protected:** Yes
- **Response:** Success message

### Applications

#### List Applications
- **Method:** GET
- **Path:** `/applications`
- **Protected:** Yes
- **Query Parameters:**
  - `status`: Filter by status (Planned, Applied, Interview, Offer, Rejected)
  - `company_id`: Filter by company
  - `search`: Search by job title
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
- **Response:** List of applications with pagination

#### Create Application
- **Method:** POST
- **Path:** `/applications`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "company_id": 1,
    "job_title": "Senior Software Engineer",
    "job_url": "https://example.com/jobs/123",
    "status": "Planned",
    "notes": "Great opportunity"
  }
  ```
- **Response:** Created application object

#### Get Application
- **Method:** GET
- **Path:** `/applications/<id>`
- **Protected:** Yes
- **Response:** Application object

#### Update Application
- **Method:** PUT
- **Path:** `/applications/<id>`
- **Protected:** Yes
- **Request Body:** Same as create
- **Response:** Updated application object

#### Delete Application
- **Method:** DELETE
- **Path:** `/applications/<id>`
- **Protected:** Yes
- **Response:** Success message

#### Bulk Upload Applications
- **Method:** POST
- **Path:** `/applications/bulk-upload`
- **Protected:** Yes
- **Content-Type:** multipart/form-data
- **Form Data:**
  - `file`: CSV file with columns: company_name, job_title, job_url, status, notes
- **Response:** Upload results with success/failure counts

### Goals

#### Get Current Goal
- **Method:** GET
- **Path:** `/goals/current`
- **Protected:** Yes
- **Response:** Current week's goal

#### Set Goal
- **Method:** POST
- **Path:** `/goals`
- **Protected:** Yes
- **Request Body:**
  ```json
  {
    "applications_goal": 5,
    "outreach_goal": 3
  }
  ```
- **Response:** Updated goal

#### Get Streak
- **Method:** GET
- **Path:** `/goals/streak`
- **Protected:** Yes
- **Response:** Streak information

#### Get Micro Quests
- **Method:** GET
- **Path:** `/goals/micro-quests`
- **Protected:** Yes
- **Response:** List of available micro-quests

#### Complete Micro Quest
- **Method:** POST
- **Path:** `/goals/micro-quests/<quest_id>/complete`
- **Protected:** Yes
- **Response:** Updated streak with points earned

### Notifications

#### List Notifications
- **Method:** GET
- **Path:** `/notifications`
- **Protected:** Yes
- **Query Parameters:**
  - `is_read`: Filter by read status (true/false)
  - `type`: Filter by type (follow_up, goal_reminder, micro_quest, system)
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
- **Response:** List of notifications with unread count

#### Mark as Read
- **Method:** PUT
- **Path:** `/notifications/<id>/read`
- **Protected:** Yes
- **Response:** Updated notification

#### Mark All as Read
- **Method:** PUT
- **Path:** `/notifications/read-all`
- **Protected:** Yes
- **Response:** Success message

#### Delete Notification
- **Method:** DELETE
- **Path:** `/notifications/<id>`
- **Protected:** Yes
- **Response:** Success message

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| BAD_REQUEST | 400 | Invalid request data |
| UNAUTHORIZED | 401 | Authentication failed or token expired |
| FORBIDDEN | 403 | User does not have permission |
| NOT_FOUND | 404 | Resource not found |
| TIMEOUT | 408 | Request timeout |
| FILE_TOO_LARGE | 413 | File exceeds maximum size |
| INVALID_DATA_FORMAT | 422 | Invalid data format |
| RATE_LIMIT_EXCEEDED | 429 | Too many requests |
| INTERNAL_SERVER_ERROR | 500 | Server error |
| SERVICE_UNAVAILABLE | 503 | Service unavailable |

## Rate Limiting

Currently, no rate limiting is implemented. This should be added in production.

## Pagination

Paginated endpoints return:
```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10
  }
}
```

## Testing

### Using cURL

```bash
# Register
curl -X POST http://localhost:5000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123","name":"John"}'

# Login
curl -X POST http://localhost:5000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"Pass123"}'

# Get Profile (with token)
curl -X GET http://localhost:5000/api/v1/profile \
  -H "Authorization: Bearer <access_token>"
```

### Using Postman

1. Import the API endpoints into Postman
2. Set the base URL to `http://localhost:5000/api/v1`
3. Create a Bearer token variable for authentication
4. Test each endpoint

## Changelog

### Version 1.0.0
- Initial API release
- All core endpoints implemented
- JWT authentication
- Error handling
- Pagination support
