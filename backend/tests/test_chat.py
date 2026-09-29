"""Chat API, history, AI failure, and retrieval-grounded answers."""

from datetime import datetime, timezone
from typing import List

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.chat import ChatTurn
from app.models.knowledge import KnowledgeItem
from app.repositories.chat_repository import ChatRepository
from app.repositories.error_audit_repository import ErrorAuditRepository
from app.services.ai_service import AIProviderError, AIResult, AIService
from app.services.chat_service import ChatService
from app.services.retrieval_service import RetrievalService


class FakeChatRepository(ChatRepository):
    def __init__(self) -> None:
        super().__init__(db=None)
        self.turns: List[ChatTurn] = []
        self.fail_save = False
        self.fail_read = False

    async def save_turn(self, turn: ChatTurn) -> None:
        if self.fail_save:
            raise RuntimeError("db_down")
        self.turns.append(turn)

    async def list_turns(self, session_id: str, *, limit: int = 50) -> List[ChatTurn]:
        if self.fail_read:
            raise RuntimeError("db_down")
        return [turn for turn in self.turns if turn.session_id == session_id][:limit]

    async def list_recent_turns(self, session_id: str, *, limit: int = 4) -> List[ChatTurn]:
        if self.fail_read:
            raise RuntimeError("db_down")
        matches = [turn for turn in self.turns if turn.session_id == session_id]
        return matches[-limit:]

    async def list_sessions(self, *, limit: int = 30):
        return []


class FakeAuditRepository(ErrorAuditRepository):
    def __init__(self) -> None:
        super().__init__(db=None)
        self.records = []

    async def record(self, **kwargs) -> None:
        self.records.append(kwargs)


class StubAIService(AIService):
    def __init__(self, answer: str = "The DAVIET Central Library is open Monday to Friday from 8:00 AM to 6:30 PM.") -> None:
        self.answer = answer
        self.fail = False
        self.calls = 0
        self.conversations = []

    async def generate_response(self, question: str, context, conversation=None, **kwargs) -> AIResult:
        self.calls += 1
        self.conversations.append(list(conversation or []))
        if self.fail:
            raise AIProviderError("offline")
        return AIResult(answer=self.answer, provider="ollama", model="llama3.2")


@pytest.fixture
def chat_stack():
    repo = FakeChatRepository()
    audit = FakeAuditRepository()
    ai = StubAIService()
    service = ChatService(
        retrieval=RetrievalService(),
        ai=ai,
        chat_repo=repo,
        audit_repo=audit,
    )
    app.state.chat_service = service
    app.state.db = None
    return {"service": service, "repo": repo, "audit": audit, "ai": ai}


@pytest.mark.asyncio
async def test_valid_library_question(chat_stack):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/chat", json={"message": "What are the library timings?"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["session_id"]
    assert "library" in payload["answer"].lower()
    assert payload["sources"]
    assert payload["sources"][0]["title"]
    assert payload["sources"][0]["url"].startswith("https://")
    assert chat_stack["repo"].turns
    assert chat_stack["repo"].turns[0].session_id == payload["session_id"]


@pytest.mark.asyncio
async def test_empty_question_is_rejected(chat_stack):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/chat", json={"message": "   "})
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_unknown_question_does_not_hallucinate(chat_stack):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/chat", json={"message": "Who will win the World Cup?"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["sources"] == []
    assert payload["unavailable"] is True
    assert "DAVIET" in payload["answer"]
    assert chat_stack["ai"].calls == 0


@pytest.mark.asyncio
async def test_ai_failure_returns_clear_message(chat_stack):
    chat_stack["ai"].fail = True
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/chat", json={"message": "Tell me about the library."})
    assert response.status_code == 200
    payload = response.json()
    assert "temporarily unavailable" in payload["answer"].lower()
    assert chat_stack["audit"].records
    assert chat_stack["audit"].records[0]["error_type"] == "ai_provider_failure"


@pytest.mark.asyncio
async def test_database_failure_still_answers(chat_stack):
    chat_stack["repo"].fail_save = True
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        response = await client.post("/api/chat", json={"message": "What are the library timings?"})
    assert response.status_code == 200
    assert response.json()["answer"]
    assert any(row["error_type"] == "database_write_failure" for row in chat_stack["audit"].records)


@pytest.mark.asyncio
async def test_session_id_is_preserved(chat_stack):
    session_id = "session-demo-1"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        first = await client.post(
            "/api/chat",
            json={"session_id": session_id, "message": "What are the library timings?"},
        )
        second = await client.post(
            "/api/chat",
            json={"session_id": session_id, "message": "What hostels are available?"},
        )
        history = await client.get(f"/api/chat/sessions/{session_id}")
    assert first.json()["session_id"] == session_id
    assert second.json()["session_id"] == session_id
    assert history.status_code == 200
    assert len(history.json()["turns"]) == 2
    assert all(turn.session_id == session_id for turn in chat_stack["repo"].turns)
    assert chat_stack["ai"].conversations[1] == []
