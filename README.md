# Deep Character Research 🎭

An advanced AI-powered system for researching historical figures and engaging in authentic conversations with them. This project combines deep web research, vector databases, and multiple AI providers to create historically accurate character embodiments.

## 🌟 Features

- **Multi-Source Research**: Automatically gathers information from Wikipedia (multiple languages), ArXiv, Wikidata
- **AI-Powered Analysis**: Uses multiple AI providers to analyze personality traits and historical context
- **Vector Database Storage**: Efficient semantic search through ChromaDB
- **Character Embodiment**: Creates authentic character personalities based on research
- **Multi-Provider AI Chat**: Switch between OpenAI, OpenRouter, and LM Studio
- **Cross-Language Support**: Researches in native languages for better historical accuracy

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or download the project
cd "deep character research"

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

Create a `.env` file in the project root:

```env
# AI Provider API Keys (at least one required)
OPENROUTER_API_KEY=your_openrouter_key_here
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# LM Studio (if running locally)
LMSTUDIO_BASE_URL=http://localhost:1234
LMSTUDIO_MODEL=local-model

# Default settings
DEFAULT_AI_PROVIDER=openrouter
DEFAULT_MODEL=nvidia/llama-3.1-nemotron-ultra-253b-v1:free
```

### 3. Research a Character

```bash
# Research and chat with Leonardo da Vinci
python research_character.py "Leonardo da Vinci"

# Research with specific depth
python research_character.py "Julius Caesar"
# When prompted, choose: basic/comprehensive/exhaustive
```

### 4. Quick Chat (if already researched)

```bash
# Chat with previously researched character
python chat_only.py "Leonardo da Vinci"
```

## 📁 Project Structure

```
deep character research/
├── main.py                 # Core research orchestration
├── research_character.py   # Research + chat interface
├── chat_only.py           # Quick chat interface
├── config.py              # Configuration management
├── ai_providers.py        # Multi-provider AI interface
├── research_agent.py      # Web research engine
├── character_engine.py    # Character personality engine
├── storage.py             # Database storage (SQLite + ChromaDB)
├── data_sources.py        # Data source management
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables
└── README.md              # This file
```

## 🎮 Usage Examples

### Research a Character
```bash
python research_character.py "Marie Curie"
```

Output:
```
🔍 Starting research on Marie Curie...
📊 Research depth: comprehensive
🤖 AI Provider: openrouter
🧠 Model: nvidia/llama-3.1-nemotron-ultra-253b-v1:free
💾 Data stored in: C:\Users\username\Documents\DeepCharacterResearch

🔍 Phase 1: Discovering character basics...
  🔎 Searching: Marie Curie biography historical facts
    Found 3 sources
  📖 Researching domain: science
    Found 5 sources for science

✅ Research complete for Marie Curie
📚 Knowledge domains: ['Science & Engineering', 'Chemistry', 'Physics']
🎭 Personality traits: ['Determined', 'Pioneering', 'Methodical']
```

### Chat Interface
```
============================================================
💬 Chat with Marie Curie
Commands:
  - Type 'quit' to exit
  - Type 'info' to see character profile
  - Type 'switch <provider>' to change AI provider
============================================================

You (openrouter/nvidia/llama-3.1-nemotron-ultra-253b-v1:free): What motivated you to study radioactivity?

Marie Curie (openrouter/nvidia/llama-3.1-nemotron-ultra-253b-v1:free):
Ah, mon ami, it was the mysterious rays discovered by Henri Becquerel that captured my imagination completely! When I learned that uranium salts could emit these invisible rays without any external energy source, I knew I had found my life's work.

Pierre and I set up our laboratory in that freezing shed, and despite the harsh conditions, we were driven by pure scientific curiosity. The possibility that matter itself could spontaneously emit energy challenged everything we knew about physics...
```

### Chat Commands

- `quit` - Exit the chat
- `info` - Show character profile and research domains
- `switch openai` - Change to OpenAI provider
- `switch lmstudio gpt-3.5-turbo` - Change provider and model
- `compare` - Compare responses from all available AI providers

## 🔧 Configuration Options

### Research Depth
- **basic**: Core biographical information
- **comprehensive**: Multi-domain research with personality analysis
- **exhaustive**: Deep cross-referenced research (slower but more thorough)

### AI Providers
- **OpenRouter**: Access to 100+ models (many free)
- **OpenAI**: GPT-3.5, GPT-4 models
- **LM Studio**: Local model hosting
- **Anthropic**: Claude models (coming soon)

### Supported Characters
The system works best with well-documented historical figures:
- **Renaissance**: Leonardo da Vinci, Michelangelo, Galileo
- **Scientists**: Einstein, Marie Curie, Newton
- **Leaders**: Julius Caesar, Napoleon, Churchill
- **Artists**: Picasso, Van Gogh, Beethoven
- **Philosophers**: Plato, Aristotle, Kant

## 🔍 How It Works

### 1. Research Phase
```
Character Input → Multi-Source Search → Content Analysis → Domain Extraction
```

- Searches Wikipedia in native languages (Italian for da Vinci, French for Napoleon)
- Gathers academic papers from ArXiv
- Extracts structured data from Wikidata
- Cross-validates information across sources

### 2. Analysis Phase
```
Raw Data → AI Analysis → Personality Extraction → Historical Context
```

- Uses AI to analyze personality traits from historical accounts
- Extracts knowledge domains (art, science, politics, etc.)
- Determines speech patterns and response style
- Compiles historical context and time period

