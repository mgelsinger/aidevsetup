from pydantic import BaseModel, Field
from typing import List, Literal, Optional

Role = Literal["system", "user", "assistant"]

class Message(BaseModel):
    role: Role = Field(..., description="Who is speaking")
    content: str = Field(..., description="Message content")

class ChatRequest(BaseModel):
    messages: List[Message]

class ChatResponse(BaseModel):
    role: Role = "assistant"
    content: str