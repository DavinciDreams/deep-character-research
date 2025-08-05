@echo off
echo ===============================================
echo  Deep Character Research - START SCRIPT
echo ===============================================
echo.

echo [1/6] Clearing Python cache files...
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo     ✓ Cleared __pycache__ directory
) else (
    echo     ✓ No __pycache__ directory found
)

echo.
echo [2/6] Running environment diagnostic...
python check_env.py

echo.
echo [3/6] Checking current environment configuration...
echo     Reading .env file...
findstr "DEFAULT_MODEL" .env
findstr "DEFAULT_AI_PROVIDER" .env
echo.

echo [4/6] Testing environment variable loading...
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'     DEFAULT_MODEL from env: {os.getenv(\"DEFAULT_MODEL\")}'); print(f'     DEFAULT_AI_PROVIDER from env: {os.getenv(\"DEFAULT_AI_PROVIDER\")}')"
echo.

echo [5/6] Testing AI configuration...
python -c "from config import ResearchConfig; from ai_providers import AIConfig; config = ResearchConfig(); ai_config = config.get_ai_config(); print(f'     Config default_model: {config.default_model}'); print(f'     AIConfig default_model: {ai_config.default_model}')"
echo.

echo [6/6] Starting application...
echo     Choose startup option:
echo     1. Main application (main.py)
echo     2. Quick start (quick_start.py)
echo     3. Chat only (chat_only.py)
echo     4. Character research (research_character.py)
echo     5. Environment check only (exit after diagnostics)
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo Starting main application...
    python main.py
) else if "%choice%"=="2" (
    echo Starting quick start...
    python quick_start.py
) else if "%choice%"=="3" (
    echo Starting chat only...
    python chat_only.py
) else if "%choice%"=="4" (
    echo Starting character research...
    python research_character.py
) else if "%choice%"=="5" (
    echo Environment check completed. Exiting...
    goto :end
) else (
    echo Invalid choice. Starting main application...
    python main.py
)

:end
echo.
echo Application finished.
pause
