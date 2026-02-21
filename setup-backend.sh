#!/bin/bash
# Backend setup script

echo "🚀 Setting up Traffic Management Platform Backend..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

echo "✅ Python version: $(python3 --version)"

# Create virtual environment
echo "📦 Creating virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if doesn't exist
if [ ! -f .env ]; then
    echo "⚙️ Creating .env file..."
    cp .env.example .env
    echo "📝 Please update .env with your configuration"
fi

# Initialize database
echo "🗄️ Initializing database..."
python -c "from app.database import init_db; init_db()"

# Seed database
echo "🌱 Seeding database with sample data..."
python seed_db.py

echo ""
echo "✅ Backend setup completed!"
echo ""
echo "To start the backend server:"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn main:app --reload"
echo ""
echo "API documentation: http://localhost:8000/docs"
