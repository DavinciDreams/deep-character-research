from dotenv import load_dotenv
load_dotenv()
import os
import uuid
import logging
import asyncio
from fastapi import FastAPI, HTTPException, Request, Query
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deep_character_researcher import DeepCharacterResearcher
from config import ResearchConfig
from typing import Dict, Any, Optional, List
from storage import DocumentStore

app = FastAPI()

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for task status and results
task_store: Dict[str, Dict[str, Any]] = {}

class ResearchRequest(BaseModel):
    character: str
    query: str

class ResearchResponse(BaseModel):
    task_id: str
    status: str

def get_config_from_env():
    # Example: override config with env vars if present
    # Extend as needed for more config options
    return ResearchConfig(
        # Example: os.getenv("VECTOR_DB_PATH", default)
        # Add more as needed
    )

# Minimal wrapper to call research_character asynchronously
async def perform_research(task_id: str, character: str, query: str):
    config = get_config_from_env()
    researcher = DeepCharacterResearcher(config)
    try:
        # Mark as running
        task_store[task_id]["status"] = "running"
        # Simulate research and store result (replace with actual result as needed)
        await researcher.research_character(character_name=character)
        # For demonstration, store a dummy result
        result = {"message": f"Research completed for {character}"}
        task_store[task_id]["status"] = "completed"
        task_store[task_id]["result"] = result
    except Exception as e:
        logging.error(f"Research failed: {e}")
        task_store[task_id]["status"] = "failed"
        task_store[task_id]["result"] = {"error": str(e)}

@app.post("/api/research", response_model=ResearchResponse)
async def research_endpoint(request: ResearchRequest):
    task_id = str(uuid.uuid4())
    try:
        # Register task as started
        task_store[task_id] = {"status": "started", "result": None}
        # Launch research as a background task
        asyncio.create_task(perform_research(task_id, request.character, request.query))
        return ResearchResponse(task_id=task_id, status="started")
    except Exception as e:
        logging.error(f"API error: {e}")
        raise HTTPException(status_code=500, detail="Research initiation failed")

@app.get("/api/research/{task_id}/status")
async def get_research_status(task_id: str):
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task["status"]}

@app.get("/api/research/{task_id}/result")
async def get_research_result(task_id: str):
    task = task_store.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task["status"] == "completed":
        return {"task_id": task_id, "result": task["result"]}
    elif task["status"] == "failed":
        return JSONResponse(status_code=500, content={"task_id": task_id, "error": task["result"]})
    else:
        raise HTTPException(status_code=202, detail="Task not completed yet")

