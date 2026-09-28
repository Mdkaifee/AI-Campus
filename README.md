# DAVIET Smart Campus AI Assistant — Phase 1

A verified, college-specific conversational AI assistant for **DAV Institute of Engineering & Technology (DAVIET), Jalandhar** (Website: [https://davietjal.org](https://davietjal.org)).

This system forms Phase 1 of the **“Smart Campus AI Assistant – AI-Based Campus Information and Navigation System”**. In this phase, the chatbot answers student inquiries grounded strictly in verified college data using a Retrieval-Augmented Generation (RAG) architecture, ensuring that the AI never hallucinates or fabricates DAVIET facts.

---

## 1. Project Overview

The DAVIET Smart Campus AI Assistant provides instant, accurate answers to questions regarding:
- **Institute Overview & Mission:** Campus background, approvals (AICTE, PTU), accreditations, and address.
- **Departments & Academic Programmes:** Engineering (CSE, CSE AI & ML, ECE, EE, ME, CE), Management, and Applied Sciences.
- **Admissions & Intake:** Annual intake, eligibility guidelines, and links to official prospectus.
- **Central Library:** Timings, circulation hours, e-resources, and membership rules.
- **Hostel Facilities:** Sutlej, Beas, and Raavi Hostels, mess facilities, amenities, and security.
- **Training & Placement Office (TPO):** Placement drives, coordinators, recruiter interface, and contact numbers.
- **Student Services & Grievances:** Grievance redressal procedure, suggestion boxes, and official emails.
- **Committees & Contacts:** Anti-ragging committee, internal complaints committee, and helpline numbers.

---

## 2. Core Architectural Principle

> **"The AI is the conversational layer, not the source of truth."**

For all DAVIET inquiries, the workflow strictly enforces:
```text
User Question
      ↓
Query Pre-processing & Keyword/Alias Expansion
      ↓
Knowledge Retrieval (DAVIET Knowledge Base)
      ↓
Relevant Verified Context
      ↓
AI Response Generation (Ollama / Local LLM)
      ↓
Final Grounded Answer with Official Sources
```
If information is not found in the verified knowledge base, the assistant explicitly directs the user to the official website rather than guessing.

---

## 3. Technology Stack

- **Frontend:**
  - React 19 + Vite
  - Vanilla CSS with modern styling (Outfit & Inter typography, responsive sidebar, glassmorphic suggestion cards, mobile drawer)
  - Modular React components (`ChatWindow`, `MessageBubble`, `ChatInput`, `SessionSidebar`, `SourceLinks`)
- **Backend:**
  - Python 3.11+ / FastAPI
  - Pydantic v2 schemas for request/response validation
  - Uvicorn ASGI server
  - Asynchronous Motor MongoDB client
- **AI Engine:**
  - Ollama (`llama3.2`) with configurable provider abstraction
  - Support for local or cloud LLM endpoints via environment configuration
- **Database:**
  - MongoDB Atlas (or local MongoDB) for chat history, sessions, error audits, and future location data

---

## 4. Folder Structure

```text
Smart-Campus-AI/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── chat.py             # Chat, session history endpoints
│   │   │   │   └── health.py           # API and DB health checks
│   │   │   └── dependencies.py        # Dependency injection
│   │   ├── core/
│   │   │   ├── config.py              # Settings from environment
│   │   │   └── logging.py             # Structured logging
│   │   ├── database/
│   │   │   └── mongodb.py             # Motor async connection & indexes
│   │   ├── models/
│   │   │   ├── chat.py                # Chat turn & source models
│   │   │   ├── knowledge.py           # Knowledge item domain model
│   │   │   └── location.py            # Phase 2 CampusLocation model
│   │   ├── repositories/
│   │   │   ├── chat_repository.py     # MongoDB chat persistence
│   │   │   ├── knowledge_repository.py# File-backed knowledge loader
│   │   │   └── error_audit_repository.py
│   │   ├── schemas/
│   │   │   ├── chat.py                # Pydantic chat request/response
│   │   │   ├── location.py            # Phase 2 CampusLocation schema
│   │   │   └── response.py            # Health schema
│   │   ├── services/
│   │   │   ├── ai_service.py          # Provider-agnostic AI layer (Ollama)
│   │   │   ├── chat_service.py        # Chat orchestration
│   │   │   └── retrieval_service.py   # Keyword & alias retrieval
│   │   └── main.py                    # FastAPI application entrypoint
│   ├── requirements.txt
│   ├── .env.example
│   └── tests/
│       ├── test_chat.py
│       ├── test_health.py
│       └── test_retrieval.py
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Chat/                  # ChatHeader, ChatWindow, EmptyState
│   │   │   ├── Input/                 # ChatInput
│   │   │   ├── Message/               # MessageBubble, SourceLinks
│   │   │   ├── Sidebar/               # SessionSidebar
│   │   │   └── UI/                    # ErrorBanner, LoadingDots
│   │   ├── hooks/
│   │   │   └── useChat.js             # Chat state & session persistence
│   │   ├── pages/
│   │   │   └── ChatPage.jsx           # Main chat layout
│   │   ├── services/
│   │   │   └── api.js                 # Backend API client
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── data/
│   └── daviet/                        # 11 Verified Knowledge Base categories
│       ├── academics.json
│       ├── admissions.json
│       ├── committees.json
│       ├── contacts.json
│       ├── departments.json
│       ├── hostels.json
│       ├── infrastructure.json
│       ├── institute.json
│       ├── library.json
│       ├── placements.json
│       └── student_services.json
│
├── .tools-path.sh                     # Helper script to export local Node & Ollama paths
├── .gitignore
└── README.md
```

---

## 5. Environment Variables

### Backend Configuration (`backend/.env`)

```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.jqexyje.mongodb.net/Campus_AI?appName=Cluster0
DATABASE_NAME=Campus_AI
CORS_ORIGINS=http://localhost:5173

# AI Provider Settings
AI_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.2
AI_TIMEOUT_SECONDS=60

# Optional cloud AI settings
AI_API_KEY=
AI_MODEL=

# Collections
KNOWLEDGE_BASE_DIR=../data/daviet
CHAT_HISTORY_COLLECTION=chat_history
ERROR_AUDIT_COLLECTION=error_audit
KNOWLEDGE_COLLECTION=knowledge_items
LOG_LEVEL=INFO
```

### Frontend Configuration (`frontend/.env`)

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## 6. Running Locally

### Step 1: Start Ollama (AI Model)
Ensure Ollama is running with the `llama3.2` model:
```bash
# If using project-local binary paths:
source .tools-path.sh

# Start Ollama server (in background or separate terminal)
ollama serve

# Pull model if not already present
ollama pull llama3.2
```

### Step 2: Start the FastAPI Backend
```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
The backend API will be available at [http://localhost:8000](http://localhost:8000).  
Interactive Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs).

### Step 3: Start the React Frontend
In a new terminal:
```bash
# If using project-local Node/NPM:
source .tools-path.sh

cd frontend
npm install
npm run dev -- --host 0.0.0.0 --port 5173
```
Open your browser at [http://localhost:5173](http://localhost:5173).

---

## 7. API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Health status and MongoDB ping |
| `POST` | `/api/chat` | Send student question and get grounded answer |
| `GET` | `/api/chat/sessions` | List previous chat sessions |
| `GET` | `/api/chat/sessions/{id}` | Get full conversation turns for a session |

### Sample Chat Request:
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What are the library timings?", "session_id": "optional-session-id"}'
```

### Sample Chat Response:
```json
{
  "session_id": "optional-session-id",
  "answer": "The library timings at DAVIET Central Library are:\n\n• Monday to Friday: 8:00 AM to 6:30 PM\n• Saturday: 8:00 AM to 4:25 PM\n• Closed on Sundays and gazetted holidays\n\nPlease confirm on the official website for current holiday schedules.",
  "sources": [
    {
      "title": "Central Library",
      "url": "https://davietjal.org/infrastructure/central-library/",
      "category": "library",
      "updated_at": "2026-09-26"
    }
  ],
  "unavailable": false
}
```

---

## 8. Testing

Run backend tests using `pytest`:
```bash
cd backend
source .venv/bin/activate
pytest -v
```
All 18 tests cover:
- Retrieval matching & ranking
- Alias handling (e.g. `TPO` → Training and Placement)
- Out-of-domain query handling (no hallucinations)
- Session persistence & error resilience
- Health checks & CORS parsing

Run frontend linting:
```bash
cd frontend
npm run lint
npm run build
```

---

## 9. Future Phase 2 Integration (Campus Location Assistance)

The project architecture is deliberately prepared for Phase 2:
- **Domain Model:** [`CampusLocation`](file:///Users/rajnandni/Smart-Campus-AI/backend/app/models/location.py) defines destinations with `block`, `floor`, `description`, `latitude`, `longitude`, `maps_url`, and `aliases`.
- **Database Schema:** MongoDB already has indexes created on `campus_locations` (`name`, `aliases`).
- **Pydantic Schemas:** [`CampusLocationResponse`](file:///Users/rajnandni/Smart-Campus-AI/backend/app/schemas/location.py) is ready for navigation endpoints.
- **Pipeline Extensibility:** An intent classification step can seamlessly branch location queries to `LocationRepository` without touching Phase 1 knowledge retrieval.
