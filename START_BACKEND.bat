@echo off
echo ========================================
echo Starting Conversational RAG Backend
echo ========================================
echo.
echo Backend will run on: http://localhost:8000
echo API Docs available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
