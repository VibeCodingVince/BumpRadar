#!/bin/bash

echo "🚀 Starting BumpRadar App..."
echo ""

# Kill any existing processes on these ports
echo "Cleaning up old processes..."
lsof -ti:8000 | xargs kill -9 2>/dev/null || true
lsof -ti:3000 | xargs kill -9 2>/dev/null || true

echo ""
echo "Starting Backend Server (Port 8000)..."
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --timeout-keep-alive 30 &
BACKEND_PID=$!

sleep 3

echo ""
echo "Starting Frontend Server (Port 3000)..."
cd ../frontend
python simple_server.py &
FRONTEND_PID=$!

echo ""
echo "============================================"
echo "✅ BumpRadar is now running!"
echo "============================================"
echo ""
echo "📱 On your phone, open:"
echo "   http://192.168.2.10:3000"
echo ""
echo "💻 On this computer:"
echo "   http://localhost:3000"
echo ""
echo "Backend API: http://localhost:8000"
echo ""
echo "Make sure your phone is on the same WiFi network!"
echo ""
echo "Press Ctrl+C to stop both servers"
echo "============================================"
echo ""

# Wait for both processes
wait $BACKEND_PID $FRONTEND_PID
