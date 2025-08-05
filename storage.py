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

    def get_characters(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        doc_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Fetch characters with optional filtering by created_at and document type.
        - start_time, end_time: ISO 8601 strings for created_at filtering.
        - doc_type: filters characters that have at least one document with source_type == doc_type.
        """
        query = """
            SELECT DISTINCT c.id, c.name, c.created_at
            FROM characters c
            {join_clause}
            WHERE 1=1
            {time_clause}
            {type_clause}
            ORDER BY c.created_at DESC
        """
        join_clause = ""
        time_clause = ""
        type_clause = ""
        params = []

        if doc_type:
            join_clause = "LEFT JOIN documents d ON d.character_id = c.id"
            type_clause = " AND d.source_type = ?"
            params.append(doc_type)

        if start_time:
            time_clause += " AND c.created_at >= ?"
            params.append(start_time)
        if end_time:
            time_clause += " AND c.created_at <= ?"
            params.append(end_time)

        final_query = query.format(
            join_clause=join_clause,
            time_clause=time_clause,
            type_clause=type_clause
        )

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(final_query, params)
            return [dict(row) for row in cursor.fetchall()]
    
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
            
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    character_id INTEGER,
                    user_message TEXT NOT NULL,
                    character_response TEXT NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (character_id) REFERENCES characters (id)
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS user_searches (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_query TEXT NOT NULL,
                    character_id INTEGER,
                    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    results_count INTEGER,
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

    def add_chat_history(self, character_id: int, user_message: str, character_response: str) -> int:
        """Add a chat history record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                '''INSERT INTO chat_history (character_id, user_message, character_response)
                   VALUES (?, ?, ?)''',
                (character_id, user_message, character_response)
            )
            return cursor.lastrowid

    def get_chat_history(self, character_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent chat history for a character"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                '''SELECT * FROM chat_history
                   WHERE character_id = ?
                   ORDER BY timestamp DESC
                   LIMIT ?''',
                (character_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]

    def add_user_search(self, user_query: str, character_id: int, results_count: int) -> int:
        """Add a user search record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                '''INSERT INTO user_searches (user_query, character_id, results_count)
                   VALUES (?, ?, ?)''',
                (user_query, character_id, results_count)
            )
            return cursor.lastrowid

    def get_user_searches(self, character_id: int, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent user searches for a character"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                '''SELECT * FROM user_searches
                   WHERE character_id = ?
                   ORDER BY search_time DESC
                   LIMIT ?''',
                (character_id, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
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