#!/bin/bash

echo "🧪 Testing Trading Research Agent Backend"
echo ""

# Start backend in background
echo "Starting backend..."
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

echo ""
echo "✅ Backend running on http://localhost:8000"
echo ""

# Test health check
echo "Testing health check..."
curl -s http://localhost:8000/ | python3 -m json.tool
echo ""

# Test analysis endpoint
echo ""
echo "Testing stock analysis for AAPL..."
echo "(This will take ~10 seconds)"
curl -s -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL"}' | python3 -m json.tool | head -50

echo ""
echo ""
echo "✅ Backend is working!"
echo ""
echo "API Documentation: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop the backend"

# Wait for Ctrl+C
trap "kill $BACKEND_PID 2>/dev/null; exit" INT
wait

