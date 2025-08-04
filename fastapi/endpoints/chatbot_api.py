import json
import os
import sys

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from celery_worker.celery_app import celery_app

class ChatRequest(BaseModel):
    message: str
    conversation_id: str


router = APIRouter()

@router.post("/chat")
async def handle_chat(request: Request):
    try:
        data = await request.json()
        message = data.get('message')
        if not message or not message.strip():
            raise HTTPException(status_code=400, detail="Missing or empty 'message' field")

        conversation_id = data.get('conversation_id')
        if not conversation_id or not str(conversation_id).strip():
            raise HTTPException(status_code=400, detail="Missing or empty 'conversation_id' field")

        conversation_id = str(conversation_id).strip()

        print("Conversation id:", conversation_id)

        task = celery_app.send_task(
            'celery_worker.task.process_chatbot_request',
            args=[message.strip(), conversation_id]
        )

        return {
            "status": "processing",
            "task_id": task.id,
            "conversation_id": conversation_id
        }

    except HTTPException:
        raise
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

