# JobBuddy WebApp
A comprehensive job search assistance platform that helps job seekers track
applications, conduct direct outreach, and optimize their CVs for better
results.

## Features
📊 - Application tracking with Kanban board
🤝 - Direct reach-out to companies and contacts
📄 - CV-JD keyword matching and optimization
🎯 - Weekly goal setting and tracking
🔥 - Streak tracking and gamification
🔔 - In-app notifications
📚 - Resources and career coaches

## Tech Stack
**Frontend:**
- React 18
- Material-UI (MUI)
- React Router
- Axios
- React Hook Form
- react-beautiful-dnd

**Backend:**
- Flask (Python 3.11)
- SQLAlchemy
- JWT Authentication
- PostgreSQL / SQLite

## Setup Instructions
### Backend Setup
1. Navigate to backend directory:
```bash
cd backend
```
2. Create virtual environment:
```bash
python3.11 -m venv venv
source venv/bin/activate
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Set up environment variables (create .env file):
```bash
# Example .env content
SECRET_KEY=your-flask-secret-key
JWT_SECRET=your-super-secret-jwt-key
DATABASE_URL=sqlite:///jobbuddy.db
FLASK_ENV=development
HUNTER_API_KEY=your-hunter-io-api-key-here
ATS_API_KEY=your-ats-api-key-here
ATS_API_URL=https://ats-api.example.com
FRONTEND_URL=http://localhost:3000
```
5. Initialize database:
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```
6. Run backend:
```bash
flask run
```

### Frontend Setup
1. Navigate to frontend directory:
```bash
cd frontend
```
2. Install dependencies:
```bash
npm install
```
3. Create .env file:
```bash
# Example .env content
REACT_APP_API_URL=http://localhost:5000/api/v1
```
4. Run frontend:
```bash
npm start
```

## Development
* Backend runs on: `http://localhost:5000`
* Frontend runs on: `http://localhost:3000`

## License
Private - All rights reserved
