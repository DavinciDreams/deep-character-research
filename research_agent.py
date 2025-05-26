import aiohttp
import asyncio
from typing import List, Dict, Optional
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import re
from dataclasses import dataclass

@dataclass
class ResearchResult:
    title: str
    authors: List[str]
    abstract: str
    url: str
    source_type: str
    quality_score: float
    publication_date: Optional[str]
    citations: int
    language: Optional[str] = None

class DeepResearchAgent:
    def __init__(self, data_sources):
        self.data_sources = data_sources
        self.session = None
        
        # Language mappings for historical figures
        self.character_languages = {
            # Italian figures
            "leonardo da vinci": ["it", "en"],
            "leonardo": ["it", "en"],
            "da vinci": ["it", "en"],
            "davinci": ["it", "en"],
            "michelangelo": ["it", "en"],
            "galileo": ["it", "en"],
            "dante": ["it", "en"],
            "machiavelli": ["it", "en"],
            
            # Roman/Latin figures
            "julius caesar": ["la", "it", "en"],
            "caesar": ["la", "it", "en"],
            "cicero": ["la", "it", "en"],
            "augustus": ["la", "it", "en"],
            "marcus aurelius": ["la", "en"],
            "virgil": ["la", "it", "en"],
            
            # French figures
            "napoleon": ["fr", "en"],
            "voltaire": ["fr", "en"],
            "descartes": ["fr", "en"],
            "rousseau": ["fr", "en"],
            "marie curie": ["fr", "pl", "en"],
            
            # German figures
            "einstein": ["de", "en"],
            "beethoven": ["de", "en"],
            "goethe": ["de", "en"],
            "kant": ["de", "en"],
            "marx": ["de", "en"],
            
            # Spanish figures
            "cervantes": ["es", "en"],
            "picasso": ["es", "en"],
            "goya": ["es", "en"],
            
            # Greek figures
            "plato": ["el", "en"],
            "aristotle": ["el", "en"],
            "socrates": ["el", "en"],
            "homer": ["el", "en"],
            
            # Russian figures
            "tolstoy": ["ru", "en"],
            "dostoevsky": ["ru", "en"],
            "tchaikovsky": ["ru", "en"],
            "putin": ["ru", "en"],
            
            # Chinese figures
            "confucius": ["zh", "en"],
            "sun tzu": ["zh", "en"],
            "lao tzu": ["zh", "en"],
            
            # Japanese figures
            "hirohito": ["ja", "en"],
            "akira kurosawa": ["ja", "en"],
        }
        
    async def get_session(self):
        """Get or create aiohttp session"""
        if not self.session:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=30),
                headers={'User-Agent': 'DeepCharacterResearch/1.0 (Educational Research Tool)'}
            )
        return self.session
        
    def _get_character_languages(self, query: str) -> List[str]:
        """Get relevant languages for a character"""
        query_lower = query.lower()
        
        # Check exact matches first
        for key, langs in self.character_languages.items():
            if key in query_lower:
                return langs
                
        # Check partial matches
        for key, langs in self.character_languages.items():
            if any(part in query_lower for part in key.split() if len(part) > 3):
                return langs
                
        # Default to English
        return ["en"]
        
    async def search_academic_sources(self, query: str) -> List[ResearchResult]:
        """Search high-quality academic sources"""
        results = []
        
        try:
            # ArXiv search
            arxiv_results = await self._search_arxiv(query)
            results.extend(arxiv_results)
            
            # Wikipedia search (multilingual)
            wikipedia_results = await self._search_wikipedia_multilingual(query)
            results.extend(wikipedia_results)
            
            # Wikidata search
            wikidata_results = await self._search_wikidata(query)
            results.extend(wikidata_results)
            
        except Exception as e:
            print(f"Error in academic search: {e}")
        
        # Sort by quality score
        return sorted(results, key=lambda x: x.quality_score, reverse=True)
    
    async def _search_wikipedia_multilingual(self, query: str) -> List[ResearchResult]:
        """Search Wikipedia in multiple languages"""
        all_results = []
        languages = self._get_character_languages(query)
        
        print(f"Searching Wikipedia in languages: {languages} for '{query}'")
        
        for lang in languages:
            try:
                results = await self._search_wikipedia_single_language(query, lang)
                all_results.extend(results)
                
                # Add delay between language searches to be respectful
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"Error searching Wikipedia in {lang}: {e}")
                continue
                
        return all_results
    
    async def _search_wikipedia_single_language(self, query: str, lang: str) -> List[ResearchResult]:
        """Search Wikipedia in a specific language"""
        session = await self.get_session()
        
        # First, search for pages
        search_url = f"https://{lang}.wikipedia.org/w/api.php"
        search_params = {
            'action': 'query',
            'format': 'json',
            'list': 'search',
            'srsearch': query,
            'srlimit': '10',  # String instead of int
            'srprop': 'snippet'
        }
        
        try:
            async with session.get(search_url, params=search_params) as response:
                if response.status != 200:
                    return []
                    
                data = await response.json()
                search_results = data.get('query', {}).get('search', [])
                
                # Get full content for top results
                results = []
                for search_result in search_results[:3]:  # Limit to top 3 per language
                    page_title = search_result['title']
                    
                    # Get page content
                    content_params = {
                        'action': 'query',
                        'format': 'json',
                        'titles': page_title,
                        'prop': 'extracts|info',
                        'exintro': '1',  # String instead of True
                        'explaintext': '1',  # String instead of True
                        'exsectionformat': 'plain',
                        'inprop': 'url'
                    }
                    
                    async with session.get(search_url, params=content_params) as content_response:
                        if content_response.status == 200:
                            content_data = await content_response.json()
                            pages = content_data.get('query', {}).get('pages', {})
                            
                            for page_id, page_info in pages.items():
                                if page_id == '-1':  # Page not found
                                    continue
                                    
                                title = page_info.get('title', '')
                                extract = page_info.get('extract', '')
                                url = page_info.get('fullurl', '')
                                
                                if extract and len(extract) > 100:
                                    quality_score = self._calculate_quality_score(
                                        title, extract, [], "wikipedia", lang
                                    )
                                    
                                    results.append(ResearchResult(
                                        title=f"{title} ({lang.upper()} Wikipedia)",
                                        authors=["Wikipedia Contributors"],
                                        abstract=extract[:500] + "..." if len(extract) > 500 else extract,
                                        url=url,
                                        source_type="wikipedia",
                                        quality_score=quality_score,
                                        publication_date="",
                                        citations=0,
                                        language=lang
                                    ))
                    
                    # Add delay between page requests
                    await asyncio.sleep(0.5)
                
                return results
                
        except Exception as e:
            print(f"Wikipedia search error for {lang}: {e}")
            return []
    
    async def _search_wikidata(self, query: str) -> List[ResearchResult]:
        """Search Wikidata for structured information"""
        session = await self.get_session()
        
        # Wikidata search API
        search_url = "https://www.wikidata.org/w/api.php"
        search_params = {
            'action': 'wbsearchentities',
            'format': 'json',
            'language': 'en',
            'search': query,
            'type': 'item',
            'limit': '5'  # String instead of int
        }
        
        try:
            async with session.get(search_url, params=search_params) as response:
                if response.status != 200:
                    return []
                    
                data = await response.json()
                entities = data.get('search', [])
                
                results = []
                for entity in entities:
                    entity_id = entity.get('id', '')
                    title = entity.get('label', '')
                    description = entity.get('description', '')
                    url = f"https://www.wikidata.org/wiki/{entity_id}"
                    
                    if title and description:
                        # Get additional data about the entity
                        entity_data = await self._get_wikidata_entity_details(entity_id)
                        
                        quality_score = self._calculate_quality_score(
                            title, description, [], "wikidata"
                        )
                        
                        results.append(ResearchResult(
                            title=f"{title} (Wikidata)",
                            authors=["Wikidata Contributors"],
                            abstract=description + (f"\n\nAdditional info: {entity_data}" if entity_data else ""),
                            url=url,
                            source_type="wikidata",
                            quality_score=quality_score,
                            publication_date="",
                            citations=0,
                            language="en"
                        ))
                
                return results
                
        except Exception as e:
            print(f"Wikidata search error: {e}")
            return []
    
    async def _get_wikidata_entity_details(self, entity_id: str) -> str:
        """Get additional details about a Wikidata entity"""
        session = await self.get_session()
        
        url = "https://www.wikidata.org/w/api.php"
        params = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': entity_id,
            'languages': 'en',
            'props': 'claims'
        }
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    entity = data.get('entities', {}).get(entity_id, {})
                    claims = entity.get('claims', {})
                    
                    # Extract key information
                    details = []
                    
                    # Birth date (P569)
                    if 'P569' in claims:
                        birth_date = self._extract_wikidata_date(claims['P569'])
                        if birth_date:
                            details.append(f"Born: {birth_date}")
                    
                    # Death date (P570)
                    if 'P570' in claims:
                        death_date = self._extract_wikidata_date(claims['P570'])
                        if death_date:
                            details.append(f"Died: {death_date}")
                    
                    return "; ".join(details)
                    
        except Exception as e:
            print(f"Error getting Wikidata entity details: {e}")
            
        return ""
    
    def _extract_wikidata_date(self, claims: List[Dict]) -> Optional[str]:
        """Extract date from Wikidata claims"""
        try:
            if claims and len(claims) > 0:
                claim = claims[0]
                datavalue = claim.get('mainsnak', {}).get('datavalue', {})
                if datavalue.get('type') == 'time':
                    time_value = datavalue.get('value', {}).get('time', '')
                    # Extract year from timestamp like "+1452-04-15T00:00:00Z"
                    match = re.match(r'\+(\d{4})-(\d{2})-(\d{2})', time_value)
                    if match:
                        year, month, day = match.groups()
                        return f"{year}-{month}-{day}"
        except:
            pass
        return None
    
    async def _search_arxiv(self, query: str) -> List[ResearchResult]:
        """Search ArXiv for relevant papers"""
        session = await self.get_session()
        base_url = "http://export.arxiv.org/api/query"
        params = {
            'search_query': f'all:{query}',
            'start': '0',  # String instead of int
            'max_results': '5',  # Reduced and string
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            async with session.get(base_url, params=params) as response:
                if response.status == 200:
                    content = await response.text()
                    return self._parse_arxiv_response(content)
                else:
                    print(f"ArXiv API error: {response.status}")
                    return []
        except Exception as e:
            print(f"ArXiv search error: {e}")
            return []
    
    def _parse_arxiv_response(self, content: str) -> List[ResearchResult]:
        """Parse ArXiv XML response"""
        try:
            root = ET.fromstring(content)
            results = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title_elem = entry.find('{http://www.w3.org/2005/Atom}title')
                summary_elem = entry.find('{http://www.w3.org/2005/Atom}summary')
                
                if title_elem is None or summary_elem is None:
                    continue
                
                title = title_elem.text.strip()
                summary = summary_elem.text.strip()
                
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name_elem = author.find('{http://www.w3.org/2005/Atom}name')
                    if name_elem is not None:
                        authors.append(name_elem.text)
                
                url_elem = entry.find('{http://www.w3.org/2005/Atom}id')
                published_elem = entry.find('{http://www.w3.org/2005/Atom}published')
                
                url = url_elem.text if url_elem is not None else ''
                published = published_elem.text if published_elem is not None else ''
                
                quality_score = self._calculate_quality_score(title, summary, authors, "arxiv")
                
                results.append(ResearchResult(
                    title=title,
                    authors=authors,
                    abstract=summary,
                    url=url,
                    source_type="arxiv",
                    quality_score=quality_score,
                    publication_date=published,
                    citations=0,
                    language="en"
                ))
            
            return results
            
        except ET.ParseError as e:
            print(f"ArXiv XML parse error: {e}")
            return []
    
    def _calculate_quality_score(self, title: str, abstract: str, authors: List[str], 
                               source: str, language: str = "en") -> float:
        """Calculate quality score for research result"""
        score = 0.0
        
        # Base score by source
        source_scores = {
            "arxiv": 0.8,
            "wikipedia": 0.7,
            "wikidata": 0.75,
            "academia": 0.6
        }
        score += source_scores.get(source, 0.5)
        
        # Language bonus (native language sources often have more detail)
        if language != "en":
            score += 0.05  # Slight bonus for non-English sources
            
        # Title relevance
        if len(title) > 10 and any(keyword in title.lower() for keyword in 
                                 ["historical", "analysis", "study", "biography"]):
            score += 0.1
            
        # Abstract quality
        if len(abstract) > 100:
            score += 0.05
            
        # Multiple authors (indicates peer review for academic sources)
        if len(authors) > 1 and source == "arxiv":
            score += 0.05
            
        return min(score, 1.0)
    
    async def search_primary_sources(self, domain: str) -> List[ResearchResult]:
        """Search for primary historical sources"""
        return []
    
    async def search_contemporary_sources(self, domain: str) -> List[ResearchResult]:
        """Search for contemporary accounts and sources"""
        return []
    
    async def cross_validate_sources(self, source_groups: List[List[ResearchResult]]) -> List[ResearchResult]:
        """Cross-validate information across multiple sources"""
        all_results = []
        for group in source_groups:
            all_results.extend(group)
        
        # Remove duplicates and rank by quality and language diversity
        unique_results = []
        seen_titles = set()
        
        for result in all_results:
            title_lower = result.title.lower()
            # More sophisticated duplicate detection
            is_duplicate = False
            for seen_title in seen_titles:
                if self._titles_similar(title_lower, seen_title):
                    is_duplicate = True
                    break
                    
            if not is_duplicate:
                seen_titles.add(title_lower)
                unique_results.append(result)
        
        return unique_results
    
    def _titles_similar(self, title1: str, title2: str) -> bool:
        """Check if two titles are similar (basic implementation)"""
        # Remove common words and check overlap
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        words1 = set(title1.split()) - common_words
        words2 = set(title2.split()) - common_words
        
        if not words1 or not words2:
            return False
            
        overlap = len(words1.intersection(words2))
        min_length = min(len(words1), len(words2))
        
        return overlap / min_length > 0.6  # 60% word overlap threshold
    
    async def close(self):
        """Close the HTTP session"""
        if self.session:
            await self.session.close()
            self.session = None