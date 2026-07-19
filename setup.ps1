# Quick setup script for Turn-based WoW (Windows PowerShell)

$ErrorActionPreference = "Stop"

Write-Host "🎮 Turn-based WoW - Quick Setup Script" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Check if uv is installed
try {
    $uvVersion = uv --version 2>$null
    Write-Host "✅ uv is installed ($uvVersion)" -ForegroundColor Green
} catch {
    Write-Host "❌ uv is not installed." -ForegroundColor Red
    Write-Host ""
    Write-Host "Installing uv..." -ForegroundColor Yellow
    powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    Write-Host ""
    Write-Host "✅ uv installed! Please restart your terminal and run this script again." -ForegroundColor Green
    exit 0
}
Write-Host ""

# Create virtual environment if it doesn't exist
if (-Not (Test-Path ".venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    uv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}
Write-Host ""

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .venv\Scripts\Activate.ps1
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Install dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
uv pip install -r requirements.txt
Write-Host "✅ Dependencies installed" -ForegroundColor Green
Write-Host ""

# Run tests
Write-Host "🧪 Running tests..." -ForegroundColor Yellow
pytest -q
Write-Host ""

# Success message
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To start playing:" -ForegroundColor Cyan
Write-Host "  1. Activate the virtual environment:"
Write-Host "     .venv\Scripts\Activate.ps1"
Write-Host ""
Write-Host "  2. Run the game:"
Write-Host "     python main.py"
Write-Host ""
Write-Host "To run tests:"
Write-Host "     pytest"
Write-Host ""
Write-Host "To check code quality:"
Write-Host "     ruff check ."
Write-Host ""
Write-Host "Enjoy the game! ⚔️🔥🛡️" -ForegroundColor Cyan
