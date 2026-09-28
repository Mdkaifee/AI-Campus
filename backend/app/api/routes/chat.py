"""Chat API — frontend talks only to this layer with user privacy isolation."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_chat_service, get_current_user_email
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatRequest,
    ChatResponse,
    ChatSessionResponse,
    ChatSource,
    ChatTurnResponse,
)
from app.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Ask the DAVIET assistant",
    description=(
        "Retrieves verified DAVIET knowledge, then asks AI to draft a student-friendly answer. "
        "The model is not allowed to invent college facts."
    ),
)
async def create_chat(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    user_email: Optional[str] = Depends(get_current_user_email),
) -> ChatResponse:
    turn = await service.ask(payload.message, payload.session_id, user_email=user_email)
    unavailable = not turn.sources and not turn.location
    return ChatResponse(
        session_id=turn.session_id,
        answer=turn.assistant_message,
        sources=[
            ChatSource(
                title=source.title,
                url=source.url,
                category=source.category,
                updated_at=source.updated_at,
            )
            for source in turn.sources
        ],
        location=turn.location,
        unavailable=unavailable,
    )


@router.post(
    "/stream",
    summary="Ask DAVIET assistant with SSE streaming",
)
async def create_chat_stream(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
    user_email: Optional[str] = Depends(get_current_user_email),
):
    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        service.ask_stream(payload.message, payload.session_id, user_email=user_email),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get(
    "/sessions",
    response_model=List[ChatSessionResponse],
    summary="List recent chat sessions for the authenticated user",
)
async def list_sessions(
    service: ChatService = Depends(get_chat_service),
    user_email: Optional[str] = Depends(get_current_user_email),
) -> List[ChatSessionResponse]:
    rows = await service.sessions(user_email=user_email)
    return [ChatSessionResponse(**row) for row in rows]


@router.get(
    "/sessions/{session_id}",
    response_model=ChatHistoryResponse,
    summary="Load one chat session",
)
async def get_session(
    session_id: str,
    service: ChatService = Depends(get_chat_service),
    user_email: Optional[str] = Depends(get_current_user_email),
) -> ChatHistoryResponse:
    if not session_id.strip():
        raise HTTPException(status_code=400, detail="Please enter a question.")
    turns = await service.history(session_id, user_email=user_email)
    return ChatHistoryResponse(
        session_id=session_id,
        turns=[
            ChatTurnResponse(
                user_message=turn.user_message,
                assistant_message=turn.assistant_message,
                sources=[
                    ChatSource(
                        title=source.title,
                        url=source.url,
                        category=source.category,
                        updated_at=source.updated_at,
                    )
                    for source in turn.sources
                ],
                location=turn.location,
                created_at=turn.created_at,
            )
            for turn in turns
        ],
    )


@router.delete(
    "/sessions/{session_id}",
    summary="Delete one chat session",
)
async def delete_session(
    session_id: str,
    service: ChatService = Depends(get_chat_service),
    user_email: Optional[str] = Depends(get_current_user_email),
) -> dict:
    if not session_id.strip():
        raise HTTPException(status_code=400, detail="Invalid session ID.")
    success = await service.delete_session(session_id, user_email=user_email)
    return {"ok": success, "session_id": session_id}
