# 🤖 Codenixia AI-Powered Business Automation Assistant

## Overview
A full-stack AI business assistant with chatbot, lead management, 
email automation, and an admin dashboard.

## Tech Stack
- **Backend**: Python, Flask, SQLite
- **AI**: Google Gemini 1.5 Flash
- **Frontend**: HTML, CSS, Vanilla JS
- **Automation**: SMTP Email Notifications
- **Deployment**: Render / Railway / Vercel

## Features
- 🤖 AI Chatbot (Gemini API)
- 📋 Lead Capture Form
- 📧 Email Notification Automation
- 📊 Admin Dashboard
- 🗄️ SQLite Storage

## Setup Instructions

### 1. Clone & Install
```bash
git clone https://github.com/YOUR_USERNAME/codenixia-assistant
cd codenixia-assistant
pip install flask flask-cors python-dotenv google-generativeai
```

### 2. Configure Environment
```bash
cp backend/.env.example backend/.env
# Edit .env with your Gemini API key and email credentials
```

### 3. Initialize Database
```bash
python backend/database.py
```

### 4. Run the App
```bash
python backend/app.py
# Visit http://localhost:5000
```

## Deployment (Render.com)
1. Push to GitHub
2. Create new Web Service on Render
3. Set root directory: `backend`
4. Build command: `pip install -r requirements.txt`
5. Start command: `python app.py`
6. Add environment variables in Render dashboard

## Architecture
```
User → Frontend (HTML/JS)
         ├── /api/chat    → Gemini AI → Response + DB Log
         ├── /api/leads   → SQLite + Email Notification
         └── /api/dashboard/stats → Admin View
```