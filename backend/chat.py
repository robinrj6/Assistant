import requests, json
from backend.schemas import ChatRequest, ChatResponse

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "gemma3:1b"
    
def chat(req: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "prompt": req.prompt,
        "stream": True
    }

    with requests.post(OLLAMA_URL, json=payload, stream=True) as r:
        for line in r.iter_lines():
            if line:
                yield line.decode("utf-8")