from fastapi import FastAPI
from chat import chat 
from schemas import ChatRequest, ChatResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/chat/", response_model=ChatResponse)
async def echo_prompt(ChatRequest: ChatRequest):
    response = chat(ChatRequest).response
    return {"response": response}

