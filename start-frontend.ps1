# PowerShell script to start the frontend server
# Run this from the project root directory

Write-Host "🚀 Starting Pharmacy AI Frontend..." -ForegroundColor Green

# Check if node_modules exists
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "📦 Installing Node.js dependencies..." -ForegroundColor Yellow
    cd frontend
    npm install
    cd ..
}

# Start frontend dev server
Write-Host "✅ Starting React dev server..." -ForegroundColor Green
Write-Host "🌐 Frontend will open at http://localhost:5173" -ForegroundColor Cyan
Write-Host ""

cd frontend
npm run dev

