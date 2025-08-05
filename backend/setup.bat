:: filepath: c:\Users\lmwat\deep character research\setup.bat
@echo off
echo Setting up Deep Character Research environment...

:: Create virtual environment
python -m venv venv
call venv\Scripts\activate

:: Install required packages
pip install --upgrade pip
pip install aiohttp asyncio
pip install chromadb sentence-transformers
pip install beautifulsoup4 lxml
pip install scholarly
pip install openai anthropic
pip install numpy pandas
pip install python-dotenv
pip install sqlite3

:: Create directory structure
mkdir data
mkdir data\vector_db
mkdir data\document_store
mkdir logs
mkdir characters

echo Setup complete! 
echo.
echo Don't forget to set your API keys in the .env file:
echo - OPENAI_API_KEY=your_key_here
echo - OPENROUTER_API_KEY=your_key_here  
echo - ANTHROPIC_API_KEY=your_key_here
echo.
echo For LM Studio, make sure it's running on localhost:1234
echo.
echo Available AI providers:
echo - OpenAI (GPT-4, GPT-3.5-turbo)
echo - OpenRouter (Claude, Llama, Mixtral, Gemini, etc.)
echo - LM Studio (Local models)

pause