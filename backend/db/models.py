from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from .database import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True)
    convo_id = Column(String, index=True)
    role = Column(String, index=True)  # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
    

class ImageGeneration(Base):
    __tablename__ = "image_generations"

    id = Column(Integer, primary_key=True)
    prompt = Column(Text)
    seed = Column(Integer, nullable=True)
    steps = Column(Integer)
    guidance_scale = Column(Integer)
    use_controlnet = Column(Integer)  # 0 or 1
    control_image_path = Column(String)
    result_image_path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)