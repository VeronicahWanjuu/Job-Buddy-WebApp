# JobBuddy - Testing Guide

This document provides guidelines and test cases for the JobBuddy application.

## Testing Strategy

The application follows a comprehensive testing strategy including:

1. **Unit Tests** - Test individual functions and components
2. **Integration Tests** - Test API endpoints and database interactions
3. **E2E Tests** - Test complete user workflows
4. **Manual Testing** - Test UI/UX and user experience

## Backend Testing

### Setup

```bash
cd backend
source venv/bin/activate
pip install pytest pytest-cov
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_auth.py

# Run specific test
pytest tests/test_auth.py::test_register
```

### Test Cases

#### Authentication Tests

```python
# Test user registration
def test_register_success():
    # Should create a new user and return access token
    pass

def test_register_duplicate_email():
    # Should fail if email already exists
    pass

def test_register_invalid_password():
    # Should fail if password doesn't meet requirements
    pass

# Test user login
def test_login_success():
    # Should return access token for valid credentials
    pass

def test_login_invalid_credentials():
    # Should fail with invalid email or password
    pass
```

#### Companies Tests

```python
def test_create_company():
    # Should create a new company
    pass

def test_list_companies():
    # Should return paginated list of companies
    pass

def test_update_company():
    # Should update company information
    pass

def test_delete_company():
    # Should delete company and related data
    pass
```

#### Applications Tests

```python
def test_create_application():
    # Should create a new application
    pass

def test_update_application_status():
    # Should update application status
    pass

def test_bulk_upload_applications():
    # Should upload multiple applications from CSV
    pass
```

#### Goals Tests

```python
def test_get_current_goal():
    # Should return current week's goal
    pass

def test_set_goal():
    # Should set weekly goals
    pass

def test_get_streak():
    # Should return streak information
    pass

def test_complete_micro_quest():
    # Should award points for completing quest
    pass
```

## Frontend Testing

### Setup

```bash
cd frontend
npm install --save-dev @testing-library/react @testing-library/jest-dom jest
```

### Running Tests

```bash
# Run all tests
npm test

# Run with coverage
npm test -- --coverage

# Run specific test file
npm test -- Login.test.js
```

### Test Cases

#### Authentication Tests

```javascript
// Test login page
describe('Login Page', () => {
  test('should render login form', () => {
    // Should display email and password fields
  });

  test('should submit login form', () => {
    // Should call login API with credentials
  });

  test('should show error on invalid credentials', () => {
    // Should display error message
  });
});

// Test register page
describe('Register Page', () => {
  test('should validate password strength', () => {
    // Should check password requirements
  });

  test('should create new account', () => {
    // Should call register API
  });
});
```

#### Component Tests

```javascript
describe('Dashboard', () => {
  test('should display weekly goals', () => {
    // Should show goal progress bars
  });

  test('should display streak information', () => {
    // Should show current and longest streak
  });

  test('should show quick action buttons', () => {
    // Should have buttons for quick actions
  });
});

describe('Applications Kanban', () => {
  test('should display all status columns', () => {
    // Should show 5 columns: Planned, Applied, Interview, Offer, Rejected
  });

  test('should move application between columns', () => {
    // Should update application status
  });

  test('should delete application', () => {
    // Should remove application from board
  });
});
```

## Manual Testing Checklist

### User Registration & Authentication

- [ ] User can register with valid email and password
- [ ] User cannot register with duplicate email
- [ ] User cannot register with weak password
- [ ] User can login with correct credentials
- [ ] User cannot login with wrong credentials
- [ ] User can logout successfully
- [ ] User is redirected to login when token expires
- [ ] User can recover password

### Dashboard

- [ ] Dashboard loads with user data
- [ ] Weekly goals display correctly
- [ ] Streak information is accurate
- [ ] Quick action buttons work
- [ ] Statistics are calculated correctly

### Companies Management

- [ ] User can add a new company
- [ ] User can view list of companies
- [ ] User can edit company information
- [ ] User can delete a company
- [ ] Search functionality works
- [ ] Pagination works correctly

### Applications Tracking

- [ ] User can add a new application
- [ ] User can view applications in Kanban board
- [ ] User can move application between statuses
- [ ] User can edit application details
- [ ] User can delete an application
- [ ] Bulk upload works with CSV file
- [ ] Application counter updates

### Profile Management

- [ ] User can view their profile
- [ ] User can update profile information
- [ ] User can change password
- [ ] User can delete their account
- [ ] Profile changes are saved

### Goals & Gamification

- [ ] User can set weekly goals
- [ ] Goal progress updates when applications are added
- [ ] Streak counter increments correctly
- [ ] Micro-quests are available
- [ ] Points are awarded for completing quests

### Notifications

- [ ] Notifications display in navbar
- [ ] User can mark notification as read
- [ ] User can delete notification
- [ ] Unread count is accurate

## Performance Testing

### Load Testing

Test the application with multiple concurrent users:

```bash
# Using Apache Bench
ab -n 1000 -c 10 http://localhost:5000/api/v1/applications

# Using wrk
wrk -t4 -c100 -d30s http://localhost:5000/api/v1/applications
```

### Response Time Targets

- API endpoints: < 200ms
- Page load: < 2s
- Database queries: < 100ms

## Security Testing

### OWASP Top 10

- [ ] SQL Injection - Validate all inputs
- [ ] Broken Authentication - Test JWT handling
- [ ] Sensitive Data Exposure - Check HTTPS usage
- [ ] XML External Entities - Not applicable
- [ ] Broken Access Control - Test authorization
- [ ] Security Misconfiguration - Review settings
- [ ] Cross-Site Scripting (XSS) - Sanitize outputs
- [ ] Insecure Deserialization - Validate JSON
- [ ] Using Components with Known Vulnerabilities - Update dependencies
- [ ] Insufficient Logging & Monitoring - Check logs

### Test Cases

```bash
# Test SQL Injection
curl -X GET "http://localhost:5000/api/v1/companies?search='; DROP TABLE companies; --"

# Test XSS
curl -X POST http://localhost:5000/api/v1/companies \
  -H "Content-Type: application/json" \
  -d '{"name":"<script>alert(\"XSS\")</script>"}'

# Test CSRF
# Attempt to make request without CSRF token

# Test Authentication
# Attempt to access protected endpoint without token
curl -X GET http://localhost:5000/api/v1/profile
```

## Browser Compatibility

Test the application on:

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Chrome
- [ ] Mobile Safari

## Accessibility Testing

- [ ] All images have alt text
- [ ] Form labels are properly associated
- [ ] Color contrast meets WCAG standards
- [ ] Keyboard navigation works
- [ ] Screen reader compatible

## Continuous Integration

The project uses GitHub Actions for CI/CD:

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run backend tests
        run: cd backend && pytest
      - name: Run frontend tests
        run: cd frontend && npm test
```

## Bug Reporting

When reporting bugs, include:

1. Steps to reproduce
2. Expected behavior
3. Actual behavior
4. Screenshots/videos
5. Browser/OS information
6. Console errors

## Test Coverage Goals

- Backend: > 80% coverage
- Frontend: > 70% coverage
- Critical paths: 100% coverage

## Resources

- [Jest Documentation](https://jestjs.io/)
- [React Testing Library](https://testing-library.com/react)
- [Pytest Documentation](https://docs.pytest.org/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
