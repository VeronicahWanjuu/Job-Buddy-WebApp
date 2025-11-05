# JobBuddy - Deployment Guide

This guide provides comprehensive instructions for setting up, running, and deploying the JobBuddy application.

## Table of Contents

1. [Local Development Setup](#local-development-setup)
2. [Running the Application](#running-the-application)
3. [Production Deployment](#production-deployment)
4. [Environment Variables](#environment-variables)
5. [Database Setup](#database-setup)
6. [Troubleshooting](#troubleshooting)

## Local Development Setup

### Prerequisites

- Python 3.11+
- Node.js 16+ and npm/yarn
- Git
- SQLite3 (for local development)

### Backend Setup

1. **Navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create .env file:**
   ```bash
   cp ../.env .env
   ```

5. **Initialize the database:**
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create .env file:**
   ```bash
   cat > .env << EOF
   REACT_APP_API_URL=http://localhost:5000/api/v1
   REACT_APP_APP_NAME=JobBuddy
   EOF
   ```

## Running the Application

### Development Mode

**Terminal 1 - Backend:**
```bash
cd backend
source venv/bin/activate
export FLASK_ENV=development
export FLASK_APP=app.py
flask run
```

The backend will be available at `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

The frontend will be available at `http://localhost:3000`

### Testing the Application

1. **Register a new account:**
   - Go to http://localhost:3000/register
   - Fill in your details and submit

2. **Login:**
   - Go to http://localhost:3000/login
   - Use your registered credentials

3. **Test features:**
   - Navigate to Dashboard
   - Add companies
   - Add applications
   - Update application status

## Production Deployment

### Deploying to Render

1. **Push your code to GitHub:**
   ```bash
   git push origin main
   ```

2. **Connect to Render:**
   - Go to https://render.com
   - Create a new Web Service
   - Connect your GitHub repository
   - Select the main branch

3. **Configure environment variables:**
   - Set `FLASK_ENV=production`
   - Set `JWT_SECRET` to a strong random value
   - Set `DATABASE_URL` to your PostgreSQL connection string
   - Set `FRONTEND_URL` to your production domain

4. **Build and deploy:**
   - Render will automatically build and deploy your application

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

This creates an optimized production build in the `frontend/build` directory.

**Backend:**
The Flask application is production-ready. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=sqlite:///jobbuddy.db  # Local development
# DATABASE_URL=postgresql://user:password@localhost/jobbuddy  # Production

# Authentication
SECRET_KEY=your-flask-secret-key-change-in-production
JWT_SECRET=your-super-secret-jwt-key-change-in-production

# File Upload
MAX_UPLOAD_MB=2

# External APIs
HUNTER_API_KEY=your-hunter-io-api-key-here
ATS_API_KEY=your-ats-api-key-here
ATS_API_URL=https://ats-api.example.com

# Frontend URL (for CORS)
FRONTEND_URL=http://localhost:3000  # Local
# FRONTEND_URL=https://jobbuddy.example.com  # Production

# Flask
FLASK_ENV=development  # or production
```

### Frontend (.env)

```bash
REACT_APP_API_URL=http://localhost:5000/api/v1  # Local
# REACT_APP_API_URL=https://api.jobbuddy.example.com/api/v1  # Production
REACT_APP_APP_NAME=JobBuddy
```

## Database Setup

### SQLite (Local Development)

The database is automatically created when you run `flask db upgrade`. It will be stored as `jobbuddy.db` in the backend directory.

### PostgreSQL (Production)

1. **Create a PostgreSQL database:**
   ```bash
   createdb jobbuddy
   ```

2. **Update DATABASE_URL in .env:**
   ```bash
   DATABASE_URL=postgresql://username:password@localhost:5432/jobbuddy
   ```

3. **Run migrations:**
   ```bash
   flask db upgrade
   ```

## Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill the process using port 5000
lsof -ti:5000 | xargs kill -9
```

**Database errors:**
```bash
# Reset the database
rm jobbuddy.db
flask db upgrade
```

**Import errors:**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Frontend Issues

**Port already in use:**
```bash
# Kill the process using port 3000
lsof -ti:3000 | xargs kill -9
```

**Node modules issues:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API connection errors:**
- Ensure the backend is running on http://localhost:5000
- Check REACT_APP_API_URL in .env
- Check CORS settings in backend/app.py

### Common Errors

**"CORS error" when making API calls:**
- Ensure FRONTEND_URL is correctly set in backend .env
- Restart the backend server

**"JWT token expired":**
- Clear localStorage in browser
- Log in again

**"Database locked":**
- Ensure only one Flask instance is running
- Close any open database connections

## API Documentation

The API is available at `/api/v1` with the following main endpoints:

- **Authentication:** `/auth/register`, `/auth/login`, `/auth/logout`
- **Profile:** `/profile`, `/profile/password`
- **Onboarding:** `/onboarding`
- **Companies:** `/companies`
- **Contacts:** `/contacts`, `/contacts/discover`
- **Applications:** `/applications`, `/applications/bulk-upload`
- **Goals:** `/goals/current`, `/goals/streak`
- **Notifications:** `/notifications`

See the backend code for detailed endpoint documentation.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the code comments in relevant files
3. Check the GitHub issues page
4. Contact the development team

## License

Private - All rights reserved
