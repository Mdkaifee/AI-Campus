"""Orchestrate retrieval, AI generation, history, and error audit."""

from __future__ import annotations

import uuid
from typing import List, Optional, Sequence, Tuple

from app.core.logging import get_logger
from app.models.chat import ChatSource, ChatTurn
from app.models.knowledge import KnowledgeItem
from app.repositories.chat_repository import ChatRepository
from app.repositories.error_audit_repository import ErrorAuditRepository
from app.services.ai_service import (
    AI_UNAVAILABLE_ANSWER,
    AIProviderError,
    AIResult,
    AIService,
    OFF_TOPIC_ANSWER,
    UNKNOWN_DAVIET_ANSWER,
)
from app.services.location_service import LocationService
from app.services.retrieval_service import RetrievalService

from app.services.web_retrieval_service import WebRetrievalService

logger = get_logger(__name__)

GREETING_WORDS = {
    "hi", "hello", "hey", "namaste", "hola", "greetings",
    "good morning", "good afternoon", "good evening",
    "hi there", "hello there", "hy", "helo"
}

GREETING_ANSWER = (
    "Hello! 👋 I am the DAVIET Smart Campus AI Assistant. How can I help you today? "
    "Feel free to ask me anything about admissions, courses & fee structures, departments, library timings, campus navigation, hostels, or student services!"
)


def _is_greeting(message: str) -> bool:
    import re
    cleaned = re.sub(r"[^\w\s]", "", message.strip().lower())
    return cleaned in GREETING_WORDS


