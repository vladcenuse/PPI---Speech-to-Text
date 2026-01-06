# Speech-to-Text Medical Web App

A full-stack web application built with FastAPI (backend) and Vue 3 + Vite (frontend) for medical speech-to-text conversion.

## Requirements

- Python 3.10+
- Node.js 
- npm 
- Git

##  Setup Instructions

### Backend Setup

1. Clone the repository
```bash
git clone https://github.com/vladcenuse/PPI---Speech-to-Text.git
cd PPI---Speech-to-Text
```

2. Set up Python virtual environment and install dependencies
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# For Windows:
venv\Scripts\activate
# For macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

3. Start the FastAPI server
```bash
# Make sure you're in the backend directory
uvicorn app.main:app --reload
```
The backend will be running at http://localhost:8000

### Frontend Setup

1. Open a new terminal and navigate to the frontend directory
```bash
cd frontend/S2T-frontend
```

2. Install Node.js dependencies
```bash
npm install
```

3. Start the Vue development server
```bash
npm run dev
```
The frontend will be running at http://localhost:5173

## Usage

1. Once both servers are running, open your browser and go to http://localhost:5173
2. The FastAPI backend API documentation is available at http://localhost:8000/docs

## Project Structure

```
PPI---Speech-to-Text/
├── backend/               # FastAPI backend
│   ├── app/
│   │   ├── main.py       # Main application file
│   │   └── ...
│   └── requirements.txt  # Python dependencies
└── frontend/             # Vue.js frontend
    └── S2T-frontend/
        ├── src/          # Source files
        ├── public/       # Public assets
        └── package.json  # Node.js dependencies
```

##  Development Notes

- The backend runs on port 8000 by default
- The frontend runs on port 5173 by default
- Make sure both servers are running simultaneously for the application to work
- Check the FastAPI documentation at /docs for available API endpoints
- The app is also deployed on https://ppi-frontend.onrender.com