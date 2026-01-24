from typing import Optional
from pydantic import BaseModel

class ChatRequest(BaseModel):
    prompt: str

class ChatResponse(BaseModel):
    response: str
    
class GenerateRequest(BaseModel):
    prompt: str
    seed: Optional[int] = None
    steps: int = 20
    guidance_scale: float = 7.5
    use_controlnet: bool = False
