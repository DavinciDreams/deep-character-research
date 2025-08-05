from typing import Dict, List
from dataclasses import dataclass

from research_agent import DeepResearchAgent
from data_sources import DataSourceManager
from storage import VectorDatabase, DocumentStore
from character_engine import CharacterEngine
from ai_providers import AIProviderManager
from config import ResearchConfig
import logging

@dataclass
class CharacterProfile:
    name: str
    time_period: str
    known_roles: List[str]
    research_domains: List[str]
    personality_traits: List[str]
    historical_context: Dict[str, str]
    contemporaries: List[str]

class DeepCharacterResearcher:
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.data_sources = DataSourceManager(config)
        self.vector_db = VectorDatabase(config.vector_db_path)
        self.doc_store = DocumentStore(config.doc_store_path)
        self.research_agent = DeepResearchAgent(self.data_sources)
        
        # Initialize AI Provider Manager
        self.ai_manager = AIProviderManager(config.get_ai_config())
        
        # Initialize Character Engine with AI Manager
        self.character_engine = CharacterEngine(self.vector_db, self.doc_store, self.ai_manager)
        
    async def research_character(self, character_name: str, 
                               research_depth: str = "comprehensive",
                               ai_provider: str = None) -> CharacterProfile:
        """Main orchestration method for deep character research"""
        
        # Use config default if no provider specified
        provider = ai_provider or self.config.default_provider
        logging.info(f"Starting deep research for {character_name} using {provider}")
        
        # Test AI provider connection
        connection_test = await self.ai_manager.test_provider_connection(provider)
        if connection_test["status"] == "error":
            logging.warning(f"Provider {provider} failed: {connection_test['message']}")
            if self.config.fallback_enabled:
                # Try other providers
                for backup_provider in self.ai_manager.get_available_providers():
                    if backup_provider != provider:
                        test = await self.ai_manager.test_provider_connection(backup_provider)
                        if test["status"] == "success":
                            provider = backup_provider
                            logging.info(f"Falling back to {provider}")
                            break
        
        # Phase 1: Initial character discovery
        print("🔍 Phase 1: Discovering character basics...")
        initial_profile = await self._discover_character_basics(character_name)
        
        # Phase 2: Domain-specific deep research
        print("📚 Phase 2: Conducting deep research...")
        research_results = await self._conduct_deep_research(initial_profile, research_depth)
        
        # Phase 3: Knowledge synthesis and storage
        print("💾 Phase 3: Synthesizing and storing knowledge...")
        await self._synthesize_and_store(character_name, research_results)
        
        # Phase 4: Character engine training with specified AI provider
        print("🎭 Phase 4: Training character engine...")
        character_profile = await self._train_character_engine(character_name, initial_profile, provider)
        
        return character_profile
    
    async def chat_with_character(self, character_name: str, message: str, 
                                ai_provider: str = None, model: str = None):
        """Chat with a researched character using specified AI provider"""
        
        # Use config defaults if not specified
        provider = ai_provider or self.config.default_provider
        model = model or self.config.default_model
        
        try:
            response = await self.character_engine.respond_as_character(
                character_name, message, provider, model
            )
            
            print(f"\n{character_name} ({response.provider}/{response.model}):")
            print(f"{response.content}")
            
            if response.tokens_used:
                print(f"\nTokens used: {response.tokens_used}")
            if response.cost:
                print(f"Estimated cost: ${response.cost:.4f}")
                
            return response
            
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    async def compare_ai_responses(self, character_name: str, message: str):
        """Compare responses from different AI providers"""
        
        providers = self.ai_manager.get_available_providers()
        responses = {}
        
        print(f"\nComparing responses from {len(providers)} AI providers for '{message}':\n")
        
        for provider in providers:
            try:
                response = await self.character_engine.respond_as_character(
                    character_name, message, provider
                )
                responses[provider] = response
                
                print(f"--- {provider.upper()} ({response.model}) ---")
                print(f"{response.content}")
                if response.tokens_used:
                    print(f"Tokens: {response.tokens_used}")
                if response.cost:
                    print(f"Cost: ${response.cost:.4f}")
                print()
                
            except Exception as e:
                print(f"--- {provider.upper()} (ERROR) ---")
                print(f"Error: {e}\n")
        
        return responses
    
    async def _train_character_engine(self, character_name: str, initial_profile: Dict, 
                                    provider: str) -> CharacterProfile:
        """Train character engine using specified AI provider"""
        
        profile = await self.character_engine.create_character_embodiment(
            character_name, provider
        )
        return CharacterProfile(
            name=character_name,
            time_period=profile.get('historical_context', {}).get('time_period', 'Unknown'),
            known_roles=profile.get('knowledge_domains', []),
            research_domains=profile.get('knowledge_domains', []),
            personality_traits=profile.get('personality', {}).get('traits', []),
            historical_context=profile.get('historical_context', {}),
            contemporaries=profile.get('contemporaries', [])
        )
    
    async def _discover_character_basics(self, character_name: str) -> Dict:
        """Discover basic information about the character"""
        discovery_queries = [
            f"{character_name} biography historical facts",
            f"{character_name} time period historical context",
            f"{character_name} major accomplishments works",
            f"{character_name} personality contemporary accounts"
        ]
        
        basic_info = {}
        for query in discovery_queries:
            print(f"  🔎 Searching: {query}")
            results = await self.research_agent.search_academic_sources(query)
            basic_info[query] = results
            print(f"    Found {len(results)} sources")
            
        return basic_info
    
    async def _conduct_deep_research(self, initial_profile: Dict, depth: str) -> Dict:
        """Conduct comprehensive domain-specific research"""
        research_domains = self._extract_research_domains(initial_profile)
        
        research_results = {}
        for domain in research_domains:
            print(f"  📖 Researching domain: {domain}")
            domain_results = await self._research_domain(domain, depth)
            research_results[domain] = domain_results
            print(f"    Found {len(domain_results)} sources for {domain}")
            
        return research_results
    
    async def _research_domain(self, domain: str, depth: str) -> List[Dict]:
        """Research a specific domain thoroughly"""
        # Academic sources (ArXiv, Wikipedia, etc.)
        academic_results = await self.research_agent.search_academic_sources(
            f"{domain} historical analysis scholarly research"
        )
        
        # Primary sources (placeholder)
        primary_sources = await self.research_agent.search_primary_sources(domain)
        
        # Contemporary accounts (placeholder)
        contemporary_accounts = await self.research_agent.search_contemporary_sources(domain)
        
        # Cross-reference and validate
        validated_results = await self.research_agent.cross_validate_sources([
            academic_results, primary_sources, contemporary_accounts
        ])
        
        return validated_results
    
    def _extract_research_domains(self, initial_profile: Dict) -> List[str]:
        """Extract research domains from initial profile"""
        # Check if we have any sources to analyze
        all_results = []
        for query, results in initial_profile.items():
            all_results.extend(results)
        
        if not all_results:
            print("  ⚠️  No research results found, using default domains")
            return ["biography", "historical context", "achievements"]
        
        # Extract domains based on found content
        domains = set()
        for result in all_results:
            title = result.title.lower() if hasattr(result, 'title') else ''
            content = result.abstract.lower() if hasattr(result, 'abstract') else ''
            text = title + ' ' + content
            
            if any(word in text for word in ['art', 'painting', 'sculpture']):
                domains.add('art')
            if any(word in text for word in ['science', 'invention', 'engineering']):
                domains.add('science')
            if any(word in text for word in ['politics', 'government', 'leadership']):
                domains.add('politics')
            if any(word in text for word in ['military', 'war', 'battle']):
                domains.add('military')
            if any(word in text for word in ['philosophy', 'thought', 'ideas']):
                domains.add('philosophy')
        
        domain_list = list(domains) if domains else ["biography", "achievements", "historical context"]
        print(f"  📊 Extracted domains: {domain_list}")
        return domain_list
    
    async def _synthesize_and_store(self, character_name: str, research_results: Dict):
        """Synthesize and store research results"""
        # Add character to document store
        character_id = self.doc_store.add_character(character_name)
        print(f"  💾 Created character record with ID: {character_id}")
        
        # Process and store research results
        documents = []
        total_stored = 0
        
        for domain, results in research_results.items():
            print(f"    📄 Storing {len(results)} documents for domain: {domain}")
            
            for result in results:
                doc = {
                    'title': result.title if hasattr(result, 'title') else 'Research Document',
                    'content': result.abstract if hasattr(result, 'abstract') else str(result),
                    'url': result.url if hasattr(result, 'url') else '',
                    'source_type': result.source_type if hasattr(result, 'source_type') else 'unknown',
                    'quality_score': result.quality_score if hasattr(result, 'quality_score') else 0.5,
                    'metadata': {
                        'domain': domain,
                        'authors': result.authors if hasattr(result, 'authors') else [],
                        'publication_date': result.publication_date if hasattr(result, 'publication_date') else '',
                        'language': result.language if hasattr(result, 'language') else 'en'
                    }
                }
                
                # Add to document store
                doc_id = self.doc_store.add_document(character_id, doc)
                documents.append(doc)
                total_stored += 1
        
        print(f"  ✅ Stored {total_stored} documents total")
        
        # Add to vector database
        if documents:
            print(f"  🔢 Adding {len(documents)} documents to vector database...")
            self.vector_db.add_documents(character_name, documents)
            print(f"  ✅ Vector database updated")
        else:
            print(f"  ⚠️  No documents to add to vector database")
    
    def filter_characters_by_profession(self, profession: str) -> List[CharacterProfile]:
        """
        Filter stored characters by profession (known_roles).
        This is a backend utility; actual storage/retrieval logic may need to be adapted.
        """
        profiles = self.doc_store.get_all_character_profiles()  # Assumes such a method exists
        return [
            profile for profile in profiles
            if profession.lower() in (role.lower() for role in profile.known_roles)
        ]

    async def cleanup(self):
        """Cleanup resources"""
        await self.ai_manager.close_all()
        await self.research_agent.close()
        await self.data_sources.close()