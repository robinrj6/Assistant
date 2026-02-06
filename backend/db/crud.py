from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import ChatMessage, ImageGeneration

def save_chat_message(db: Session, convo_id: str, role: str, content: str):
    chat_message = ChatMessage(convo_id=convo_id, role=role, content=content)
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    return chat_message

def getChatAllHistory(db: Session):
    subquery = db.query(func.max(ChatMessage.id).label('id')).filter(ChatMessage.role == "user").group_by(ChatMessage.convo_id).subquery()
    return db.query(ChatMessage).filter(ChatMessage.id.in_(db.query(subquery.c.id))).order_by(ChatMessage.timestamp.asc()).all()

def get_chat_history(db: Session, convo_id: str):
    return db.query(ChatMessage).filter(ChatMessage.convo_id == convo_id).all()


def build_ollama_messages(history, user_message):
    messages = [
        {"role": msg.role, "content": msg.content}
        for msg in history
    ]
    messages.append({"role": "user", "content": user_message})
    return messages