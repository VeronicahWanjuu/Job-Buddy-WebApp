# JobBuddy - System Architecture

This document provides a comprehensive overview of the JobBuddy application architecture.

## Table of Contents

1. [System Overview](#system-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture Diagram](#architecture-diagram)
4. [Backend Architecture](#backend-architecture)
5. [Frontend Architecture](#frontend-architecture)
6. [Database Schema](#database-schema)
7. [API Architecture](#api-architecture)
8. [Security Architecture](#security-architecture)
9. [Deployment Architecture](#deployment-architecture)

## System Overview

JobBuddy is a comprehensive job search assistance platform that helps users track applications, manage contacts, set goals, and optimize their job search process.

### Key Features

- **Application Tracking**: Kanban board for managing job applications
- **Company Management**: Track target companies and their information
- **Contact Management**: Store and discover recruiter contacts
- **Goal Setting**: Set weekly goals and track progress
- **Gamification**: Streak tracking and micro-quests with points
- **Notifications**: Real-time notifications for important events
- **CV Analysis**: Match CV against job descriptions (placeholder for API)

## Technology Stack

### Backend

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | Flask | 2.3+ |
| Database | SQLAlchemy | 2.0+ |
| Authentication | JWT (PyJWT) | 2.8+ |
| ORM | SQLAlchemy | 2.0+ |
| Validation | Marshmallow | 3.19+ |
| Testing | Pytest | 7.4+ |
| API Documentation | Flask-RESTX | 0.5+ |

### Frontend

| Component | Technology | Version |
|-----------|-----------|---------|
| Framework | React | 18.2+ |
| UI Library | Material-UI | 5.14+ |
| Routing | React Router | 6.14+ |
| HTTP Client | Axios | 1.4+ |
| State Management | React Context | Built-in |
| Form Handling | React Hook Form | 7.45+ |
| Testing | Jest | 29+ |
| Build Tool | Create React App | 5.0+ |

### Database

| Component | Technology |
|-----------|-----------|
| Development | SQLite | 3+ |
| Production | PostgreSQL | 13+ |

### DevOps

| Component | Technology |
|-----------|-----------|
| Version Control | Git/GitHub |
| CI/CD | GitHub Actions |
| Deployment | Render/Heroku |
| Containerization | Docker (optional) |

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      User Browser                            │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/HTTPS
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Frontend (React)                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Pages: Login, Register, Dashboard, Applications    │   │
│  │  Components: Navbar, Sidebar, Cards, Forms          │   │
│  │  Services: API Client, Auth Context                 │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ REST API (JSON)
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Backend (Flask)                            │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Routes: /auth, /profile, /companies, /applications │   │
│  │  Services: Business logic, Validation               │   │
│  │  Models: User, Company, Application, Contact        │   │
│  │  Middleware: Authentication, Error Handling         │   │
│  └──────────────────────────────────────────────────────┘   │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ SQL
                         │
┌────────────────────────▼────────────────────────────────────┐
│                   Database                                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Tables: users, companies, applications, contacts   │   │
│  │  Indexes: user_id, company_id, status               │   │
│  │  Relationships: Foreign keys, Constraints           │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Backend Architecture

### Project Structure

```
backend/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── models/               # Database models
│   ├── __init__.py
│   ├── user.py          # User model
│   ├── company.py       # Company model
│   ├── application.py   # Application model
│   ├── contact.py       # Contact model
│   ├── goal.py          # Goal model
│   ├── streak.py        # Streak model
│   └── notification.py  # Notification model
├── routes/              # API routes/blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication endpoints
│   ├── profile.py       # Profile endpoints
│   ├── companies.py     # Company endpoints
│   ├── applications.py  # Application endpoints
│   ├── contacts.py      # Contact endpoints
│   ├── goals.py         # Goal endpoints
│   └── notifications.py # Notification endpoints
├── services/            # Business logic
│   ├── __init__.py
│   ├── auth_service.py
│   ├── email_service.py
│   └── analytics_service.py
├── utils/               # Utility functions
│   ├── __init__.py
│   ├── decorators.py    # Custom decorators
│   ├── validators.py    # Input validation
│   └── error_handlers.py # Error handling
└── migrations/          # Database migrations
```

### Request Flow

1. **Request arrives** at Flask app
2. **Middleware processes** request (CORS, logging)
3. **Route handler** processes request
4. **Service layer** executes business logic
5. **Database layer** performs CRUD operations
6. **Response** is formatted and returned

### Authentication Flow

```
1. User submits credentials
   ↓
2. Hash password and verify
   ↓
3. Generate JWT token
   ↓
4. Return token to client
   ↓
5. Client includes token in Authorization header
   ↓
6. Server validates token on each request
   ↓
7. Token expires after 24 hours
```

## Frontend Architecture

### Project Structure

```
frontend/
├── public/
│   └── index.html       # HTML entry point
├── src/
│   ├── index.js         # React entry point
│   ├── index.css        # Global styles
│   ├── App.js           # Root component
│   ├── pages/           # Page components
│   │   ├── Login.js
│   │   ├── Register.js
│   │   ├── Dashboard.js
│   │   ├── Applications.js
│   │   ├── Companies.js
│   │   └── Profile.js
│   ├── components/      # Reusable components
│   │   ├── common/
│   │   │   └── ProtectedRoute.js
│   │   └── layout/
│   │       ├── Navbar.js
│   │       └── Sidebar.js
│   ├── services/        # API services
│   │   └── api.js       # Axios instance and API calls
│   ├── context/         # React Context
│   │   └── AuthContext.js
│   ├── hooks/           # Custom hooks (future)
│   └── utils/           # Utility functions (future)
├── package.json
└── .env                 # Environment variables
```

### Component Hierarchy

```
App
├── AuthProvider
│   └── Router
│       ├── Navbar
│       ├── Sidebar
│       └── Routes
│           ├── Login
│           ├── Register
│           ├── Dashboard
│           │   ├── GoalsWidget
│           │   ├── StreakWidget
│           │   └── StatsWidget
│           ├── Applications
│           │   └── KanbanBoard
│           ├── Companies
│           │   └── CompanyTable
│           └── Profile
│               ├── ProfileForm
│               ├── PasswordForm
│               └── DangerZone
```

### State Management

- **Global State**: AuthContext (user, token, login/logout)
- **Local State**: useState for component-specific state
- **API State**: Axios interceptors for token management

### Data Flow

```
User Action
    ↓
Component Event Handler
    ↓
API Service Call
    ↓
Backend Processing
    ↓
Response
    ↓
State Update (useState/Context)
    ↓
Component Re-render
```

## Database Schema

### Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    dream_milestone TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Companies Table

```sql
CREATE TABLE companies (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    name VARCHAR(255) NOT NULL,
    website VARCHAR(255),
    location VARCHAR(255),
    industry VARCHAR(255),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Applications Table

```sql
CREATE TABLE applications (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    job_url VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Planned',
    notes TEXT,
    applied_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

### Relationships

```
User (1) ──────── (Many) Companies
User (1) ──────── (Many) Applications
User (1) ──────── (Many) Contacts
User (1) ──────── (Many) Goals
User (1) ──────── (Many) Streaks
User (1) ──────── (Many) Notifications

Company (1) ──────── (Many) Applications
Company (1) ──────── (Many) Contacts
```

## API Architecture

### Endpoint Organization

```
/api/v1/
├── /auth
│   ├── POST /register
│   ├── POST /login
│   ├── POST /logout
│   └── POST /password-recovery
├── /profile
│   ├── GET /
│   ├── PUT /
│   ├── PUT /password
│   └── DELETE /
├── /companies
│   ├── GET /
│   ├── POST /
│   ├── GET /<id>
│   ├── PUT /<id>
│   └── DELETE /<id>
├── /applications
│   ├── GET /
│   ├── POST /
│   ├── GET /<id>
│   ├── PUT /<id>
│   ├── DELETE /<id>
│   └── POST /bulk-upload
├── /contacts
│   ├── GET /
│   ├── POST /
│   ├── POST /discover
│   ├── PUT /<id>
│   └── DELETE /<id>
├── /goals
│   ├── GET /current
│   ├── POST /
│   ├── GET /streak
│   ├── GET /micro-quests
│   └── POST /micro-quests/<id>/complete
└── /notifications
    ├── GET /
    ├── PUT /<id>/read
    ├── PUT /read-all
    └── DELETE /<id>
```

### Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "message": "Operation successful",
  "data": {},
  "pagination": {
    "page": 1,
    "per_page": 10,
    "total": 100,
    "pages": 10
  }
}
```

## Security Architecture

### Authentication

- **JWT Tokens**: Stateless authentication
- **Token Expiration**: 24 hours
- **Refresh Tokens**: Not implemented (can be added)
- **Password Hashing**: bcrypt with salt

### Authorization

- **Role-Based Access Control**: User owns their data
- **Endpoint Protection**: @login_required decorator
- **Data Isolation**: Users can only access their own data

### Data Protection

- **HTTPS**: Required in production
- **CORS**: Configured for frontend domain
- **Input Validation**: All inputs validated
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Output encoding

### API Security

- **Rate Limiting**: To be implemented
- **API Keys**: For external services
- **CORS Headers**: Configured
- **Security Headers**: To be added

## Deployment Architecture

### Development Environment

```
Local Machine
├── Backend (Flask dev server)
├── Frontend (React dev server)
└── SQLite Database
```

### Production Environment

```
Cloud Provider (Render/Heroku)
├── Frontend (Static files on CDN)
├── Backend (Gunicorn + Flask)
├── PostgreSQL Database
└── Redis Cache (optional)
```

### CI/CD Pipeline

```
Git Push
    ↓
GitHub Actions
    ├── Run Tests
    ├── Build Frontend
    ├── Build Backend
    └── Deploy to Production
```

### Scaling Considerations

- **Horizontal Scaling**: Multiple backend instances
- **Database Replication**: Master-slave setup
- **Caching**: Redis for frequently accessed data
- **Load Balancing**: Distribute traffic across instances
- **CDN**: Serve static assets from CDN

## Performance Optimization

### Backend

- Database indexing on frequently queried columns
- Query optimization and eager loading
- Caching for frequently accessed data
- Pagination for large datasets
- Async tasks for long-running operations

### Frontend

- Code splitting and lazy loading
- Component memoization
- Image optimization
- CSS minification
- JavaScript bundling

## Monitoring & Logging

### Backend Logging

- Request/response logging
- Error logging with stack traces
- Database query logging
- Authentication event logging

### Frontend Logging

- Error boundary for error tracking
- Console logging for debugging
- User action tracking (optional)

### Monitoring

- Application performance monitoring (APM)
- Error tracking (Sentry)
- Database performance monitoring
- API response time monitoring

## Future Enhancements

1. **Microservices**: Split into separate services
2. **Real-time Features**: WebSockets for notifications
3. **Machine Learning**: Resume optimization recommendations
4. **Mobile App**: Native iOS/Android apps
5. **Advanced Analytics**: Job search insights and trends
6. **Integration**: Calendar, email, LinkedIn integration

## Conclusion

JobBuddy follows a modern, scalable architecture with clear separation of concerns between frontend and backend. The system is designed to be maintainable, testable, and easily extensible for future features.
