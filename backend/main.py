import base64
import os
from io import BytesIO
from uuid import uuid4
from typing import Optional
from fastapi import FastAPI, File, Form, UploadFile, Depends
from sqlalchemy.orm import Session
from chat import chat
from sd import sd
from schemas import ChatRequest, GenerateRequest
from controlNetCanny import control_net_Canny
from db.database import engine, get_db
from db.models import Base
from db.crud import save_chat_message, get_chat_history, build_ollama_messages

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/images/history")
async def get_image_history():
    # Placeholder for image history retrieval logic
    return {"images": []}


@app.get("/chat/history/{conversation_id}")
async def get_chat_history(conversation_id: str):
    # Placeholder for chat history retrieval logic
    return {"conversation_id": conversation_id, "messages": []}


@app.post("/chat")
async def chat_stream(ChatRequest: ChatRequest):
    save_chat_message(
        db=Depends(get_db),
        convo_id=ChatRequest.convo_id,
        role="user",
        content=ChatRequest.prompt,
    )
    response = chat(ChatRequest)
    
    save_chat_message(
        db=Depends(get_db),
        convo_id=ChatRequest.convo_id,
        role="assistant",
        content=response,
    )
    # # Ensure response is serializable
    return response

@app.post("/images/generate")
async def controlnetCanny_generate(
    prompt: str = Form(...),
    seed: Optional[int] = Form(None),
    steps: int = Form(20),
    guidance_scale: float = Form(7.5),
    use_controlnet: bool = Form(False),
    Cimage: Optional[UploadFile] = File(None),
):
    if use_controlnet:
        # Build the generation request from form fields so FastAPI can handle mixed file/form data
        generate_request = GenerateRequest(
            prompt=prompt,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            use_controlnet=True,
        )

        # Read uploaded file bytes for the ControlNet canny processor
        image_bytes = await Cimage.read()
        image = control_net_Canny(generate_request, image_bytes)
        
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
    
    else:
        generate_request = GenerateRequest(
            prompt=prompt,
            seed=seed,
            steps=steps,
            guidance_scale=guidance_scale,
            use_controlnet=False,
        )
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