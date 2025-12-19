from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.chatbot.nlp import handle_query


router = APIRouter(prefix="/chatbot", tags=["chatbot"])


class ChatRequest(BaseModel):
    query: str


@router.post("")
def chatbot(req: ChatRequest, db: Session = Depends(get_db)):
    return handle_query(db, req.query)



