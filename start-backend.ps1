# PowerShell script to start the backend server
# Run this from the project root directory

Write-Host "🚀 Starting Pharmacy AI Backend..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\.venv\Scripts\Activate.ps1

# Install dependencies if needed
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Start backend server
Write-Host "✅ Starting FastAPI server on http://localhost:8000" -ForegroundColor Green
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

