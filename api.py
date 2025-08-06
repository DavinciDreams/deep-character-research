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
@app.get("/")
async def root():
    return {"message": "Character Researcher API root. See /api/research, /api/chat, /api/characters."}

# Allow CORS for local frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://deep-character-research.vercel.app"
    ],
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
    type: Optional[str] = Query(None, description="Filter by document source_type")
):
    """
    Returns a list of researched characters, optionally filtered by start_time, end_time, and type.
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
        return {"characters": characters}
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