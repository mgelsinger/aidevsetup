import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from .schemas import ChatRequest, ChatResponse
from .llm_client import LLMClient, PROVIDER

load_dotenv()

app = FastAPI(title="AI Dev Sandbox", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = LLMClient()

@app.get("/health")
def health():
    return {"status": "ok", "provider": PROVIDER}

@app.post("/v1/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    try:
        content = await client.chat([m.model_dump() for m in req.messages])
        return ChatResponse(content=content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))