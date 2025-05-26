@echo off
echo Installing required packages for Deep Character Research...

:: Activate virtual environment
call venv\Scripts\activate

:: Upgrade pip first
python -m pip install --upgrade pip

:: Install core packages
pip install aiohttp
pip install asyncio
pip install requests
pip install beautifulsoup4
pip install lxml
pip install python-dotenv

:: Install AI and ML packages
pip install openai
pip install anthropic

:: Install data science packages
pip install numpy
pip install pandas

:: Install vector database and embeddings
pip install chromadb
pip install sentence-transformers

:: Install scholarly (for Google Scholar)
pip install scholarly

:: Install XML parsing
pip install xmltodict

echo.
echo Installation complete!
echo Don't forget to activate the virtual environment before running:
echo call venv\Scripts\activate

pause