class ChatService:
    def __init__(
        self,
        retrieval: Optional[RetrievalService] = None,
        ai: Optional[AIService] = None,
        chat_repo: Optional[ChatRepository] = None,
        audit_repo: Optional[ErrorAuditRepository] = None,
        location_service: Optional[LocationService] = None,
        web_retrieval_service: Optional[WebRetrievalService] = None,
    ) -> None:
        self._retrieval = retrieval or RetrievalService()
        self._ai = ai or AIService()
        self._chat_repo = chat_repo or ChatRepository()
        self._audit_repo = audit_repo or ErrorAuditRepository()
        self._location_service = location_service or LocationService()
        self._web_retrieval = web_retrieval_service or WebRetrievalService()

    async def ask(self, message: str, session_id: Optional[str] = None) -> ChatTurn:
        session = session_id.strip() if session_id and session_id.strip() else str(uuid.uuid4())

        if _is_greeting(message):
            turn = ChatTurn(
                session_id=session,
                user_message=message,
                assistant_message=GREETING_ANSWER,
                sources=[],
                location=None,
                provider="rules",
                model="greeting",
            )
            await self._safe_save_turn(turn)
            return turn

        # Load recent conversational history to preserve multi-turn context
        recent = await self._safe_recent_turns(session)
        conversation = [
            (turn.user_message, turn.assistant_message) for turn in recent[-4:]
        ]

        # Check for campus location match (fuzzy typos like 'ug blok', context follow-ups)
        matched_loc = self._location_service.match_location(message, conversation_context=conversation)
        location_data = matched_loc.to_dict() if matched_loc else None

        # Fetch dynamic live catalog items (e.g. fees, PTU notifications)
        dynamic_items = await self._web_retrieval.fetch_dynamic_items(message)

        # Retrieve knowledge with conversation context expansion & dynamic items
        context = self._retrieval.retrieve(
            message, limit=3, conversation=conversation
        )
        # Merge dynamic catalog items if not already present in retrieved context
        existing_ids = {item.id for item in context}
        for item in dynamic_items:
            if item.id not in existing_ids:
                context.append(item)
                existing_ids.add(item.id)

        sources = [
            ChatSource(
                title=item.title,
                url=item.source_url,
                category=item.category,
                updated_at=item.updated_at,
            )
            for item in context
        ]

        answer, provider, model = await self._generate_answer(
            message=message,
            context=context,
            conversation=conversation,
            location_data=location_data,
            session_id=session,
        )

        turn = ChatTurn(
            session_id=session,
            user_message=message,
            assistant_message=answer,
            sources=sources if context else [],
            location=location_data,
            provider=provider,
            model=model,
        )
        await self._safe_save_turn(turn)
        return turn

    async def ask_stream(self, message: str, session_id: Optional[str] = None):
        session = session_id.strip() if session_id and session_id.strip() else str(uuid.uuid4())

        import json

        if _is_greeting(message):
            metadata_event = {
                "type": "metadata",
                "session_id": session,
                "sources": [],
                "location": None,
            }
            yield f"data: {json.dumps(metadata_event)}\n\n"
            yield f"data: {json.dumps({'type': 'token', 'content': GREETING_ANSWER})}\n\n"
            turn = ChatTurn(
                session_id=session,
                user_message=message,
                assistant_message=GREETING_ANSWER,
                sources=[],
                location=None,
                provider="rules",
                model="greeting",
            )
            await self._safe_save_turn(turn)
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        recent = await self._safe_recent_turns(session)
        conversation = [
            (turn.user_message, turn.assistant_message) for turn in recent[-4:]
        ]

        matched_loc = self._location_service.match_location(message, conversation_context=conversation)
        location_data = matched_loc.to_dict() if matched_loc else None

        # Fetch dynamic live catalog items (e.g. fees, PTU notifications)
        dynamic_items = await self._web_retrieval.fetch_dynamic_items(message)

        context = self._retrieval.retrieve(
            message, limit=3, conversation=conversation
        )
        existing_ids = {item.id for item in context}
        for item in dynamic_items:
            if item.id not in existing_ids:
                context.append(item)
                existing_ids.add(item.id)

        sources = [
            ChatSource(
                title=item.title,
                url=item.source_url,
                category=item.category,
                updated_at=item.updated_at,
            )
            for item in context
        ]

        import json
        metadata_event = {
            "type": "metadata",
            "session_id": session,
            "sources": [s.model_dump() if hasattr(s, "model_dump") else s.__dict__ for s in (sources if context else [])],
            "location": location_data,
        }
        yield f"data: {json.dumps(metadata_event)}\n\n"


        if not context and not location_data:
            if self._looks_off_topic(message, conversation):
                answer = OFF_TOPIC_ANSWER
            else:
                answer = UNKNOWN_DAVIET_ANSWER
            yield f"data: {json.dumps({'type': 'token', 'content': answer})}\n\n"
            turn = ChatTurn(
                session_id=session,
                user_message=message,
                assistant_message=answer,
                sources=[],
                location=None,
                provider="rules",
                model="fallback",
            )
            await self._safe_save_turn(turn)
            yield f"data: {json.dumps({'type': 'done'})}\n\n"
            return

        full_answer_chunks = []
        try:
            async for token in self._ai.generate_stream(
                question=message,
                context=context,
                conversation=conversation,
                location_meta=location_data,
            ):
                full_answer_chunks.append(token)
                yield f"data: {json.dumps({'type': 'token', 'content': token})}\n\n"
        except Exception as exc:
            logger.warning("Streaming AI failed, falling back to grounded knowledge: %s", type(exc).__name__)
            if context:
                primary = context[0]
                fallback_answer = f"Here is the verified information from official DAVIET records regarding **{primary.title}**:\n\n{primary.content}"
            elif location_data:
                fallback_answer = f"**{location_data.get('name')}** is located in **{location_data.get('block', 'Main Campus')}** ({location_data.get('floor', 'Ground Floor')}). {location_data.get('description', '')}"
            else:
                fallback_answer = AI_UNAVAILABLE_ANSWER
            full_answer_chunks = [fallback_answer]
            yield f"data: {json.dumps({'type': 'token', 'content': fallback_answer})}\n\n"

        complete_answer = "".join(full_answer_chunks).strip()
        turn = ChatTurn(
            session_id=session,
            user_message=message,
            assistant_message=complete_answer,
            sources=sources if context else [],
            location=location_data,
            provider=getattr(self._ai._provider, "__class__", {}).__name__ if hasattr(self._ai, "_provider") else "ai",
            model=getattr(self._ai._provider, "_model", "gemini-3.8-flash"),
        )
        await self._safe_save_turn(turn)

        yield f"data: {json.dumps({'type': 'done'})}\n\n"


    async def history(self, session_id: str) -> List[ChatTurn]:
        return await self._chat_repo.list_turns(session_id)

    async def sessions(self):
        return await self._chat_repo.list_sessions()

    async def delete_session(self, session_id: str) -> bool:
        return await self._chat_repo.delete_session(session_id)

    async def _generate_answer(
        self,
        *,
        message: str,
        context: Sequence[KnowledgeItem],
        conversation: Sequence[Tuple[str, str]],
        location_data: Optional[dict],
        session_id: str,
    ) -> Tuple[str, Optional[str], Optional[str]]:
        # If location is matched or context found, proceed with full AI reasoning
        if not context and not location_data:
            # Check if this could be an off-topic question or simply unknown
            if self._looks_off_topic(message, conversation):
                return OFF_TOPIC_ANSWER, None, None
            return UNKNOWN_DAVIET_ANSWER, None, None

        try:
            result: AIResult = await self._ai.generate_response(
                question=message,
                context=context,
                conversation=conversation,
                location_meta=location_data,
            )
            return result.answer, result.provider, result.model
        except AIProviderError as exc:
            await self._audit_repo.record(
                error_type="ai_provider_failure",
                message=str(exc),
                session_id=session_id,
                provider="ai",
            )
            if context:
                primary = context[0]
                return f"Here is the verified information from official DAVIET records regarding **{primary.title}**:\n\n{primary.content}", "grounded_knowledge", "knowledge_base"
            elif location_data:
                return f"**{location_data.get('name')}** is located in **{location_data.get('block', 'Main Campus')}** ({location_data.get('floor', 'Ground Floor')}). {location_data.get('description', '')}", "campus_map", "location_service"
            return AI_UNAVAILABLE_ANSWER, None, None
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unexpected AI failure")
            await self._audit_repo.record(
                error_type="ai_unexpected_failure",
                message=type(exc).__name__,
                session_id=session_id,
                provider="ai",
            )
            if context:
                primary = context[0]
                return f"Here is the verified information from official DAVIET records regarding **{primary.title}**:\n\n{primary.content}", "grounded_knowledge", "knowledge_base"
            elif location_data:
                return f"**{location_data.get('name')}** is located in **{location_data.get('block', 'Main Campus')}** ({location_data.get('floor', 'Ground Floor')}). {location_data.get('description', '')}", "campus_map", "location_service"
            return AI_UNAVAILABLE_ANSWER, None, None

    async def _safe_recent_turns(self, session_id: str) -> List[ChatTurn]:
        try:
            return await self._chat_repo.list_recent_turns(session_id, limit=4)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to load recent turns: %s", type(exc).__name__)
            await self._audit_repo.record(
                error_type="database_read_failure",
                message=type(exc).__name__,
                session_id=session_id,
            )
            return []

    async def _safe_save_turn(self, turn: ChatTurn) -> None:
        try:
            await self._chat_repo.save_turn(turn)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to save chat history: %s", type(exc).__name__)
            await self._audit_repo.record(
                error_type="database_write_failure",
                message=type(exc).__name__,
                session_id=turn.session_id,
            )

    def _looks_off_topic(self, message: str, conversation: Sequence[Tuple[str, str]]) -> bool:
        text = message.lower()

        # If recent conversation was on college topics, don't prematurely classify short turns as off-topic
        if conversation:
            recent_text = " ".join([f"{u} {a}" for u, a in conversation[-2:]]).lower()
            if any(hint in recent_text for hint in ("daviet", "college", "fee", "block", "library", "hostel", "tpo", "placement", "dept")):
                return False

        campus_hints = (
            "daviet", "college", "campus", "library", "lib", "hostel", "admission",
            "department", "placement", "tpo", "jalandhar", "fee", "fees", "tuition",
            "btech", "course", "courses", "ptu", "ikg", "scholarship", "branch",
            "engineering", "exam", "grievance", "block", "blok", "audi", "auditorium",
            "canteen", "mess", "lab", "workshop", "office", "principal", "timing",
            "timings", "hours", "open", "closed", "schedule", "working", "rn", "today",
            "where", "directions", "location", "ug", "pg", "rd"
        )
        return not any(hint in text for hint in campus_hints)