@app.get("/api/characters")
async def get_characters(
    name: Optional[str] = Query(None, description="Search by name (partial, case-insensitive)"),
    field: Optional[str] = Query(None, description="Filter by profession/role"),
    era: Optional[str] = Query(None, description="Filter by era (period or years)"),
    keywords: Optional[str] = Query(None, description="Search in description/metadata (comma/space separated)")
):
    """
    Search historical figures by name, field, era, and description keywords.
    Returns: id, name, years, era, shortDescription, portraitUrl, contemporaries
    """
    try:
        config = get_config_from_env()
        db_path = getattr(config, "db_path", "data/characters.sqlite")
        store = DocumentStore(db_path)
        characters = store.get_characters()

        # Prepare keyword list
        keyword_list = []
        if keywords:
            # Split by comma or whitespace
            keyword_list = [k.strip().lower() for k in keywords.replace(",", " ").split() if k.strip()]

        results = []
        for char in characters:
            char_name = char.get("name", "")
            char_id = char.get("id")
            docs = store.get_character_documents(char_name)

            # Aggregate metadata
            years = None
            era_val = None
            short_desc = None
            portrait_url = None
            contemporaries = set()
            known_roles = set()
            descriptions = []

            for doc in docs:
                meta = doc.get("metadata", {})
                # Years
                y = meta.get("years") or meta.get("life_years")
                if y and not years:
                    years = y
                # Era
                e = meta.get("era") or meta.get("period")
                if e and not era_val:
                    era_val = e
                # Description
                desc = meta.get("shortDescription") or meta.get("description")
                if desc:
                    descriptions.append(desc)
                    if not short_desc:
                        short_desc = desc
                # Portrait
                purl = meta.get("portraitUrl") or meta.get("portrait_url")
                if purl and not portrait_url:
                    portrait_url = purl
                # Roles
                roles = meta.get("known_roles") or meta.get("roles") or []
                if isinstance(roles, str):
                    roles = [r.strip() for r in roles.split(",") if r.strip()]
                known_roles.update(roles)
                # Contemporaries
                cont = meta.get("contemporaries") or []
                if isinstance(cont, str):
                    cont = [c.strip() for c in cont.split(",") if c.strip()]
                contemporaries.update(cont)

            # Filtering
            # Name filter
            if name and name.lower() not in char_name.lower():
                continue
            # Field/profession filter
            if field:
                if not any(field.lower() in r.lower() for r in known_roles):
                    continue
            # Era filter
            if era:
                era_str = (str(era_val) or "").lower()
                if era.lower() not in era_str:
                    continue
            # Keywords filter (search in all descriptions and metadata as string)
            if keyword_list:
                meta_text = " ".join(descriptions + [str(meta) for doc in docs for meta in [doc.get("metadata", {})]])
                meta_text = meta_text.lower()
                if not all(k in meta_text for k in keyword_list):
                    continue

            results.append({
                "id": char_id,
                "name": char_name,
                "years": years,
                "era": era_val,
                "shortDescription": short_desc,
                "portraitUrl": portrait_url,
                "contemporaries": list(contemporaries)
            })

        return {"characters": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch characters: {e}")

# --- Chat API ---

class ChatRequest(BaseModel):
    character: str
    message: str

class ChatResponse(BaseModel):
    response: str

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        config = get_config_from_env()
        researcher = DeepCharacterResearcher(config)
        response = await researcher.chat_with_character(request.character, request.message)
        if response and hasattr(response, "content"):
            return ChatResponse(response=response.content)
        else:
            return ChatResponse(response="No response generated.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {e}")
# --- CRUD API Endpoints for Characters, Documents, Chat History, User Searches ---

from fastapi import Path

# --- Pydantic Models ---

class CharacterCreate(BaseModel):
    name: str

class CharacterUpdate(BaseModel):
    name: str

class CharacterOut(BaseModel):
    id: int
    name: str

class DocumentCreate(BaseModel):
    character_id: int
    title: str
    content: str
    url: str = ""
    source_type: str = ""
    quality_score: float = 0.0
    metadata: dict = {}

class DocumentUpdate(BaseModel):
    title: str = ""
    content: str = ""
    url: str = ""
    source_type: str = ""
    quality_score: float = 0.0
    metadata: dict = {}

class DocumentOut(BaseModel):
    id: int
    character_id: int
    title: str
    content: str
    url: str
    source_type: str
    quality_score: float
    metadata: dict

class ChatHistoryCreate(BaseModel):
    character_id: int
    user_message: str
    character_response: str

class ChatHistoryOut(BaseModel):
    id: int
    character_id: int
    user_message: str
    character_response: str
    timestamp: str

class UserSearchCreate(BaseModel):
    user_query: str
    character_id: int
    results_count: int

class UserSearchOut(BaseModel):
    id: int
    user_query: str
    character_id: int
    search_time: str
    results_count: int

# --- Helper to get DocumentStore instance ---
def get_store():
    config = get_config_from_env()
    db_path = getattr(config, "db_path", "data/characters.sqlite")
    return DocumentStore(db_path)

# --- Characters CRUD ---

@app.post("/api/characters", response_model=CharacterOut)
async def create_character(request: CharacterCreate):
    store = get_store()
    char_id = store.add_character(request.name)
    return CharacterOut(id=char_id, name=request.name)

@app.get("/api/characters/{character_id}", response_model=CharacterOut)
async def get_character(character_id: int = Path(...)):
    store = get_store()
    chars = store.get_characters()
    for c in chars:
        if c["id"] == character_id:
            return CharacterOut(id=c["id"], name=c["name"])
    raise HTTPException(status_code=404, detail="Character not found")

@app.put("/api/characters/{character_id}", response_model=CharacterOut)
async def update_character(character_id: int, request: CharacterUpdate):
    store = get_store()
    # Only name can be updated
    with store:
        with sqlite3.connect(store.db_path) as conn:
            conn.execute("UPDATE characters SET name = ? WHERE id = ?", (request.name, character_id))
            conn.commit()
    return CharacterOut(id=character_id, name=request.name)

@app.delete("/api/characters/{character_id}")
async def delete_character(character_id: int):
    store = get_store()
    with store:
        with sqlite3.connect(store.db_path) as conn:
            conn.execute("DELETE FROM characters WHERE id = ?", (character_id,))
            conn.commit()
    return {"detail": "Character deleted"}

# --- Documents CRUD ---

@app.post("/api/documents", response_model=DocumentOut)
async def create_document(request: DocumentCreate):
    store = get_store()
    doc_id = store.add_document(request.character_id, request.dict())
    return DocumentOut(id=doc_id, **request.dict())

@app.get("/api/documents/{document_id}", response_model=DocumentOut)
async def get_document(document_id: int = Path(...)):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM documents WHERE id = ?", (document_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Document not found")
        doc = dict(row)
        doc["metadata"] = json.loads(doc["metadata"]) if doc["metadata"] else {}
        return DocumentOut(**doc)