### 3. Storage Phase
```
Processed Data → SQLite Database → ChromaDB Vector Store
```

- Stores documents in SQLite for structured queries
- Creates vector embeddings for semantic search
- Enables fast retrieval of relevant information

### 4. Chat Phase
```
User Query → Vector Search → Context Building → AI Generation → Character Response
```

- Searches for relevant historical context
- Builds character-appropriate prompts
- Generates responses using selected AI provider
- Maintains historical accuracy and personality consistency

## 📊 Research Quality

The system ensures high-quality character embodiments through:

- **Multi-language sources**: Researches in native languages for authenticity
- **Source validation**: Cross-references multiple sources
- **Quality scoring**: Ranks sources by reliability and relevance
- **AI analysis**: Uses advanced models to extract nuanced personality traits
- **Historical accuracy**: Maintains period-appropriate knowledge and perspectives

## 🛠️ Advanced Usage

### Custom Research Domains
```python
# Modify _extract_research_domains() in main.py to add custom domains
domains.add('medicine')
domains.add('literature')
```

### Custom AI Providers
```python
# Add new providers in ai_providers.py
class CustomProvider(BaseAIProvider):
    # Implementation here
```

### Batch Character Research
```python
characters = ["Einstein", "Curie", "Darwin"]
for character in characters:
    await researcher.research_character(character)
```

## 🐛 Troubleshooting

### Common Issues

**"No research data found"**
```bash
# Re-run research first
python research_character.py "Character Name"
```

**"Provider not available"**
```bash
# Check your .env file has valid API keys
# Test connection: python -c "from config import ResearchConfig; print(ResearchConfig().openrouter_api_key)"
```

**"Database permission error"**
```bash
# Data is stored in: Documents/DeepCharacterResearch/
# Make sure you have write permissions to your Documents folder
```

**Wikipedia API errors**
```bash
# The system includes rate limiting and error handling
# If Wikipedia is temporarily unavailable, other sources will be used
```

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add new AI providers, research sources, or character analysis methods
4. Submit a pull request

### Ideas for Contributions
- Additional research sources (Project Gutenberg, historical archives)
- More sophisticated personality analysis
- Voice synthesis for character responses
- Visual character representation
- Historical fact-checking system

## 📜 License

This project is for educational and research purposes. Please respect the terms of service of all external APIs and data sources used.

## 🙏 Acknowledgments

- **Wikipedia**: Primary source of multilingual historical information
- **ArXiv**: Academic research papers
- **Wikidata**: Structured historical data
- **OpenRouter**: Access to diverse AI models
- **ChromaDB**: Vector database for semantic search

## 🛡️ FastAPI Backend API

The backend provides three main endpoints for character research and interaction.

---

### `POST /research_character`

**Purpose:**
Initiate deep research on a historical character, gathering information and generating a personality profile.

**Request JSON:**
```json
{
  "character_name": "string",         // Name of the character to research (required)
  "research_depth": "string",         // Research depth: "basic", "comprehensive", or "exhaustive" (optional, default: "comprehensive")
  "ai_provider": "string"             // AI provider to use (optional)
}
```

**Example Request:**
```http
POST /research_character
Content-Type: application/json

{
  "character_name": "Leonardo da Vinci",
  "research_depth": "comprehensive",
  "ai_provider": "openrouter"
}
```

**Example Response:**
```json
{
  "character_name": "Leonardo da Vinci",
  "personality_traits": ["Curious", "Inventive", "Analytical"],
  "knowledge_domains": ["Art", "Science", "Engineering"],
  "sources": [
    {"title": "Wikipedia", "url": "..."},
    {"title": "ArXiv", "url": "..."}
  ],
  "summary": "Leonardo da Vinci was a Renaissance polymath..."
}
```

---

### `POST /chat_with_character`

**Purpose:**
Send a message to a researched character and receive an AI-generated response in their persona.

**Request JSON:**
```json
{
  "character_name": "string",         // Name of the character to chat with (required)
  "message": "string",                // User's message to the character (required)
  "ai_provider": "string",            // AI provider to use (optional)
  "model": "string"                   // Specific model to use (optional)
}
```

**Example Request:**
```http
POST /chat_with_character
Content-Type: application/json

{
  "character_name": "Leonardo da Vinci",
  "message": "What inspired your inventions?",
  "ai_provider": "openrouter"
}
```

**Example Response:**
```json
{
  "response": "Curiosity has always been my guiding force. The wonders of nature inspired many of my inventions..."
}
```

---

### `POST /compare_ai_responses`

**Purpose:**
Send a message to a character and compare responses from all available AI providers.

**Request JSON:**
```json
{
  "character_name": "string",         // Name of the character (required)
  "message": "string"                 // User's message to the character (required)
}
```

**Example Request:**
```http
POST /compare_ai_responses
Content-Type: application/json

{
  "character_name": "Leonardo da Vinci",
  "message": "Describe your artistic process."
}
```

**Example Response:**
```json
{
  "openai": {
    "response": "My artistic process begins with careful observation of nature..."
  },
  "openrouter": {
    "response": "For me, art and science are intertwined. I study anatomy to improve my paintings..."
  }
}
```

---

**Note:**
All endpoints return HTTP 500 with a JSON error message if an internal error occurs.

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Ensure all dependencies are installed correctly
3. Verify your API keys are valid
4. Check that you have internet connectivity for research

---

**Start your journey through history! Research any historical figure and engage in authentic conversations that bring the past to life.** 🚀📚