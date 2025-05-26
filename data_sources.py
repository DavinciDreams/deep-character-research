import asyncio
import aiohttp
from typing import Dict, List, Any
import logging
from config import ResearchConfig

class DataSourceManager:
    def __init__(self, config: ResearchConfig):
        self.config = config
        self.session = None
        
    async def get_session(self):
        """Get or create HTTP session"""
        if not self.session or self.session.closed:
            timeout = aiohttp.ClientTimeout(total=30)
            self.session = aiohttp.ClientSession(timeout=timeout)
        return self.session
    
    async def search_source(self, source_name: str, query: str, 
                          max_results: int = 50) -> List[Dict[str, Any]]:
        """Search a specific data source"""
        
        if source_name not in self.data_sources:
            raise ValueError(f"Unknown data source: {source_name}")
        
        source = self.data_sources[source_name]
        
        # Route to appropriate search method
        if source_name == "arxiv":
            return await self._search_arxiv(query, max_results)
        elif source_name == "crossref":
            return await self._search_crossref(query, max_results)
        elif source_name == "semantic_scholar":
            return await self._search_semantic_scholar(query, max_results)
        elif source_name == "openlibrary":
            return await self._search_openlibrary(query, max_results)
        else:
            return []
    
    async def _search_arxiv(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search ArXiv API"""
        session = await self.get_session()
        
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
            'sortBy': 'relevance',
            'sortOrder': 'descending'
        }
        
        try:
            async with session.get(self.data_sources["arxiv"].base_url, params=params) as response:
                if response.status == 200:
                    content = await response.text()
                    return self._parse_arxiv_response(content)
                else:
                    logging.error(f"ArXiv API error: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"ArXiv search error: {e}")
            return []
    
    def _parse_arxiv_response(self, xml_content: str) -> List[Dict[str, Any]]:
        """Parse ArXiv XML response"""
        import xml.etree.ElementTree as ET
        
        try:
            root = ET.fromstring(xml_content)
            results = []
            
            for entry in root.findall('{http://www.w3.org/2005/Atom}entry'):
                title = entry.find('{http://www.w3.org/2005/Atom}title')
                summary = entry.find('{http://www.w3.org/2005/Atom}summary')
                
                authors = []
                for author in entry.findall('{http://www.w3.org/2005/Atom}author'):
                    name = author.find('{http://www.w3.org/2005/Atom}name')
                    if name is not None:
                        authors.append(name.text)
                
                url = entry.find('{http://www.w3.org/2005/Atom}id')
                published = entry.find('{http://www.w3.org/2005/Atom}published')
                
                if title is not None and summary is not None:
                    results.append({
                        'title': title.text.strip(),
                        'abstract': summary.text.strip(),
                        'authors': authors,
                        'url': url.text if url is not None else '',
                        'published': published.text if published is not None else '',
                        'source': 'arxiv',
                        'quality_score': self.data_sources["arxiv"].quality_weight
                    })
            
            return results
            
        except ET.ParseError as e:
            logging.error(f"ArXiv XML parse error: {e}")
            return []
    
    async def _search_crossref(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search CrossRef API"""
        session = await self.get_session()
        
        params = {
            'query': query,
            'rows': max_results,
            'sort': 'relevance',
            'order': 'desc'
        }
        
        try:
            async with session.get(self.data_sources["crossref"].base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_crossref_response(data)
                else:
                    logging.error(f"CrossRef API error: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"CrossRef search error: {e}")
            return []
    
    def _parse_crossref_response(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse CrossRef JSON response"""
        results = []
        
        items = data.get('message', {}).get('items', [])
        
        for item in items:
            title = item.get('title', [''])[0] if item.get('title') else ''
            abstract = item.get('abstract', '')
            
            authors = []
            if 'author' in item:
                for author in item['author']:
                    given = author.get('given', '')
                    family = author.get('family', '')
                    full_name = f"{given} {family}".strip()
                    if full_name:
                        authors.append(full_name)
            
            url = item.get('URL', '')
            published = ''
            if 'published-print' in item:
                date_parts = item['published-print'].get('date-parts', [[]])
                if date_parts and date_parts[0]:
                    published = '-'.join(map(str, date_parts[0]))
            
            if title:
                results.append({
                    'title': title,
                    'abstract': abstract,
                    'authors': authors,
                    'url': url,
                    'published': published,
                    'source': 'crossref',
                    'quality_score': self.data_sources["crossref"].quality_weight
                })
        
        return results
    
    async def _search_semantic_scholar(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Semantic Scholar API"""
        session = await self.get_session()
        
        url = f"{self.data_sources['semantic_scholar'].base_url}/paper/search"
        params = {
            'query': query,
            'limit': max_results,
            'fields': 'title,abstract,authors,url,year,citationCount'
        }
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_semantic_scholar_response(data)
                else:
                    logging.error(f"Semantic Scholar API error: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Semantic Scholar search error: {e}")
            return []
    
    def _parse_semantic_scholar_response(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse Semantic Scholar JSON response"""
        results = []
        
        papers = data.get('data', [])
        
        for paper in papers:
            title = paper.get('title', '')
            abstract = paper.get('abstract', '')
            
            authors = []
            if paper.get('authors'):
                for author in paper['authors']:
                    name = author.get('name', '')
                    if name:
                        authors.append(name)
            
            url = paper.get('url', '')
            year = paper.get('year', '')
            citation_count = paper.get('citationCount', 0)
            
            # Boost quality score based on citations
            base_quality = self.data_sources["semantic_scholar"].quality_weight
            citation_boost = min(0.1, citation_count / 1000)  # Max 0.1 boost
            quality_score = min(1.0, base_quality + citation_boost)
            
            if title:
                results.append({
                    'title': title,
                    'abstract': abstract or '',
                    'authors': authors,
                    'url': url,
                    'published': str(year) if year else '',
                    'source': 'semantic_scholar',
                    'quality_score': quality_score,
                    'citation_count': citation_count
                })
        
        return results
    
    async def _search_openlibrary(self, query: str, max_results: int) -> List[Dict[str, Any]]:
        """Search Open Library API"""
        session = await self.get_session()
        
        url = "https://openlibrary.org/search.json"
        params = {
            'q': query,
            'limit': max_results,
            'fields': 'key,title,author_name,first_publish_year,subject'
        }
        
        try:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return self._parse_openlibrary_response(data)
                else:
                    logging.error(f"Open Library API error: {response.status}")
                    return []
        except Exception as e:
            logging.error(f"Open Library search error: {e}")
            return []
    
    def _parse_openlibrary_response(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse Open Library JSON response"""
        results = []
        
        docs = data.get('docs', [])
        
        for doc in docs:
            title = doc.get('title', '')
            authors = doc.get('author_name', [])
            year = doc.get('first_publish_year', '')
            subjects = doc.get('subject', [])
            key = doc.get('key', '')
            
            url = f"https://openlibrary.org{key}" if key else ''
            
            # Create abstract from subjects
            abstract = f"Book covering topics: {', '.join(subjects[:5])}" if subjects else ''
            
            if title:
                results.append({
                    'title': title,
                    'abstract': abstract,
                    'authors': authors,
                    'url': url,
                    'published': str(year) if year else '',
                    'source': 'openlibrary',
                    'quality_score': self.data_sources["openlibrary"].quality_weight
                })
        
        return results
    
    async def search_all_sources(self, query: str, max_results_per_source: int = 20) -> List[Dict[str, Any]]:
        """Search all available data sources"""
        all_results = []
        
        for source_name in self.data_sources:
            try:
                results = await self.search_source(source_name, query, max_results_per_source)
                all_results.extend(results)
                
                # Rate limiting
                await asyncio.sleep(self.data_sources[source_name].rate_limit)
                
            except Exception as e:
                logging.error(f"Error searching {source_name}: {e}")
                continue
        
        # Sort by quality score
        all_results.sort(key=lambda x: x.get('quality_score', 0), reverse=True)
        
        return all_results
    
    async def close(self):
        """Close HTTP session"""
        if self.session and not self.session.closed:
            try:
                await self.session.close()
            except Exception as e:
                logging.warning(f"Error closing data sources session: {e}")
            finally:
                self.session = None