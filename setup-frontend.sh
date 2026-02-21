#!/bin/bash
# Frontend setup script

echo "🚀 Setting up Traffic Management Platform Frontend..."

# Check Node version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    exit 1
fi

echo "✅ Node version: $(node --version)"
echo "✅ npm version: $(npm --version)"

# Install dependencies
echo "📥 Installing dependencies..."
cd frontend
npm install

# Build for production (optional)
# echo "🔨 Building for production..."
# npm run build

echo ""
echo "✅ Frontend setup completed!"
echo ""
echo "To start the development server:"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "Application: http://localhost:5173"
