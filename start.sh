#!/bin/bash

echo "🚀 Starting User Management API..."
echo "📦 Installing dependencies..."
pip install -r requirements.txt

echo "🔧 Starting FastAPI server..."
echo "📖 Swagger UI will be available at: http://localhost:8000/docs"
echo "📖 ReDoc will be available at: http://localhost:8000/redoc"
echo "🌐 API base URL: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

python app.py 