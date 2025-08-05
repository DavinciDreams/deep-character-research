import asyncio
import sys
from backend.main import DeepCharacterResearcher
from backend.config import ResearchConfig

async def quick_chat(character_name: str):
    """Quick chat with a character (assumes already researched)"""
    
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    
    try:
        print(f"💬 Starting chat with {character_name}")
        print(f"🤖 Using: {config.default_provider}/{config.default_model}")
        print(f"💾 Data from: {config.base_data_dir}")
        
        # Check if character exists in database
        docs = researcher.doc_store.get_character_documents(character_name)
        if not docs:
            print(f"\n❌ No research data found for {character_name}")
            print("Please run research first:")
            print(f'python research_character.py "{character_name}"')
            return
        
        print(f"✅ Found {len(docs)} documents for {character_name}")
        
        # Start chat
        print(f"\n{'='*60}")
        print(f"💬 Chat with {character_name}")
        print("Commands:")
        print("  - Type 'quit' to exit")
        print("  - Type 'info' to see character profile")
        print("  - Type 'switch <provider> [model]' to change AI provider")
        print(f"{'='*60}")
        
        current_provider = config.default_provider
        current_model = config.default_model
        
        while True:
            try:
                user_input = input(f"\nYou ({current_provider}/{current_model}): ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'info':
                    # Show character info
                    profile = await researcher.character_engine.create_character_embodiment(character_name)
                    print(f"\n📋 Character Profile for {character_name}:")
                    print(f"⏰ Time period: {profile.get('historical_context', {}).get('time_period', 'Unknown')}")
                    print(f"🎭 Traits: {profile.get('personality', {}).get('traits', [])}")
                    print(f"📚 Domains: {profile.get('knowledge_domains', [])}")
                elif user_input.lower().startswith('switch '):
                    parts = user_input.split(' ')
                    new_provider = parts[1]
                    new_model = parts[2] if len(parts) > 2 else current_model
                    
                    if new_provider in researcher.ai_manager.get_available_providers():
                        current_provider = new_provider
                        current_model = new_model
                        print(f"🔄 Switched to {current_provider}/{current_model}")
                    else:
                        print(f"❌ Provider {new_provider} not available")
                        print(f"Available: {researcher.ai_manager.get_available_providers()}")
                elif user_input:
                    await researcher.chat_with_character(
                        character_name, 
                        user_input, 
                        current_provider,
                        current_model
                    )
                    
            except KeyboardInterrupt:
                print("\n\n🛑 Exiting chat...")
                break
            except EOFError:
                print("\n\n🛑 End of input, exiting...")
                break
    
    except Exception as e:
        print(f"\n❌ Error during chat: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🧹 Cleaning up...")
        await researcher.cleanup()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        character_name = " ".join(sys.argv[1:])
    else:
        character_name = input("Enter character name to chat with: ")
    
    asyncio.run(quick_chat(character_name))