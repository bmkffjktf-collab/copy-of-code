#!/bin/bash
# Full setup script

echo "🚀 Setting up Nationwide AI-Powered Traffic Management Platform..."
echo ""

# Make setup scripts executable
chmod +x setup-backend.sh
chmod +x setup-frontend.sh

# Run backend setup
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 1: Backend Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./setup-backend.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Step 2: Frontend Setup"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
./setup-frontend.sh

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Setup Completed Successfully!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📚 Next Steps:"
echo ""
echo "Option 1: Docker Compose (Recommended)"
echo "  docker-compose up --build"
echo ""
echo "Option 2: Manual Run"
echo "  Terminal 1 (Backend):"
echo "    cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo ""
echo "  Terminal 2 (Frontend):"
echo "    cd frontend && npm run dev"
echo ""
echo "🌐 Access the application:"
echo "  Frontend: http://localhost:5173"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
