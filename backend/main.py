import base64
import json
import os
from io import BytesIO
from uuid import uuid4
from typing import Optional
import fastapi
from fastapi import FastAPI, File, Form, UploadFile, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend.chat import chat
from backend.sd import sd
from backend.schemas import ChatRequest, GenerateRequest
from backend.controlNetCanny import control_net_Canny
from backend.db.database import engine, get_db
from backend.db.models import Base
from backend.db.crud import save_chat_message, get_chat_history, build_ollama_messages,getChatAllHistory

app = FastAPI()
start = True

Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}

@app.get("/images/history")
async def get_image_history():
    # Placeholder for image history retrieval logic
    return {"images": []}

@app.get("/chat/history")
async def get_all_chat_history(db: Session = Depends(get_db)):
    history = getChatAllHistory(db)
    return [{"convo_id": msg.convo_id, "role": msg.role, "content": msg.content} for msg in history]

@app.get("/chat/history/{conversation_id}")
async def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    messages = get_chat_history(db, conversation_id)
    return [{"convo_id": msg.convo_id, "role": msg.role, "content": msg.content} for msg in messages]
    


@app.post("/chat")
async def chat_stream(request: fastapi.Request, ChatRequest: ChatRequest, db: Session = Depends(get_db)):
    # Debug: log raw request body
    body = await request.body()

    if ChatRequest.convo_id:
        convo_id = ChatRequest.convo_id
    else:
        convo_id = str(uuid4().hex)
    
    # Get existing conversation history if convo_id exists
    history = get_chat_history(db, convo_id)
    if history:
        context_lines = [f"{msg.role}: {msg.content}" for msg in history]
        context_lines.append(f"user: {ChatRequest.prompt}")
        context_lines.append("assistant:")
        prompt_for_model = "\n".join(context_lines)
    else:
        prompt_for_model = ChatRequest.prompt

    save_chat_message(
        db=db,
        convo_id=convo_id,
        role="user",
        content=ChatRequest.prompt,
    )
    
    async def generate_and_save():
        full_response = ""
        # Yield convo_id first so client can store it
        yield json.dumps({"convo_id": convo_id}) + "\n"
        
        for chunk in chat(prompt_for_model):
            chunk_data = json.loads(chunk)
            if "response" in chunk_data:
                token = chunk_data["response"]
                full_response += token
                # Add a newline so the client can split the NDJSON stream correctly
                yield chunk + "\n"
        
        # Save complete response to database after streaming
        save_chat_message(
            db=db,
            convo_id=convo_id,
            role="assistant",
            content=full_response,
        )
    
    return StreamingResponse(generate_and_save(), media_type="application/x-ndjson")

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
        if Cimage is None:
            return {"error": "ControlNet enabled but no image provided"}
            
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

        return {"file_path": file_path}
    
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

        return {"file_path": file_path}