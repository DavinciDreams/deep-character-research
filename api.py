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
    start_time: Optional[str] = Query(None, description="Filter by created_at >= start_time (ISO 8601)"),
    end_time: Optional[str] = Query(None, description="Filter by created_at <= end_time (ISO 8601)"),
    type: Optional[str] = Query(None, description="Filter by document source_type"),
    profession: Optional[str] = Query(None, description="Filter by profession (matches known_roles)")
):
    """
    Returns a list of researched characters, optionally filtered by start_time, end_time, type, and profession.

    Each character object includes:
    - id: Character ID
    - name: Character name
    - created_at: Creation timestamp
    - known_roles: List of professions/roles (aggregated from document metadata)
    - contemporaries: List of contemporary character names (if available)
    """
    try:
        config = get_config_from_env()
        db_path = getattr(config, "db_path", "data/characters.sqlite")
        store = DocumentStore(db_path)
        characters = store.get_characters(
            start_time=start_time,
            end_time=end_time,
            doc_type=type
        )

        enriched_characters = []
        # Build a mapping of character id to name for contemporaries lookup
        id_to_name = {c["id"]: c["name"] for c in characters}

        for char in characters:
            name = char["name"]
            # Fetch all documents for this character
            docs = store.get_character_documents(name)
            # Aggregate known_roles and contemporaries from metadata
            known_roles = set()
            contemporaries = set()
            for doc in docs:
                meta = doc.get("metadata", {})
                # Extract known_roles from metadata if present
                roles = meta.get("known_roles") or meta.get("roles") or []
                if isinstance(roles, str):
                    # Handle comma-separated string
                    roles = [r.strip() for r in roles.split(",") if r.strip()]
                known_roles.update(roles)
                # Extract contemporaries from metadata if present
                cont = meta.get("contemporaries") or []
                if isinstance(cont, str):
                    cont = [c.strip() for c in cont.split(",") if c.strip()]
                contemporaries.update(cont)
            # Optionally, filter out empty strings
            known_roles = [r for r in known_roles if r]
            contemporaries = [c for c in contemporaries if c and c != name]

            # If profession filter is set, skip if not present in known_roles
            if profession:
                if not any(profession.lower() in r.lower() for r in known_roles):
                    continue

            enriched_characters.append({
                "id": char["id"],
                "name": name,
                "created_at": char["created_at"],
                "known_roles": known_roles,
                "contemporaries": contemporaries
            })

        return {"characters": enriched_characters}
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