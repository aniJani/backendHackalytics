from fastapi import APIRouter
from app.models.schema import ChatRequest
from app.services.insights_service import chat_with_assistant

router = APIRouter()


@router.post("/chat")
async def chat_with_bot(request: ChatRequest):
    # For simplicity, we assume no dataset context here.
    reply = chat_with_assistant(
        [{"role": "user", "content": request.message}], "No dataset summary provided"
    )
    return {"reply": reply}