@app.put("/api/documents/{document_id}", response_model=DocumentOut)
async def update_document(document_id: int, request: DocumentUpdate):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.execute(
            "UPDATE documents SET title=?, content=?, url=?, source_type=?, quality_score=?, metadata=? WHERE id=?",
            (
                request.title,
                request.content,
                request.url,
                request.source_type,
                request.quality_score,
                json.dumps(request.metadata),
                document_id,
            ),
        )
        conn.commit()
    return await get_document(document_id)

@app.delete("/api/documents/{document_id}")
async def delete_document(document_id: int):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.execute("DELETE FROM documents WHERE id = ?", (document_id,))
        conn.commit()
    return {"detail": "Document deleted"}

# --- Chat History CRUD ---

@app.post("/api/chat_history", response_model=ChatHistoryOut)
async def create_chat_history(request: ChatHistoryCreate):
    store = get_store()
    chat_id = store.add_chat_history(request.character_id, request.user_message, request.character_response)
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM chat_history WHERE id = ?", (chat_id,))
        row = cur.fetchone()
        return ChatHistoryOut(**dict(row))

@app.get("/api/chat_history/{chat_id}", response_model=ChatHistoryOut)
async def get_chat_history(chat_id: int = Path(...)):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM chat_history WHERE id = ?", (chat_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="Chat history not found")
        return ChatHistoryOut(**dict(row))

@app.delete("/api/chat_history/{chat_id}")
async def delete_chat_history(chat_id: int):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.execute("DELETE FROM chat_history WHERE id = ?", (chat_id,))
        conn.commit()
    return {"detail": "Chat history deleted"}

# --- User Searches CRUD ---

@app.post("/api/user_searches", response_model=UserSearchOut)
async def create_user_search(request: UserSearchCreate):
    store = get_store()
    search_id = store.add_user_search(request.user_query, request.character_id, request.results_count)
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM user_searches WHERE id = ?", (search_id,))
        row = cur.fetchone()
        return UserSearchOut(**dict(row))

@app.get("/api/user_searches/{search_id}", response_model=UserSearchOut)
async def get_user_search(search_id: int = Path(...)):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("SELECT * FROM user_searches WHERE id = ?", (search_id,))
        row = cur.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User search not found")
        return UserSearchOut(**dict(row))

@app.delete("/api/user_searches/{search_id}")
async def delete_user_search(search_id: int):
    store = get_store()
    with sqlite3.connect(store.db_path) as conn:
        conn.execute("DELETE FROM user_searches WHERE id = ?", (search_id,))
        conn.commit()
    return {"detail": "User search deleted"}