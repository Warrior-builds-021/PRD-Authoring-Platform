@echo off
cd /d "%~dp0"
echo.
echo ================================================
echo   🚀 Starting PRD Creator Platform...
echo ================================================
echo.
echo Open your browser to: http://localhost:8501
echo Press Ctrl+C to stop the server
echo ================================================
echo.
python -m streamlit run app.py --server.port=8501
pause