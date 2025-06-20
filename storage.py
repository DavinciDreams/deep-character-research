import sqlite3
import json
import chromadb
from typing import List, Dict, Any, Optional
import logging
from pathlib import Path
from sentence_transformers import SentenceTransformer

class DocumentStore:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS characters (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_id INTEGER,
                    title TEXT,
                    content TEXT,
                    url TEXT,
                    source_type TEXT,
                    quality_score REAL,
                    metadata TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (character_id) REFERENCES characters (id)
                )
            ''')
            
            conn.commit()
    
    def add_character(self, name: str) -> int:
        """Add a character and return their ID"""
        with sqlite3.connect(self.db_path) as conn:
            try:
                cursor = conn.execute(
                    'INSERT INTO characters (name) VALUES (?)', 
                    (name,)
                )
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                # Character already exists
                cursor = conn.execute(
                    'SELECT id FROM characters WHERE name = ?', 
                    (name,)
                )
                return cursor.fetchone()[0]
    
    def add_document(self, character_id: int, document: Dict[str, Any]) -> int:
        """Add a document for a character"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute('''
                INSERT INTO documents 
                (character_id, title, content, url, source_type, quality_score, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                character_id,
                document.get('title', ''),
                document.get('content', ''),
                document.get('url', ''),
                document.get('source_type', ''),
                document.get('quality_score', 0.0),
                json.dumps(document.get('metadata', {}))
            ))
            return cursor.lastrowid
    
    def get_character_documents(self, character_name: str) -> List[Dict[str, Any]]:
        """Get all documents for a character"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('''
                SELECT d.* FROM documents d
                JOIN characters c ON d.character_id = c.id
                WHERE c.name = ?
                ORDER BY d.quality_score DESC
            ''', (character_name,))
            
            documents = []
            for row in cursor.fetchall():
                doc = dict(row)
                doc['metadata'] = json.loads(doc['metadata']) if doc['metadata'] else {}
                documents.append(doc)
            
            return documents

class VectorDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        
        try:
            self.client = chromadb.PersistentClient(path=db_path)
            self.collections = {}
        except Exception as e:
            logging.error(f"Error initializing ChromaDB: {e}")
            self.client = None
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def _get_collection(self, character_name: str):
        """Get or create collection for character"""
        if not self.client:
            return None
            
        collection_name = f"character_{character_name.lower().replace(' ', '_')}"
        
        if collection_name not in self.collections:
            try:
                self.collections[collection_name] = self.client.get_or_create_collection(
                    name=collection_name
                )
            except Exception as e:
                logging.error(f"Error creating collection for {character_name}: {e}")
                return None
        
        return self.collections.get(collection_name)
    
    def add_documents(self, character_name: str, documents: List[Dict[str, Any]]):
        """Add documents to vector database"""
        collection = self._get_collection(character_name)
        if not collection:
            return
        
        try:
            texts = []
            metadatas = []
            ids = []
            
            for i, doc in enumerate(documents):
                # Combine title and content for embedding
                text = f"{doc.get('title', '')} {doc.get('content', doc.get('abstract', ''))}"
                texts.append(text)
                
                # Prepare metadata
                metadata = {
                    'title': doc.get('title', ''),
                    'source_type': doc.get('source_type', ''),
                    'url': doc.get('url', ''),
                    'quality_score': doc.get('quality_score', 0.0)
                }
                metadatas.append(metadata)
                
                # Create unique ID
                ids.append(f"{character_name}_{i}_{hash(text) % 10000}")
            
            # Add to collection
            collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logging.info(f"Added {len(documents)} documents to vector DB for {character_name}")
            
        except Exception as e:
            logging.error(f"Error adding documents to vector DB: {e}")
    
    def search_similar(self, character_name: str, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for similar documents"""
        collection = self._get_collection(character_name)
        if not collection:
            return []
        
        try:
            results = collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            # Format results
            documents = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'][0] else {}
                    documents.append({
                        'content': doc,
                        'title': metadata.get('title', ''),
                        'source_type': metadata.get('source_type', ''),
                        'url': metadata.get('url', ''),
                        'quality_score': metadata.get('quality_score', 0.0)
                    })
            
            return documents
            
        except Exception as e:
            logging.error(f"Error searching vector DB: {e}")
            return []