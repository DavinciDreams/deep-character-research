import asyncio
from main import DeepCharacterResearcher
from config import ResearchConfig

async def quick_research():
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    
    print("🚀 Deep Character Research System")
    print(f"🤖 Using AI Provider: {config.default_provider}")
    print(f"🧠 Default Model: {config.default_model}")
    print()
    print("Available characters (examples):")
    print("  - Julius Caesar")
    print("  - Leonardo da Vinci") 
    print("  - Marie Curie")
    print("  - Winston Churchill")
    print("  - Cleopatra")
    print("  - Albert Einstein")
    
    character = input("\n📝 Enter character name: ")
    
    try:
        # Use the default provider from config instead of hardcoded "openai"
        profile = await researcher.research_character(
            character, 
            "comprehensive", 
            ai_provider=config.default_provider  # This was missing!
        )
        
        print(f"\n✅ {character} is ready for conversation!")
        
        # Quick test conversation using default provider and model
        response = await researcher.chat_with_character(
            character, 
            "Hello! Please introduce yourself and tell me about your most important work.",
            ai_provider=config.default_provider,
            model=config.default_model
        )
        
    finally:
        await researcher.cleanup()

if __name__ == "__main__":
    asyncio.run(quick_research())