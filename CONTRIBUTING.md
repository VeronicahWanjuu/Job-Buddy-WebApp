# Contributing to JobBuddy

Thank you for your interest in contributing to JobBuddy! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

We are committed to providing a welcoming and inclusive environment. Please be respectful and constructive in all interactions.

## Getting Started

### Prerequisites

- Git
- Python 3.11+
- Node.js 16+
- GitHub account

### Setup Development Environment

1. **Fork the repository:**
   ```bash
   # Go to https://github.com/VeronicahWanjuu/Job-Buddy-WebApp
   # Click "Fork" button
   ```

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/Job-Buddy-WebApp.git
   cd JobBuddy
   ```

3. **Add upstream remote:**
   ```bash
   git remote add upstream https://github.com/VeronicahWanjuu/Job-Buddy-WebApp.git
   ```

4. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

5. **Set up the development environment:**
   ```bash
   # Backend
   cd backend
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Frontend
   cd ../frontend
   npm install
   ```

## Development Workflow

### Making Changes

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/descriptive-name
   ```

2. **Make your changes:**
   - Follow the coding standards below
   - Write clear, descriptive commit messages
   - Include tests for new functionality

3. **Test your changes:**
   ```bash
   # Backend
   cd backend
   pytest

   # Frontend
   cd ../frontend
   npm test
   ```

4. **Commit your changes:**
   ```bash
   git add .
   git commit -m "Add: descriptive message of changes"
   ```

5. **Push to your fork:**
   ```bash
   git push origin feature/descriptive-name
   ```

6. **Create a Pull Request:**
   - Go to GitHub and create a PR from your fork
   - Provide a clear description of changes
   - Reference any related issues

## Coding Standards

### Python (Backend)

- Follow PEP 8 style guide
- Use 4 spaces for indentation
- Use type hints for function parameters and returns
- Write docstrings for all functions and classes
- Maximum line length: 100 characters

**Example:**
```python
def create_company(name: str, website: str) -> Company:
    """
    Create a new company in the database.
    
    Args:
        name: Company name
        website: Company website URL
    
    Returns:
        Created Company object
    
    Raises:
        ValueError: If name is empty
    """
    if not name:
        raise ValueError("Company name is required")
    
    company = Company(name=name, website=website)
    db.session.add(company)
    db.session.commit()
    return company
```

### JavaScript/React (Frontend)

- Follow Airbnb JavaScript style guide
- Use 2 spaces for indentation
- Use meaningful variable names
- Write JSDoc comments for components
- Use functional components with hooks

**Example:**
```javascript
/**
 * Company List Component
 * 
 * Displays a list of companies with search and pagination.
 * 
 * @component
 * @returns {JSX.Element} The company list component
 */
const CompanyList = () => {
  const [companies, setCompanies] = useState([]);
  
  useEffect(() => {
    fetchCompanies();
  }, []);
  
  return (
    <div className="company-list">
      {/* Component content */}
    </div>
  );
};

export default CompanyList;
```

## Commit Message Guidelines

Follow the Conventional Commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: A new feature
- **fix**: A bug fix
- **docs**: Documentation only changes
- **style**: Changes that don't affect code meaning
- **refactor**: Code change without feature or bug fix
- **perf**: Code change that improves performance
- **test**: Adding or updating tests
- **chore**: Changes to build process or dependencies

### Examples

```
feat(applications): add bulk upload functionality

- Add CSV file upload endpoint
- Parse and validate CSV data
- Create applications in batch

Closes #123
```

```
fix(auth): fix JWT token expiration issue

The token was not being refreshed correctly.
Now using proper expiration time.

Fixes #456
```

## Pull Request Process

1. **Update documentation:**
   - Update README.md if needed
   - Add/update docstrings
   - Update API documentation if endpoints changed

2. **Ensure tests pass:**
   ```bash
   # Backend
   cd backend && pytest

   # Frontend
   cd frontend && npm test
   ```

3. **Check code quality:**
   - No console errors or warnings
   - No unused imports or variables
   - Proper error handling

4. **Create descriptive PR:**
   - Clear title and description
   - Reference related issues
   - Include screenshots for UI changes

5. **Respond to review feedback:**
   - Make requested changes
   - Explain any disagreements
   - Push updates to the same branch

## Testing Requirements

### Backend Tests

- Write unit tests for new functions
- Write integration tests for API endpoints
- Aim for > 80% code coverage
- Test both success and error cases

```python
def test_create_company():
    """Test creating a company"""
    company = create_company("Google", "https://google.com")
    assert company.name == "Google"
    assert company.website == "https://google.com"

def test_create_company_invalid():
    """Test creating company with invalid data"""
    with pytest.raises(ValueError):
        create_company("", "https://example.com")
```

### Frontend Tests

- Write tests for components
- Test user interactions
- Test API integration
- Aim for > 70% code coverage

```javascript
describe('CompanyForm', () => {
  test('should submit form with valid data', () => {
    const { getByText, getByLabelText } = render(<CompanyForm />);
    
    fireEvent.change(getByLabelText('Company Name'), {
      target: { value: 'Google' }
    });
    fireEvent.click(getByText('Submit'));
    
    expect(mockSubmit).toHaveBeenCalledWith({ name: 'Google' });
  });
});
```

## Documentation

### Code Comments

- Explain the "why", not the "what"
- Use clear, concise language
- Update comments when code changes

```python
# Good
# Check if user has admin privileges before allowing deletion
if not user.is_admin:
    raise PermissionError("Only admins can delete companies")

# Bad
# Check admin
if not user.is_admin:
    raise PermissionError("Only admins can delete companies")
```

### Docstrings

- Use Google-style docstrings for Python
- Use JSDoc for JavaScript
- Include parameters, returns, and exceptions

## Performance Considerations

- Optimize database queries (use eager loading)
- Cache frequently accessed data
- Minimize API calls from frontend
- Use pagination for large datasets
- Optimize images and assets

## Security Best Practices

- Never commit secrets or API keys
- Validate all user inputs
- Use parameterized queries to prevent SQL injection
- Implement proper authentication and authorization
- Use HTTPS in production
- Keep dependencies updated

## Issue Reporting

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots/logs
- Environment (OS, browser, versions)

### Feature Requests

Include:
- Clear description of the feature
- Use cases and benefits
- Proposed implementation (if applicable)
- Any related issues

## Questions?

- Check existing issues and discussions
- Review documentation
- Ask in GitHub discussions
- Contact the maintainers

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to JobBuddy!
