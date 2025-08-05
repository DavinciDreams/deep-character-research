import asyncio
import sys
import signal
from backend.main import DeepCharacterResearcher
from backend.config import ResearchConfig

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print("\n\n🛑 Received interrupt signal. Cleaning up...")
    raise KeyboardInterrupt

async def research_and_chat(character_name: str, research_depth: str = "comprehensive"):
    """Research a character and start interactive chat"""
    
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    
    try:
        print(f"🔍 Starting research on {character_name}...")
        print(f"📊 Research depth: {research_depth}")
        print(f"🤖 AI Provider: {config.default_provider}")
        print(f"🧠 Model: {config.default_model}")
        print(f"💾 Data stored in: {config.base_data_dir}")
        print("⏳ This may take several minutes...\n")
        
        # Use config defaults
        character_profile = await researcher.research_character(
            character_name, 
            research_depth,
            ai_provider=config.default_provider
        )
        
        print(f"✅ Research complete for {character_profile.name}")
        print(f"📚 Knowledge domains: {character_profile.research_domains}")
        print(f"🎭 Personality traits: {character_profile.personality_traits}")
        
        # Start interactive chat
        print(f"\n{'='*60}")
        print(f"💬 Chat with {character_profile.name}")
        print("Commands:")
        print("  - Type 'quit' to exit")
        print("  - Type 'compare' to see responses from all AI providers")
        print("  - Type 'switch <provider> [model]' to change AI provider/model")
        print("  - Type 'info' to see character profile")
        print(f"{'='*60}")
        
        current_provider = config.default_provider
        current_model = config.default_model
        
        while True:
            try:
                user_input = input(f"\nYou ({current_provider}/{current_model}): ").strip()
                
                if user_input.lower() == 'quit':
                    break
                elif user_input.lower() == 'info':
                    print(f"\n📋 Character Profile for {character_profile.name}:")
                    print(f"⏰ Time period: {character_profile.time_period}")
                    print(f"🎯 Roles: {character_profile.known_roles}")
                    print(f"📚 Domains: {character_profile.research_domains}")
                    print(f"🎭 Traits: {character_profile.personality_traits}")
                elif user_input.lower() == 'compare':
                    query = input("Enter question to compare across providers: ")
                    await researcher.compare_ai_responses(character_profile.name, query)
                elif user_input.lower().startswith('switch '):
                    parts = user_input.split(' ')
                    new_provider = parts[1]
                    new_model = parts[2] if len(parts) > 2 else None
                    
                    if new_provider in researcher.ai_manager.get_available_providers():
                        current_provider = new_provider
                        if new_model:
                            current_model = new_model
                        print(f"🔄 Switched to {current_provider}")
                        if new_model:
                            print(f"🧠 Using model: {current_model}")
                    else:
                        print(f"❌ Provider {new_provider} not available")
                        print(f"Available: {researcher.ai_manager.get_available_providers()}")
                elif user_input:
                    await researcher.chat_with_character(
                        character_profile.name, 
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
    
    except KeyboardInterrupt:
        print("\n\n🛑 Research interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during research: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("\n🧹 Cleaning up resources...")
        try:
            await researcher.cleanup()
            print("✅ Cleanup complete")
        except Exception as e:
            print(f"⚠️ Cleanup warning: {e}")

if __name__ == "__main__":
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Get character name from command line or prompt
    if len(sys.argv) > 1:
        character_name = " ".join(sys.argv[1:])
    else:
        character_name = input("Enter character name to research: ")
    
    # Optional: get research depth
    depth = input("Research depth (basic/comprehensive/exhaustive) [comprehensive]: ").strip()
    if not depth:
        depth = "comprehensive"
    
    try:
        asyncio.run(research_and_chat(character_name, depth))
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")