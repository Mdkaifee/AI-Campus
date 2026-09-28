"""Ollama & Cloud AI generation. Production-grade conversational intelligence with YAML prompt loading."""

from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Protocol, Sequence

import httpx

from app.core.config import get_settings
from app.core.logging import get_logger
from app.models.knowledge import KnowledgeItem

logger = get_logger(__name__)

PROMPT_FILE = Path(__file__).resolve().parents[1] / "core" / "prompts" / "system_prompt.yaml"

DEFAULT_FALLBACK_PROMPT = """You are the DAVIET Smart Campus AI Assistant for DAV Institute of Engineering & Technology (DAVIET), Jalandhar, Punjab.
Affiliated to IKG-PTU and approved by AICTE.

Role & Behavioral Persona:
- You are an intelligent, empathetic, articulate AI companion — comparable to ChatGPT / Gemini in fluency, warmth, and responsiveness.
- Ground all DAVIET-specific academic facts, fees, syllabus, facilities, and intake numbers in the provided verified context.
- When answering location / campus navigation questions, provide clear building, block, floor, and landmark descriptions.
- Tolerate student typos and abbreviations gracefully (e.g. 'ug blok' -> Core / Undergraduate Block, 'audi' -> Auditorium, 'tpo' -> Training & Placement Office).
- If the conversation was already discussing locations and the student inputs another place name, treat it as a navigation follow-up.
- Answer clearly and directly first, followed by well-structured bullet points where appropriate.
"""


def load_system_prompt() -> str:
    """Load system prompt from external YAML or return the comprehensive fallback."""
    if PROMPT_FILE.exists():
        try:
            content = PROMPT_FILE.read_text(encoding="utf-8")
            if content.strip():
                return content
        except Exception as exc:  # noqa: BLE001
            logger.warning("Could not read system_prompt.yaml: %s", type(exc).__name__)
    return DEFAULT_FALLBACK_PROMPT


SYSTEM_PROMPT = load_system_prompt()

UNKNOWN_DAVIET_ANSWER = (
    "I couldn't find specific official records for that in the DAVIET knowledge base. "
    "For the most accurate and up-to-date confirmation, please visit the official DAVIET website at **davietjal.org** "
    "or check directly with the college administrative office."
)

OFF_TOPIC_ANSWER = (
    "I am the DAVIET Smart Campus Assistant, dedicated to helping with college-related queries such as "
    "admissions, course fee structures, departments, library timings, campus navigation, hostels, and student services. "
    "Feel free to ask anything about DAVIET!"
)

AI_UNAVAILABLE_ANSWER = (
    "I'm experiencing a brief moment of high demand — please send your message again in a few seconds and I'll respond right away! 🙏"
)


class AIProviderError(Exception):
    """Raised when the AI provider cannot generate a response."""


@dataclass
class AIResult:
    answer: str
    provider: str
    model: str
    attempts: int = 1
    fallback_used: bool = False


class AIProvider(Protocol):
    async def generate_response(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ) -> AIResult:
        ...


def _format_context(items: Sequence[KnowledgeItem], location_meta: Optional[dict] = None) -> str:
    blocks: List[str] = []

    # If a campus location was matched, feed location ground truth directly into AI context
    if location_meta:
        blocks.append(
            "\n".join(
                [
                    f"[Verified Campus Location Destination] {location_meta.get('name')}",
                    f"Block / Building: {location_meta.get('block', 'Main Campus')}",
                    f"Floor / Level: {location_meta.get('floor', 'Ground Floor')}",
                    f"Directions & Description: {location_meta.get('description', '')}",
                    "Interactive Google Maps and navigation links are being rendered on the student's screen.",
                ]
            )
        )

    for index, item in enumerate(items, start=1):
        blocks.append(
            "\n".join(
                [
                    f"[Source {index}] {item.title}",
                    f"Category: {item.category}",
                    f"Updated: {item.updated_at}",
                    f"URL: {item.source_url}",
                    item.content,
                ]
            )
        )

    if not blocks:
        return "(No matching DAVIET knowledge-base entries were found.)"
    return "\n\n".join(blocks)


def _format_conversation(conversation: Optional[Sequence[tuple[str, str]]]) -> str:
    if not conversation:
        return "(No previous turns.)"
    lines = []
    for user_message, assistant_message in conversation:
        lines.append(f"Student: {user_message}")
        lines.append(f"Assistant: {assistant_message}")
    return "\n".join(lines)


class OllamaAIService:
    def __init__(
        self,
        *,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        settings = get_settings()
        self._base_url = (base_url or settings.ollama_base_url).rstrip("/")
        self._model = model or settings.ollama_model
        self._timeout = timeout_seconds or settings.ai_timeout_seconds
        self._client = client

    async def generate_response(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ) -> AIResult:
        from datetime import datetime, timezone, timedelta
        # DAVIET is in Punjab, India (IST is UTC+5:30)
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_tz)
        current_time_str = now_ist.strftime("%A, %d %B %Y %I:%M %p IST")
        day_of_week = now_ist.strftime("%A")
        hour_24 = now_ist.hour
        # Weekdays: Monday to Friday
        is_weekday = now_ist.weekday() < 5
        is_academic_hours = is_weekday and (9 <= hour_24 < 17)

        if is_academic_hours:
            status_summary = f"Currently OPEN for academic classes and offices ({current_time_str})."
        elif is_weekday and (hour_24 >= 17 or hour_24 < 9):
            status_summary = f"Currently CLOSED for academic classes (it is {current_time_str}; regular hours are 9:00 AM - 5:00 PM Monday-Friday). Hostels remain open 24/7."
        elif now_ist.weekday() == 5: # Saturday
            status_summary = f"Currently Saturday ({current_time_str}). Administrative offices and library open partially; academic lectures closed."
        else: # Sunday
            status_summary = f"Currently Sunday ({current_time_str}). Academic classes and administrative offices are CLOSED today. Hostels remain open 24/7."

        current_system_prompt = load_system_prompt()
        prompt = (
            f"{current_system_prompt}\n\n"
            f"[Current Live Campus Time & Day]: {current_time_str}\n"
            f"[Live Campus Operating Status]: {status_summary}\n\n"
            f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
            f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
            f"Student Question: {question}\n\n"
            "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
        )
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.3,
                "num_predict": 300,
                "num_ctx": 2048,
            },
        }

        url = f"{self._base_url}/api/generate"

        try:
            if self._client is not None:
                response = await self._client.post(url, json=payload)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=payload)
        except httpx.TimeoutException as exc:
            logger.error("Ollama timeout model=%s", self._model)
            raise AIProviderError("timeout") from exc
        except httpx.HTTPError as exc:
            logger.error("Ollama HTTP error: %s", type(exc).__name__)
            raise AIProviderError("network") from exc

        if response.status_code >= 400:
            logger.error("Ollama status=%s model=%s", response.status_code, self._model)
            raise AIProviderError(f"status_{response.status_code}")

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("invalid_json") from exc

        answer = (data.get("response") or "").strip()
        if not answer:
            raise AIProviderError("empty_response")

        return AIResult(
            answer=answer,
            provider="ollama",
            model=self._model,
            attempts=1,
        )

    async def generate_stream(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ):
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        now_ist = datetime.now(ist_tz)
        current_time_str = now_ist.strftime("%A, %d %B %Y %I:%M %p IST")
        day_of_week = now_ist.strftime("%A")
        hour_24 = now_ist.hour
        is_weekday = now_ist.weekday() < 5
        is_academic_hours = is_weekday and (9 <= hour_24 < 17)

        if is_academic_hours:
            status_summary = f"Currently OPEN for academic classes and offices ({current_time_str})."
        elif is_weekday and (hour_24 >= 17 or hour_24 < 9):
            status_summary = f"Currently CLOSED for academic classes (it is {current_time_str}; regular hours are 9:00 AM - 5:00 PM Monday-Friday). Hostels remain open 24/7."
        elif now_ist.weekday() == 5:
            status_summary = f"Currently Saturday ({current_time_str}). Administrative offices and library open partially; academic lectures closed."
        else:
            status_summary = f"Currently Sunday ({current_time_str}). Academic classes and administrative offices are CLOSED today. Hostels remain open 24/7."

        current_system_prompt = load_system_prompt()
        prompt = (
            f"{current_system_prompt}\n\n"
            f"[Current Live Campus Time & Day]: {current_time_str}\n"
            f"[Live Campus Operating Status]: {status_summary}\n\n"
            f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
            f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
            f"Student Question: {question}\n\n"
            "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
        )
        payload = {
            "model": self._model,
            "prompt": prompt,
            "stream": True,
            "options": {
                "temperature": 0.3,
                "num_predict": 300,
                "num_ctx": 2048,
            },
        }
        url = f"{self._base_url}/api/generate"

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream("POST", url, json=payload) as response:
                    if response.status_code >= 400:
                        raise AIProviderError(f"status_{response.status_code}")
                    import json
                    async for line in response.aiter_lines():
                        if line:
                            try:
                                chunk = json.loads(line)
                                token = chunk.get("response", "")
                                if token:
                                    yield token
                            except ValueError:
                                continue
        except Exception as exc:
            logger.error("Ollama streaming error: %s", type(exc).__name__)
            raise AIProviderError("stream_failed") from exc



class OpenAICompatibleAIService:
    """Optional cloud provider implementation (OpenAI, Gemini OpenAI-compatible, etc.)."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.ai_api_key
        self._base_url = (base_url or settings.ollama_base_url or "https://api.openai.com/v1").rstrip("/")
        model_name = model or settings.ai_model or "gpt-4o-mini"
        if "gemini" in model_name.lower() and model_name in {"gemini-2.0-flash", "gemini-1.5-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite", "gemini-2.0-flash-exp"}:
            model_name = "gemini-flash-lite-latest"
        self._model = model_name
        self._timeout = timeout_seconds or settings.ai_timeout_seconds
        self._client = client

    async def generate_response(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ) -> AIResult:
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time_str = datetime.now(ist_tz).strftime("%A, %d %B %Y %I:%M %p IST")

        current_system_prompt = load_system_prompt()
        messages = [
            {"role": "system", "content": current_system_prompt},
            {
                "role": "user",
                "content": (
                    f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                    f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                    f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                    f"Student Question: {question}\n\n"
                    "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                ),
            },
        ]
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": 0.3,
        }
        url = f"{self._base_url}/chat/completions"
        if "generativelanguage.googleapis.com" in self._base_url:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:generateContent?key={self._api_key}"
            gemini_payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": (
                                    f"{current_system_prompt}\n\n"
                                    f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                                    f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                                    f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                                    f"Student Question: {question}\n\n"
                                    "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                                )
                            }
                        ],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                },
            }
            max_retries = 4
            retry_wait = [2, 5, 12]
            for attempt in range(max_retries):
                try:
                    async with httpx.AsyncClient(timeout=self._timeout) as client:
                        response = await client.post(url, json=gemini_payload)
                    if response.status_code in (429, 503):
                        if attempt < max_retries - 1:
                            wait_s = retry_wait[min(attempt, len(retry_wait) - 1)]
                            logger.warning("Gemini 429/503 attempt %d — retrying in %ds", attempt + 1, wait_s)
                            await asyncio.sleep(wait_s)
                            continue
                        raise AIProviderError(f"status_{response.status_code}")
                    if response.status_code >= 400:
                        raise AIProviderError(f"status_{response.status_code}")
                    data = response.json()
                    candidates = data.get("candidates") or []
                    parts = candidates[0].get("content", {}).get("parts") if candidates else []
                    answer = (parts[0].get("text") or "").strip() if parts else ""
                    if not answer:
                        raise AIProviderError("empty_response")
                    return AIResult(
                        answer=answer,
                        provider="gemini_native",
                        model=self._model,
                        attempts=attempt + 1,
                    )
                except AIProviderError:
                    raise
                except Exception as exc:
                    if attempt < max_retries - 1:
                        wait_s = retry_wait[min(attempt, len(retry_wait) - 1)]
                        logger.warning("Gemini attempt %d failed: %s — retrying in %ds", attempt + 1, type(exc).__name__, wait_s)
                        await asyncio.sleep(wait_s)
                        continue
                    logger.error("Native Gemini generate error after %d attempts: %s", max_retries, type(exc).__name__)
                    raise AIProviderError("native_gemini_failed") from exc
            raise AIProviderError("max_retries_exceeded")

        try:
            if self._client is not None:
                response = await self._client.post(url, json=payload, headers=headers)
            else:
                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    response = await client.post(url, json=payload, headers=headers)
        except httpx.TimeoutException as exc:
            logger.error("Cloud AI timeout model=%s", self._model)
            raise AIProviderError("timeout") from exc
        except httpx.HTTPError as exc:
            logger.error("Cloud AI HTTP error: %s", type(exc).__name__)
            raise AIProviderError("network") from exc



        if response.status_code >= 400:
            logger.error("Cloud AI status=%s model=%s", response.status_code, self._model)
            raise AIProviderError(f"status_{response.status_code}")

        try:
            data = response.json()
        except ValueError as exc:
            raise AIProviderError("invalid_json") from exc

        choices = data.get("choices") or []
        if not choices:
            raise AIProviderError("empty_response")

        answer = (choices[0].get("message", {}).get("content") or "").strip()
        if not answer:
            raise AIProviderError("empty_response")

        return AIResult(
            answer=answer,
            provider="openai_compatible",
            model=self._model,
            attempts=1,
        )

    async def generate_stream(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ):
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time_str = datetime.now(ist_tz).strftime("%A, %d %B %Y %I:%M %p IST")

        current_system_prompt = load_system_prompt()
        messages = [
            {"role": "system", "content": current_system_prompt},
            {
                "role": "user",
                "content": (
                    f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                    f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                    f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                    f"Student Question: {question}\n\n"
                    "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                ),
            },
        ]
        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self._model,
            "messages": messages,
            "temperature": 0.3,
            "stream": True,
        }
        url = f"{self._base_url}/chat/completions"
        if "generativelanguage.googleapis.com" in self._base_url:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self._model}:streamGenerateContent?alt=sse&key={self._api_key}"
            gemini_payload = {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": (
                                    f"{current_system_prompt}\n\n"
                                    f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                                    f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                                    f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                                    f"Student Question: {question}\n\n"
                                    "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                                )
                            }
                        ],
                    }
                ],
                "generationConfig": {
                    "temperature": 0.3,
                },
            }
            max_retries = 4
            retry_wait = [2, 5, 12]  # wait seconds before each retry on 429/503
            for attempt in range(max_retries):
                retry_needed = False
                collected: list[str] = []
                attempt_error: Exception | None = None

                async with httpx.AsyncClient(timeout=self._timeout) as client:
                    try:
                        async with client.stream("POST", url, json=gemini_payload) as response:
                            if response.status_code in (429, 503):
                                retry_needed = True
                            elif response.status_code >= 400:
                                attempt_error = AIProviderError(f"status_{response.status_code}")
                            else:
                                async for line in response.aiter_lines():
                                    if line and line.startswith("data: "):
                                        raw_data = line[6:].strip()
                                        try:
                                            chunk = json.loads(raw_data)
                                            cands = chunk.get("candidates") or []
                                            if cands:
                                                cparts = cands[0].get("content", {}).get("parts") or []
                                                for cp in cparts:
                                                    if "thoughtSignature" in cp:
                                                        continue
                                                    t = cp.get("text", "")
                                                    if t:
                                                        collected.append(t)
                                        except (ValueError, KeyError, IndexError):
                                            pass
                    except AIProviderError:
                        raise
                    except Exception as exc:
                        attempt_error = exc

                # All context managers are closed — now handle results safely
                if isinstance(attempt_error, AIProviderError):
                    raise attempt_error
                if attempt_error is not None:
                    if attempt < max_retries - 1:
                        wait_s = retry_wait[min(attempt, len(retry_wait) - 1)]
                        logger.warning("Gemini stream attempt %d failed: %s — retrying in %ds", attempt + 1, type(attempt_error).__name__, wait_s)
                        await asyncio.sleep(wait_s)
                        continue
                    logger.error("Native Gemini streaming error after %d attempts: %s", max_retries, type(attempt_error).__name__)
                    raise AIProviderError("stream_failed") from attempt_error

                if retry_needed:
                    if attempt < max_retries - 1:
                        wait_s = retry_wait[min(attempt, len(retry_wait) - 1)]
                        logger.warning("Gemini 429/503 on attempt %d — retrying in %ds", attempt + 1, wait_s)
                        await asyncio.sleep(wait_s)
                        continue
                    raise AIProviderError("status_429")

                # Yield all tokens — completely outside try/async-with blocks
                for tok in collected:
                    yield tok
                return  # success

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code >= 400:
                        raise AIProviderError(f"status_{response.status_code}")
                    import json
                    async for line in response.aiter_lines():
                        if line and line.startswith("data: "):
                            raw_data = line[6:].strip()
                            if raw_data == "[DONE]":
                                break
                            try:
                                chunk = json.loads(raw_data)
                                choices = chunk.get("choices") or []
                                if choices:
                                    token = choices[0].get("delta", {}).get("content") or ""
                                    if token:
                                        yield token
                            except ValueError:
                                continue
        except Exception as exc:
            logger.error("Cloud AI streaming error: %s", type(exc).__name__)
            raise AIProviderError("stream_failed") from exc




class AnthropicClaudeAIService:
    """Native Anthropic Claude generation service."""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout_seconds: Optional[float] = None,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        settings = get_settings()
        self._api_key = api_key or settings.ai_api_key
        self._model = model or settings.ai_model or "claude-haiku-4-5-20251001"
        self._timeout = timeout_seconds or settings.ai_timeout_seconds
        self._client = client

    async def generate_response(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ) -> AIResult:
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time_str = datetime.now(ist_tz).strftime("%A, %d %B %Y %I:%M %p IST")

        current_system_prompt = load_system_prompt()
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self._model,
            "max_tokens": 1024,
            "system": current_system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                        f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                        f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                        f"Student Question: {question}\n\n"
                        "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                    ),
                }
            ],
        }
        url = "https://api.anthropic.com/v1/messages"

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                response = await client.post(url, json=payload, headers=headers)
            if response.status_code >= 400:
                logger.error("Claude status=%s model=%s: %s", response.status_code, self._model, response.text)
                raise AIProviderError(f"status_{response.status_code}")
            data = response.json()
            content_list = data.get("content") or []
            answer = (content_list[0].get("text") or "").strip() if content_list else ""
            if not answer:
                raise AIProviderError("empty_response")
            return AIResult(
                answer=answer,
                provider="anthropic_claude",
                model=self._model,
                attempts=1,
            )
        except AIProviderError:
            raise
        except Exception as exc:
            logger.error("Claude generate error: %s", type(exc).__name__)
            raise AIProviderError("claude_failed") from exc

    async def generate_stream(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ):
        from datetime import datetime, timezone, timedelta
        ist_tz = timezone(timedelta(hours=5, minutes=30))
        current_time_str = datetime.now(ist_tz).strftime("%A, %d %B %Y %I:%M %p IST")

        current_system_prompt = load_system_prompt()
        headers = {
            "x-api-key": self._api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        payload = {
            "model": self._model,
            "max_tokens": 1024,
            "system": current_system_prompt,
            "stream": True,
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"[Current Live Campus Local Time]: {current_time_str}\n\n"
                        f"Verified DAVIET Campus Context:\n{_format_context(context, location_meta)}\n\n"
                        f"Recent Conversation History:\n{_format_conversation(conversation)}\n\n"
                        f"Student Question: {question}\n\n"
                        "Respond naturally, authoritatively, and helpfully as DAVIET Campus AI:"
                    ),
                }
            ],
        }
        url = "https://api.anthropic.com/v1/messages"

        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream("POST", url, json=payload, headers=headers) as response:
                    if response.status_code >= 400:
                        err_text = await response.aread()
                        logger.error("Claude stream status=%s: %s", response.status_code, err_text.decode("utf-8", errors="ignore"))
                        raise AIProviderError(f"status_{response.status_code}")
                    import json
                    async for line in response.aiter_lines():
                        if line and line.startswith("data: "):
                            raw_data = line[6:].strip()
                            if raw_data == "[DONE]":
                                break
                            try:
                                event = json.loads(raw_data)
                                if event.get("type") == "content_block_delta":
                                    delta = event.get("delta") or {}
                                    if delta.get("type") == "text_delta":
                                        tok = delta.get("text") or ""
                                        if tok:
                                            yield tok
                            except ValueError:
                                continue
        except AIProviderError:
            raise
        except Exception as exc:
            logger.error("Claude streaming error: %s", type(exc).__name__)
            raise AIProviderError("stream_failed") from exc


class AIService:
    """Provider-agnostic wrapper used by ChatService."""

    def __init__(self, provider: Optional[AIProvider] = None) -> None:
        if provider is not None:
            self._provider = provider
            return

        settings = get_settings()
        if (
            settings.ai_provider in {"anthropic", "claude"}
            or (settings.ai_api_key and settings.ai_api_key.startswith("sk-ant-"))
            or ("claude" in (settings.ai_model or "").lower())
        ):
            self._provider = AnthropicClaudeAIService()
        elif settings.ai_provider in {"openai", "cloud", "openai_compatible"}:
            self._provider = OpenAICompatibleAIService()
        else:
            self._provider = OllamaAIService()

    async def generate_response(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ) -> AIResult:
        return await self._provider.generate_response(
            question,
            context,
            conversation,
            location_meta=location_meta,
        )

    async def generate_stream(
        self,
        question: str,
        context: Sequence[KnowledgeItem],
        conversation: Optional[Sequence[tuple[str, str]]] = None,
        location_meta: Optional[dict] = None,
    ):
        if hasattr(self._provider, "generate_stream"):
            async for token in self._provider.generate_stream(
                question, context, conversation, location_meta=location_meta
            ):
                yield token
        else:
            result = await self.generate_response(
                question, context, conversation, location_meta=location_meta
            )
            yield result.answer

