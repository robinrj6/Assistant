import requests, json
from schemas import ChatRequest, ChatResponse

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"
    
def chat(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": req.prompt,
        "stream": False
    }

    r = requests.post(OLLAMA_URL, json=payload)
    r.raise_for_status()

    return ChatResponse(response=r.json()["response"])