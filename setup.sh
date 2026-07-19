#!/bin/bash
# Quick setup script for Turn-based WoW

set -e  # Exit on error

echo "🎮 Turn-based WoW - Quick Setup Script"
echo "======================================"
echo ""

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "❌ uv is not installed."
    echo ""
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo ""
    echo "✅ uv installed! Please restart your terminal and run this script again."
    exit 0
fi

echo "✅ uv is installed ($(uv --version))"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    uv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install dependencies
echo "📥 Installing dependencies..."
uv pip install -r requirements.txt
echo "✅ Dependencies installed"
echo ""

# Run tests
echo "🧪 Running tests..."
pytest -q
echo ""

# Success message
echo "======================================"
echo "✅ Setup complete!"
echo ""
echo "To start playing:"
echo "  1. Activate the virtual environment:"
echo "     source .venv/bin/activate"
echo ""
echo "  2. Run the game:"
echo "     python main.py"
echo ""
echo "To run tests:"
echo "     pytest"
echo ""
echo "To check code quality:"
echo "     ruff check ."
echo ""
echo "Enjoy the game! ⚔️🔥🛡️"
