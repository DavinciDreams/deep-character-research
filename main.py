from dotenv import load_dotenv
load_dotenv()
import uvicorn
from api import app

import asyncio
import logging
from config import ResearchConfig
from deep_character_researcher import DeepCharacterResearcher, CharacterProfile


async def main():
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    
    try:
        # Example: Research Julius Caesar using config defaults
        print("Starting research on Julius Caesar...")
        print(f"Using provider: {config.default_provider}")
        print(f"Using model: {config.default_model}")
        
        character_profile = await researcher.research_character(
            "Julius Caesar", 
            "comprehensive"
            # No need to specify ai_provider - will use config default
        )
        
        print(f"Research complete for {character_profile.name}")
        print(f"Domains: {character_profile.research_domains}")
        
        # Interactive chat
        print("\n" + "="*50)
        print(f"Chat with {character_profile.name}")
        print("Type 'quit' to exit, 'compare' to see all AI responses")
        print("Type 'switch <provider> [model]' to change AI provider/model")
        print("="*50)
        
        current_provider = config.default_provider
        current_model = config.default_model
        
        while True:
            user_input = input(f"\nYou ({current_provider}/{current_model}): ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'compare':
                query = input("Enter question to compare across providers: ")
                await researcher.compare_ai_responses(character_profile.name, query)
            elif user_input.lower().startswith('switch '):
                parts = user_input.split(' ')
                new_provider = parts[1]
                new_model = parts[2] if len(parts) > 2 else current_model
                
                if new_provider in researcher.ai_manager.get_available_providers():
                    current_provider = new_provider
                    current_model = new_model
                    print(f"Switched to {current_provider}/{current_model}")
                else:
                    print(f"Provider {new_provider} not available")
                    print(f"Available: {researcher.ai_manager.get_available_providers()}")
            elif user_input:
                await researcher.chat_with_character(
                    character_profile.name, 
                    user_input, 
                    current_provider,
                    current_model
                )
    
    finally:
        await researcher.cleanup()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)