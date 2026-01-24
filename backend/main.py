import base64
import os
from io import BytesIO
from uuid import uuid4

from fastapi import FastAPI

from chat import chat
from sd import sd
from schemas import ChatRequest, GenerateRequest

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.post("/chat_stream")
async def chat_stream(ChatRequest: ChatRequest):
    response = await chat(ChatRequest)

    # Ensure response is serializable
    return response

@app.post("/sd")
async def sd_generate(generate_request: GenerateRequest):
    image = sd(generate_request)

    # Encode the PIL image as base64 so FastAPI can serialize it to JSON
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    
    # Save image locally under backend/outputs
    base_dir = os.path.dirname(__file__)
    output_dir = os.path.join(base_dir, "outputs")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"sd_{uuid4().hex}.png"
    file_path = os.path.join(output_dir, filename)
    image.save(file_path, format="PNG")

    return {"image_base64": encoded, "file_path": file_path}