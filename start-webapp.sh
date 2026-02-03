#!/bin/bash

echo "🚀 Starting Trading Research Agent..."
echo ""

# Start backend
echo "Starting backend on http://localhost:8000"
cd backend
python3 main.py &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start frontend
echo "Starting frontend on http://localhost:3000"
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✨ Ready! Open http://localhost:3000 in your browser"
echo ""
echo "Press Ctrl+C to stop"

# Stop both on Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait

