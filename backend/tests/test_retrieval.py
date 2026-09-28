"""Retrieval layer tests — information quality matters."""

from app.repositories.knowledge_repository import KnowledgeRepository
from app.services.retrieval_service import RetrievalService


def _service() -> RetrievalService:
    repo = KnowledgeRepository()
    repo.load(force=True)
    return RetrievalService(repository=repo)


def test_knowledge_files_load():
    repo = KnowledgeRepository()
    repo.load(force=True)
    items = repo.list_all()
    assert len(items) >= 10
    assert all(item.title and item.content and item.source_url for item in items)


def test_library_timings_query_finds_library():
    results = _service().retrieve("What are the library timings?")
    assert results
    assert any("library" in r.category or "library" in r.title.lower() for r in results)


def test_hostel_query_finds_hostels():
    results = _service().retrieve("What hostels are available?")
    assert results
    assert any(r.category == "hostels" for r in results)


def test_tpo_alias_finds_placements():
    results = _service().retrieve("Where is the TPO office contact?")
    assert results
    assert any(r.category == "placements" for r in results)


def test_departments_query():
    results = _service().retrieve("What departments are available?")
    assert results
    assert any(r.category in {"departments", "admissions", "academics"} for r in results)


def test_grievance_query():
    results = _service().retrieve("How can I submit a grievance?")
    assert results
    assert any(r.category == "student_services" for r in results)


def test_address_query():
    results = _service().retrieve("What is the college address?")
    assert results
    assert any(r.category in {"contacts", "institute"} for r in results)


def test_fee_structure_query_finds_fees():
    results = _service().retrieve("what is the course fee for btech")
    assert results
    assert any("fee" in r.title.lower() or "admissions" in r.category for r in results)


def test_unrelated_question_returns_empty():
    results = _service().retrieve("Who will win the World Cup?")
    assert results == []


def test_empty_query_returns_empty():
    assert _service().retrieve("   ") == []
