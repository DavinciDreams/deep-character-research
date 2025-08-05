from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from main import DeepCharacterResearcher
from config import ResearchConfig

app = FastAPI()

# CORS: Allow all origins for now (development only).
# For production, restrict allow_origins to trusted domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ResearchCharacterRequest(BaseModel):
    character_name: str
    research_depth: Optional[str] = "comprehensive"
    ai_provider: Optional[str] = None

from fastapi import HTTPException

@app.post("/research_character")
async def research_character_endpoint(request: ResearchCharacterRequest):
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    try:
        result = await researcher.research_character(
            character_name=request.character_name,
            research_depth=request.research_depth,
            ai_provider=request.ai_provider
        )
        return result.__dict__
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if hasattr(researcher, "cleanup"):
            await researcher.cleanup()
class ChatWithCharacterRequest(BaseModel):
    character_name: str
    message: str
    ai_provider: Optional[str] = None
    model: Optional[str] = None

@app.post("/chat_with_character")
async def chat_with_character_endpoint(request: ChatWithCharacterRequest):
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    try:
        response = await researcher.chat_with_character(
            character_name=request.character_name,
            message=request.message,
            ai_provider=request.ai_provider,
            model=request.model
        )
        # Try to return as dict if possible, else fallback to str
        if hasattr(response, "dict"):
            return response.dict()
        elif hasattr(response, "__dict__"):
            return response.__dict__
        else:
            return {"result": str(response)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if hasattr(researcher, "cleanup"):
            await researcher.cleanup()
class CompareAIResponsesRequest(BaseModel):
    character_name: str
    message: str

@app.post("/compare_ai_responses")
async def compare_ai_responses_endpoint(request: CompareAIResponsesRequest):
    config = ResearchConfig()
    researcher = DeepCharacterResearcher(config)
    try:
        result = await researcher.compare_ai_responses(
            character_name=request.character_name,
            message=request.message
        )
        # Convert response objects to dict if possible
        result_dict = {}
        for provider, response in result.items():
            if hasattr(response, "dict"):
                result_dict[provider] = response.dict()
            elif hasattr(response, "__dict__"):
                result_dict[provider] = response.__dict__
            else:
                result_dict[provider] = str(response)
        return result_dict
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        if hasattr(researcher, "cleanup"):
            await researcher.cleanup()


@app.get("/")
async def health_check():
    return {"status": "ok"}