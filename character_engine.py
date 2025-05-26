from typing import List, Dict, Any, Optional
from storage import VectorDatabase, DocumentStore
from ai_providers import AIProviderManager
import json
import asyncio
from dataclasses import dataclass
import logging

@dataclass
class AIResponse:
    content: str
    provider: str
    model: str
    tokens_used: Optional[int] = None
    cost: Optional[float] = None

class CharacterEngine:
    def __init__(self, vector_db: VectorDatabase, doc_store: DocumentStore, 
                 ai_manager: AIProviderManager):
        self.vector_db = vector_db
        self.doc_store = doc_store
        self.ai_manager = ai_manager
        self.character_profiles = {}
        
    async def create_character_embodiment(self, character_name: str, 
                                        provider: str = "openrouter") -> Dict[str, Any]:
        """Create a comprehensive character embodiment"""
        
        # Retrieve all character knowledge
        documents = self.doc_store.get_character_documents(character_name)
        
        if not documents:
            # If no documents found, create a basic profile
            return {
                "name": character_name,
                "personality": {"traits": []},
                "knowledge_domains": ["General Knowledge"],
                "speech_patterns": {},
                "response_style": "formal",
                "core_beliefs": [],
                "historical_context": {"time_period": "Unknown"}
            }
        
        # Analyze knowledge to extract character traits
        personality_analysis = await self._analyze_personality(character_name, documents, provider)
        knowledge_domains = await self._extract_knowledge_domains(character_name, documents, provider)
        speech_patterns = await self._analyze_speech_patterns(character_name, documents, provider)
        
        # Create character profile
        character_profile = {
            "name": character_name,
            "personality": personality_analysis,
            "knowledge_domains": knowledge_domains,
            "speech_patterns": speech_patterns,
            "response_style": await self._determine_response_style(character_name, documents, provider),
            "core_beliefs": await self._extract_core_beliefs(character_name, documents, provider),
            "historical_context": await self._compile_historical_context(character_name, documents, provider)
        }
        
        self.character_profiles[character_name] = character_profile
        return character_profile
    
    async def respond_as_character(self, character_name: str, query: str, 
                                 provider: str = "openrouter", model: str = None) -> AIResponse:
        """Generate a response as the character"""
        
        # Get character profile
        if character_name not in self.character_profiles:
            await self.create_character_embodiment(character_name, provider)
        
        profile = self.character_profiles.get(character_name, {})
        
        # Get relevant documents for context
        relevant_docs = self.vector_db.search_similar(character_name, query, limit=5)
        
        # Build context from documents
        context = self._build_context_from_documents(relevant_docs)
        
        # Create character prompt
        character_prompt = self._build_character_prompt(profile, context, query)
        
        # Generate response using AI provider
        try:
            response = await self.ai_manager.generate_response(
                provider, character_prompt, model
            )
            
            return AIResponse(
                content=response.get('content', 'I cannot respond at this time.'),
                provider=provider,
                model=response.get('model', model or 'unknown'),
                tokens_used=response.get('tokens_used'),
                cost=response.get('cost')
            )
            
        except Exception as e:
            logging.error(f"Error generating character response: {e}")
            return AIResponse(
                content=f"I apologize, but I'm having trouble responding right now. Error: {e}",
                provider=provider,
                model=model or 'unknown'
            )
    
    async def _analyze_personality(self, character_name: str, documents: List[Dict], 
                                 provider: str) -> Dict[str, Any]:
        """Analyze personality traits from documents"""
        
        if not documents:
            return {"traits": [], "description": "Personality analysis unavailable"}
        
        # Combine document content for analysis
        combined_text = "\n".join([doc.get('content', doc.get('abstract', '')) for doc in documents[:3]])
        
        prompt = f"""Analyze the personality of {character_name} based on this historical information:

{combined_text[:2000]}

Extract key personality traits, temperament, and character qualities. Respond in JSON format:
{{
    "traits": ["trait1", "trait2", "trait3"],
    "temperament": "description",
    "notable_qualities": ["quality1", "quality2"],
    "description": "brief personality summary"
}}"""

        try:
            response = await self.ai_manager.generate_response(provider, prompt)
            
            # Try to parse JSON response
            content = response.get('content', '{}')
            try:
                personality_data = json.loads(content)
                return personality_data
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                return {
                    "traits": ["Intelligent", "Creative", "Determined"],
                    "temperament": "Complex and multifaceted",
                    "description": content[:200]
                }
                
        except Exception as e:
            logging.error(f"Error analyzing personality: {e}")
            return {"traits": ["Historical Figure"], "description": "Analysis unavailable"}
    
    async def _extract_knowledge_domains(self, character_name: str, documents: List[Dict], 
                                       provider: str) -> List[str]:
        """Extract knowledge domains from documents"""
        
        if not documents:
            return ["General Knowledge"]
        
        # Extract domains from document metadata and content
        domains = set()
        
        for doc in documents:
            # Check metadata for domains
            metadata = doc.get('metadata', {})
            if 'domain' in metadata:
                domains.add(metadata['domain'])
            
            # Analyze content for implicit domains
            content = doc.get('content', doc.get('abstract', ''))
            title = doc.get('title', '')
            
            # Simple keyword-based domain detection
            text = (title + ' ' + content).lower()
            
            if any(word in text for word in ['art', 'paint', 'sculpture', 'drawing']):
                domains.add('Art')
            if any(word in text for word in ['science', 'engineer', 'invention', 'machine']):
                domains.add('Science & Engineering')
            if any(word in text for word in ['anatomy', 'medical', 'body', 'dissection']):
                domains.add('Anatomy & Medicine')
            if any(word in text for word in ['military', 'war', 'battle', 'strategy']):
                domains.add('Military Strategy')
            if any(word in text for word in ['philosophy', 'thought', 'idea', 'belief']):
                domains.add('Philosophy')
            if any(word in text for word in ['mathematics', 'geometry', 'calculation']):
                domains.add('Mathematics')
            if any(word in text for word in ['architecture', 'building', 'design']):
                domains.add('Architecture')
        
        return list(domains) if domains else ["General Knowledge"]
    
    async def _analyze_speech_patterns(self, character_name: str, documents: List[Dict], 
                                     provider: str) -> Dict[str, Any]:
        """Analyze speech patterns and communication style"""
        
        # For now, return basic patterns based on historical period
        time_period = await self._determine_time_period(character_name, documents)
        
        if "renaissance" in time_period.lower() or "15th" in time_period or "16th" in time_period:
            return {
                "style": "Renaissance formal",
                "characteristics": ["Eloquent", "Learned", "Artistic"],
                "typical_phrases": ["Indeed", "Perchance", "I observe that"]
            }
        else:
            return {
                "style": "Historical formal",
                "characteristics": ["Thoughtful", "Articulate"],
                "typical_phrases": ["I believe", "In my experience", "It is my view"]
            }
    
    async def _determine_response_style(self, character_name: str, documents: List[Dict], 
                                      provider: str) -> str:
        """Determine overall response style"""
        
        # Simple heuristic based on character
        name_lower = character_name.lower()
        
        if any(word in name_lower for word in ['da vinci', 'leonardo', 'michelangelo']):
            return "Renaissance master - thoughtful, artistic, scientific"
        elif any(word in name_lower for word in ['caesar', 'napoleon']):
            return "Military leader - confident, strategic, authoritative"
        elif any(word in name_lower for word in ['einstein', 'curie']):
            return "Scientist - curious, analytical, methodical"
        else:
            return "Historical figure - knowledgeable, reflective"
    
    async def _extract_core_beliefs(self, character_name: str, documents: List[Dict], 
                                  provider: str) -> List[str]:
        """Extract core beliefs and values"""
        
        # Basic beliefs based on character type
        name_lower = character_name.lower()
        
        if 'da vinci' in name_lower or 'leonardo' in name_lower:
            return [
                "Knowledge comes through observation and experience",
                "Art and science are interconnected",
                "Human potential is limitless",
                "Nature is the supreme teacher"
            ]
        else:
            return [
                "Learning and knowledge are valuable",
                "Human achievement matters",
                "History shapes the present"
            ]
    
    async def _compile_historical_context(self, character_name: str, documents: List[Dict], 
                                        provider: str) -> Dict[str, str]:
        """Compile historical context information"""
        
        time_period = await self._determine_time_period(character_name, documents)
        
        context = {
            "time_period": time_period,
            "cultural_context": "Historical period of significant change",
            "major_events": "Various historical developments",
            "social_environment": "Complex social structures of the time"
        }
        
        # Enhance based on character
        name_lower = character_name.lower()
        if 'da vinci' in name_lower or 'leonardo' in name_lower:
            context.update({
                "time_period": "Italian Renaissance (1452-1519)",
                "cultural_context": "Rebirth of art, science, and learning",
                "major_events": "Discovery of the Americas, rise of humanism",
                "social_environment": "Patronage system, city-states, artistic workshops"
            })
        
        return context
    
    async def _determine_time_period(self, character_name: str, documents: List[Dict]) -> str:
        """Determine the character's historical time period"""
        
        # Check documents for date information
        for doc in documents:
            content = doc.get('content', '') + ' ' + doc.get('abstract', '')
            
            # Look for date patterns
            import re
            
            # Look for birth/death dates
            date_patterns = [
                r'(\d{4})-(\d{4})',  # 1452-1519
                r'born.*?(\d{4})',   # born 1452
                r'died.*?(\d{4})',   # died 1519
                r'(\d{4}).*?(\d{4})', # 1452 ... 1519
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, content)
                if matches:
                    if isinstance(matches[0], tuple):
                        return f"{matches[0][0]}-{matches[0][1]}"
                    else:
                        return f"Around {matches[0]}"
        
        # Fallback based on character name
        name_lower = character_name.lower()
        if 'da vinci' in name_lower or 'leonardo' in name_lower:
            return "Italian Renaissance (1452-1519)"
        elif 'caesar' in name_lower:
            return "Roman Republic (100-44 BCE)"
        elif 'napoleon' in name_lower:
            return "Early 19th Century (1769-1821)"
        
        return "Historical period"
    
    def _build_context_from_documents(self, documents: List[Dict]) -> str:
        """Build context string from relevant documents"""
        
        if not documents:
            return "Limited historical information available."
        
        context_parts = []
        for doc in documents[:3]:  # Use top 3 most relevant
            title = doc.get('title', 'Historical Document')
            content = doc.get('content', doc.get('abstract', ''))
            
            # Truncate content
            content_snippet = content[:300] + "..." if len(content) > 300 else content
            context_parts.append(f"From {title}: {content_snippet}")
        
        return "\n\n".join(context_parts)
    
    def _build_character_prompt(self, profile: Dict, context: str, query: str) -> str:
        """Build the prompt for character response generation"""
        
        name = profile.get('name', 'Historical Figure')
        personality = profile.get('personality', {})
        traits = personality.get('traits', [])
        domains = profile.get('knowledge_domains', [])
        historical_context = profile.get('historical_context', {})
        response_style = profile.get('response_style', 'thoughtful historical figure')
        
        prompt = f"""You are {name}, responding as this historical figure would.

CHARACTER PROFILE:
- Personality traits: {', '.join(traits)}
- Areas of expertise: {', '.join(domains)}
- Time period: {historical_context.get('time_period', 'Historical period')}
- Response style: {response_style}

HISTORICAL CONTEXT:
{context}

Please respond to this question as {name} would, drawing upon your historical knowledge, personality, and the context provided. Stay in character and speak from your historical perspective:

QUESTION: {query}

RESPONSE:"""
        
        return prompt