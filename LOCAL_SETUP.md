# 🏠 Local Development Setup Guide

This guide will help you run the Pharmacy AI platform locally on Windows.

## Prerequisites

- **Python 3.9+** installed ([Download](https://www.python.org/downloads/))
- **Node.js 18+** and npm installed ([Download](https://nodejs.org/))
- **Git** (optional, for version control)

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Setup Backend (FastAPI)

Open **PowerShell** in the project root (`C:\Users\hai\Desktop\pharma`):

```powershell
# 1. Create virtual environment
python -m venv .venv

# 2. Activate virtual environment
.\.venv\Scripts\Activate.ps1

# 3. Install Python dependencies
pip install -r requirements.txt

# 4. Start the backend server
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend is running at:** `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

**Keep this terminal open!**

---

### Step 2: Setup Frontend (React + Vite)

Open a **NEW PowerShell window** (keep backend running):

```powershell
# Navigate to project root
cd C:\Users\hai\Desktop\pharma

# Go to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the frontend dev server
npm run dev
```

**✅ Frontend is running at:** `http://localhost:5173` (or the port shown in terminal)

The frontend will automatically connect to `http://localhost:8000` (backend).

---

## 📋 Testing the Application

1. **Open your browser** → Go to `http://localhost:5173`

2. **Upload Sample Data:**
   - Click **"Excel Uploads"** in the navigation
   - Upload `data/sample_excel_files/inventory_sample.xlsx`
   - Upload `data/sample_excel_files/sales_sample.xlsx` (if available)

3. **View Dashboard:**
   - Go to **"Dashboard"**
   - You should see:
     - KPI cards (Total SKUs, Low Stock, etc.)
     - Alerts list
     - Inventory table
     - Forecast chart

4. **Test AI Chatbot:**
   - Go to **"AI Assistant"**
   - Try queries like:
     - `How many Paracetamol are left?`
     - `Which medicines expire this week?`
     - `Generate wastage report`
     - `Suggest reorder list`

---

## 🔧 Troubleshooting

### Backend Issues

**Port 8000 already in use:**
```powershell
# Use a different port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```
Then update `frontend/.env` with `VITE_API_BASE_URL=http://localhost:8001`

**Module not found errors:**
```powershell
# Make sure virtual environment is activated
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Database errors:**
- The app uses SQLite by default (no setup needed)
- Database file: `backend/pharmacy.db` (auto-created)

### Frontend Issues

**npm install fails:**
```powershell
# Clear cache and retry
npm cache clean --force
npm install
```

**Port 5173 already in use:**
- Vite will automatically use the next available port
- Check terminal output for the actual URL

**CORS errors:**
- Backend CORS is configured to allow all origins in development
- If issues persist, check backend is running on port 8000

---

## 📁 Project Structure

```
pharma/
├── backend/
│   ├── app/
│   │   ├── api/          # API endpoints
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   ├── ml/           # ML forecasting
│   │   ├── chatbot/      # NLP chatbot
│   │   └── main.py       # FastAPI app
│   └── pharmacy.db       # SQLite database (auto-created)
│
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages
│   │   ├── components/   # Reusable components
│   │   ├── services/     # API calls
│   │   └── App.jsx       # Main app component
│   └── package.json
│
└── data/
    └── sample_excel_files/  # Sample Excel files
```

---

## 🎯 Next Steps

- Upload your own Excel files via the **Excel Uploads** page
- Configure alert thresholds in the database
- Customize forecasting parameters
- Deploy to production (Render + Vercel)

---

## 💡 Tips

- **Keep both terminals open** (backend + frontend)
- **Hot reload enabled:** Changes to code will auto-refresh
- **Database resets:** Delete `backend/pharmacy.db` to start fresh
- **Check logs:** Both terminals show helpful error messages

---

**Happy coding! 🚀**

