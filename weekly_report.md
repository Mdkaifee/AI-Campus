# Weekly Project Report

## Project Title

**DAVIET Smart Campus AI Assistant**

## Student Details

**Submitted by:** Rajnandni  
**Program:** B.Tech, 7th Semester  
**Course/Branch:** Electronics and Communication Engineering (ECE)  
**University Roll No.:** 2301763
**Class Roll No.:** 37/23  
**Submitted to:** Love Kumar Sir  
**Project Start Date:** 25 July 2026  
**Report Type:** Weekly Project Progress Report

## Project Summary

The DAVIET Smart Campus AI Assistant is a full-stack web application designed to help students, visitors, and staff get instant, verified information about DAV Institute of Engineering and Technology, Jalandhar. The system combines a modern React frontend, a FastAPI backend, MongoDB-based persistence, campus-specific knowledge retrieval, AI-generated responses, user authentication, chat history, source references, and campus navigation support.

The application works as a smart digital campus helpdesk. Users can ask questions about admissions, courses, departments, fee structure, placements, hostels, library timings, working hours, campus contacts, committees, student services, and campus locations. Instead of giving random or unsupported answers, the backend first retrieves verified DAVIET information and then uses an AI model to generate a clear student-friendly response.

The project has also been deployed online:

- Frontend live URL: https://ai-campus-147j.onrender.com/
- Backend live URL: https://daviet-ai-campus-backend.onrender.com

## Main Objective

The main objective of this project is to create an AI-powered campus assistant that provides fast, reliable, and easy-to-understand answers for DAVIET-related queries. The application reduces the need to manually search multiple college pages or documents by presenting relevant information through a conversational interface.

The system is built with the principle that the AI should act as a communication layer, while verified college data remains the source of truth.

## Project Need and Motivation

Students usually need information from many different sources during daily campus life. A student may want to know about admission rules, course details, fee structure, library timings, hostel facilities, training and placement contacts, faculty departments, college working hours, or the location of a campus block. This information is often available on official websites, notices, departments, or administrative sources, but searching it manually takes time.

The motivation behind this project is to create one intelligent interface where students can ask questions in normal language and receive relevant answers quickly. The project is especially useful because it does not only depend on a general AI model. It uses a verified DAVIET knowledge base and then generates answers from that context. This makes the system more reliable for college-specific information.

Another important motivation is improving accessibility. New students, visitors, and even existing students may not know exact department names, abbreviations, or official terminology. The assistant supports informal words, short forms, and typos, making it easier to use in real situations.

## Project Scope

The scope of the project includes designing and developing a complete full-stack AI assistant for DAVIET. The frontend provides a polished user interface for students. The backend handles authentication, chat processing, retrieval, AI response generation, database storage, and API endpoints. MongoDB is used as the online database for storing user accounts, chat sessions, and related data.

The current scope includes:

- A public landing page for DAVIET Smart Campus Portal.
- Guest chat access without login.
- Student signup and login.
- Private chat history for authenticated users.
- AI-based campus question answering.
- Verified knowledge retrieval.
- Source-based responses.
- Campus location assistance.
- Online MongoDB database setup.
- Backend deployment.
- Frontend deployment.
- Environment configuration for production and local development.

The project can be extended in the future with admin controls, more campus data, voice support, multilingual support, and advanced navigation.

## Development Timeline

The project work started on **25 July 2026**. The development was carried out step by step, beginning with planning and gradually moving toward frontend design, backend APIs, database integration, AI integration, and deployment.

### Phase 1: Planning and Requirement Understanding

In the initial phase, the main problem statement was identified: students need a single assistant that can answer DAVIET-related questions. The required features were planned, including campus information, admissions, departments, placements, library, hostels, contacts, and navigation. The decision was made to build a full-stack application rather than only a simple chatbot.

During this phase, the technology stack was also selected. React and Vite were selected for the frontend because they provide fast development and a modern UI structure. FastAPI was selected for the backend because it is lightweight, fast, and suitable for API-based applications. MongoDB was selected because it can store flexible JSON-like documents such as users, chat turns, sources, and location objects.

### Phase 2: Frontend Design and Layout

After planning, the frontend structure was developed. The landing page was created to give the application a proper identity as the DAVIET Smart Campus Portal. The landing page includes DAVIET branding, quick topic cards, call-to-action buttons, theme toggle, user profile state, and a floating chat button.

The chat page was then developed with a clean layout containing a header, sidebar, message area, input box, loading states, and error display. The interface was designed to be useful for both guest users and logged-in students.

### Phase 3: Backend API Development

The backend was built using FastAPI. Separate API routes were created for authentication, chat, streaming chat, session management, and health checks. Pydantic schemas were used for request and response validation. The backend was structured into services and repositories so that each part of the application has a clear responsibility.

The backend does not directly generate random AI answers. It first retrieves relevant DAVIET information and then sends that verified context to the AI provider. This improves the reliability of answers.

### Phase 4: MongoDB Online Database Setup

MongoDB was configured as the online database for the project. The database is used to store user accounts, chat history, chat sessions, dynamic knowledge items, campus locations, and error audit data. Environment variables were used to connect the backend with MongoDB securely.

Indexes were also added for important collections so that chat history, knowledge items, and campus locations can be accessed efficiently. The online database setup was important because the deployed backend and frontend need persistent data storage.

### Phase 5: AI and Retrieval Integration

The retrieval system was implemented to search verified DAVIET knowledge before generating an answer. This includes keyword search, category matching, alias expansion, typo tolerance, and conversation context handling.

The AI service was made provider-flexible so the project can work with local or cloud AI providers. The AI prompt includes verified context, conversation history, current campus time, and optional location metadata.

### Phase 6: Deployment

After local development and environment setup, both frontend and backend were deployed on Render. The backend was deployed as a FastAPI service and the frontend was deployed as a Vite static site. The deployed frontend was configured to communicate with the deployed backend API. MongoDB online database was connected to the deployed backend.

Current deployed links:

- Frontend: https://ai-campus-147j.onrender.com/
- Backend: https://daviet-ai-campus-backend.onrender.com

## Week-Wise Progress Report

The project work started on **25 July 2026** and the current report is prepared up to **28 September 2026**. The progress has been divided week-wise to show how the application gradually moved from planning to full-stack development and deployment.

### Week 1: 25 July 2026 to 31 July 2026

During the first week, the project idea was finalized and the main objective was defined. The problem statement was studied: students need a single smart assistant that can answer DAVIET-related questions quickly and reliably.

Work completed during this week:

- Finalized the project topic: DAVIET Smart Campus AI Assistant.
- Identified the main users of the system, including students, visitors, and staff.
- Listed major information areas such as admissions, departments, fees, library, hostels, placements, contacts, working hours, and campus locations.
- Decided that the application should be a complete full-stack web app instead of only a basic chatbot.
- Selected the initial technology stack: React for frontend, FastAPI for backend, MongoDB for database, and AI-based response generation.
- Planned the project architecture with separate frontend, backend, database, and AI layers.

### Week 2: 1 August 2026 to 7 August 2026

In the second week, the basic project structure was prepared. Separate folders and development responsibilities were planned for frontend, backend, and data. The focus was on setting up the foundation so that future features could be added cleanly.

Work completed during this week:

- Created the initial project structure.
- Planned separate frontend and backend modules.
- Set up React and Vite for frontend development.
- Set up FastAPI structure for backend development.
- Created basic configuration files.
- Planned environment variable usage for local and production setup.
- Started collecting DAVIET-related information categories for the knowledge base.

### Week 3: 8 August 2026 to 14 August 2026

The third week focused mainly on frontend development. The landing page concept was created to give the project a professional first screen. DAVIET branding, navigation, and student-friendly topic cards were planned and implemented.

Work completed during this week:

- Developed the initial landing page layout.
- Added DAVIET Smart Campus Portal branding.
- Added hero section and call-to-action buttons.
- Added quick topic cards for common student queries.
- Added official portal link.
- Added visual design improvements for a clean and modern interface.
- Started planning the chat page layout.

### Week 4: 15 August 2026 to 21 August 2026

During the fourth week, the chat interface was developed. The main goal was to create a usable interface where students can ask questions and view assistant responses clearly.

Work completed during this week:

- Created the chat page layout.
- Added chat header, message window, and input area.
- Designed user and assistant message bubbles.
- Added loading state for assistant responses.
- Added error banner support.
- Added copy response functionality.
- Added sidebar layout for chat sessions.
- Improved responsive behavior for smaller screens.

### Week 5: 22 August 2026 to 28 August 2026

The fifth week focused on backend APIs and core backend structure. FastAPI routes and schemas were developed for chat, health checks, and structured responses.

Work completed during this week:

- Created FastAPI backend application entry point.
- Added CORS configuration for frontend-backend communication.
- Added health check endpoint.
- Created chat request and response schemas.
- Created initial chat API route.
- Structured backend folders into routes, services, repositories, schemas, models, and core configuration.
- Added input validation for chat messages.

### Week 6: 29 August 2026 to 4 September 2026

During the sixth week, the verified knowledge base and retrieval system were implemented. This was one of the most important parts of the project because the assistant needed to answer from DAVIET-specific information.

Work completed during this week:

- Created DAVIET knowledge base JSON files.
- Added categories such as academics, admissions, contacts, departments, hostels, infrastructure, library, placements, student services, committees, and working hours.
- Developed knowledge repository to load JSON data.
- Implemented retrieval service for searching relevant knowledge.
- Added keyword matching, category matching, title matching, and content matching.
- Added alias expansion for common student terms.
- Added typo tolerance for queries like `librari`, `ug blok`, and `audi`.

### Week 7: 5 September 2026 to 11 September 2026

The seventh week focused on AI integration and grounded answer generation. The backend was improved so the AI receives verified context before generating a response.

Work completed during this week:

- Developed AI service layer.
- Added support for configurable AI providers.
- Added prompt structure for DAVIET Smart Campus Assistant.
- Passed retrieved DAVIET context to the AI model.
- Added recent conversation history into the AI prompt.
- Added fallback messages for unknown DAVIET queries.
- Added off-topic query handling.
- Added greeting response handling.
- Improved answer safety by avoiding unsupported DAVIET facts.

### Week 8: 12 September 2026 to 18 September 2026

During the eighth week, authentication, session history, and MongoDB integration were developed. This converted the project from a simple chat app into a user-based system with persistent data.

Work completed during this week:

- Set up MongoDB online database.
- Added backend MongoDB connection using Motor.
- Added database health check.
- Created user signup and login APIs.
- Added password hashing with salt.
- Added token-based authentication.
- Added frontend auth modal for login and signup.
- Added authenticated user state in frontend.
- Added private chat history for logged-in users.
- Added chat session listing, loading, and deletion.
- Added guest mode with browser session storage.

### Week 9: 19 September 2026 to 25 September 2026

The ninth week focused on advanced assistant features, location support, streaming responses, and UI improvements.

Work completed during this week:

- Added Server-Sent Events streaming for AI responses.
- Updated frontend to display answers token by token.
- Added campus location detection service.
- Added campus destinations such as Central Library, TPO, Auditorium, R and D Block, Core Block, hostels, and canteen.
- Added fuzzy matching for campus location queries.
- Added location card component on frontend.
- Added embedded Google Maps and open-in-map functionality.
- Added source links under assistant responses.
- Added dynamic fee and IKG-PTU knowledge catalog.
- Improved sidebar behavior and session handling.

### Week 10: 26 September 2026 to 28 September 2026

The final report period focused on production readiness, deployment, environment setup, and documentation. Both frontend and backend were deployed online and connected with the online MongoDB database.

Work completed during this period:

- Configured backend environment variables for production.
- Configured frontend API URL for deployed backend.
- Connected backend with online MongoDB database.
- Deployed backend API on Render.
- Deployed frontend application on Render.
- Connected deployed frontend with deployed backend.
- Verified deployed URLs.
- Checked local and production environment configuration.
- Updated project report with features, deployment links, database setup, and week-wise progress.
- Prepared documentation for final weekly report submission.

Live deployment links:

- Frontend: https://ai-campus-147j.onrender.com/
- Backend: https://daviet-ai-campus-backend.onrender.com

## Major Features Implemented

### 1. Smart Landing Page

The application includes a complete landing page for DAVIET Smart Campus Portal. It introduces the institute and gives users a professional first interaction with the product.

Key features of the landing page include:

- DAVIET branding with institute name and Smart Campus Portal identity.
- Hero section with DAVIET campus visual.
- Clear call-to-action buttons for opening the AI assistant.
- Light and dark theme toggle.
- Navigation links for Academics, Facilities, About, and Official Portal.
- Official DAVIET website external link.
- Quick statistics such as years of excellence, engineering streams, auditorium capacity, and AI assistance availability.
- Floating chat button for quick access to the AI assistant.
- User-aware welcome message when a student is logged in.

### 2. Topic-Based Quick Explore Cards

The landing page provides clickable topic cards that help users start meaningful queries quickly.

Implemented topic cards include:

- Academics and Courses.
- Fee Structure.
- Campus Navigation.
- Departments and Labs.
- Hostels and Mess.
- Admissions.
- Hours and Timetable.
- Contacts and Helpline.

Each card contains a title, short description, icon, and predefined prompt. When a user clicks a card, the app opens the chat page and automatically sends the related question to the assistant.

### 3. AI Chat Interface

The core feature of the application is the chat interface. Users can ask natural language questions and receive structured answers from the DAVIET Campus AI.

Chat features include:

- User and assistant message bubbles.
- Real-time answer streaming.
- Blinking cursor while the assistant is responding.
- Copy button for assistant responses.
- Bullet-point rendering for structured AI answers.
- Loading states while responses are being generated.
- Error banner for user-friendly failure messages.
- New chat button.
- Sidebar for previous sessions.
- Mobile-friendly sidebar overlay.
- Back-to-home navigation.
- Theme toggle inside the chat page.

### 4. Streaming AI Responses

The frontend and backend support Server-Sent Events streaming for chat responses. This makes the assistant feel faster because the answer appears token by token instead of waiting for the full response.

Streaming includes:

- Metadata event containing session ID, sources, and location details.
- Token events for incremental assistant response.
- Done event when generation is complete.
- Frontend state updates as tokens arrive.
- Automatic fallback handling if streaming fails.

### 5. Guest Mode

The application supports guest access. A user can use the chat assistant without creating an account.

Guest mode features include:

- Guest users can ask questions immediately.
- Guest sessions are stored in browser session storage.
- Guest chat history is tab-scoped to avoid unnecessary cross-tab leakage.
- Guest sessions can be loaded and deleted from the sidebar.
- Guest history is not shared globally or saved as authenticated user history.

### 6. Student Authentication

The application includes a student authentication system with signup, login, logout, and profile verification.

Authentication features include:

- Sign up with full name, email, and password.
- Login with email and password.
- Password confirmation during signup.
- Password visibility toggle.
- Form validation for email, name, password length, and password match.
- Loading state during authentication requests.
- Error messages for failed login or signup.
- Auth token stored in local storage.
- Current user profile check through `/api/auth/me`.
- Logout support.
- User profile display in the landing page navbar.

### 7. Secure Password Handling

The backend hashes user passwords before storing them. The implementation uses PBKDF2-HMAC-SHA256 with salt and multiple iterations. This means raw passwords are not stored directly.

The authentication service also generates signed access tokens for logged-in users. These tokens are used by the frontend to access private chat history and authenticated API endpoints.

### 8. Private Chat History for Logged-In Users

Authenticated users get persistent chat history stored in MongoDB.

Chat history features include:

- Every chat turn stores user message, assistant response, sources, location data, provider, model, session ID, and user email.
- Sessions are isolated by user email.
- A logged-in user can only access their own sessions.
- Sidebar lists recent sessions.
- Each session has a title based on the first user message.
- Sessions are sorted by last updated time.
- Users can load old conversations.
- Users can delete old sessions.
- Recent turns are loaded into context so follow-up questions work better.

### 9. Verified Knowledge Base

The assistant uses a local DAVIET knowledge base stored in JSON files. This prevents the AI from depending only on model memory.

Current knowledge categories include:

- Academics.
- Admissions.
- Committees.
- Contacts.
- Departments.
- Hostels.
- Infrastructure.
- Institute information.
- Library.
- Placements.
- Student services.
- Working hours.

The repository currently contains 12 JSON files with verified DAVIET-related knowledge entries. These files are loaded by the backend and converted into searchable knowledge items.

### 10. Retrieval-Augmented Generation

The backend follows a retrieval-first architecture. When a student asks a question, the system searches the DAVIET knowledge base before generating an answer.

The retrieval process includes:

- Query normalization.
- Stopword removal.
- Keyword matching.
- Category matching.
- Title matching.
- Content matching.
- Alias expansion.
- Typo tolerance.
- Ranking of relevant knowledge items.
- Limiting the final context to the most relevant entries.

This improves accuracy because the AI receives verified context before answering.

### 11. Alias and Typo Handling

The retrieval service supports student-friendly abbreviations, typos, and informal queries.

Examples supported by the system include:

- `tpo` mapped to Training and Placement Office.
- `lib` and `librari` mapped to library.
- `ug blok` mapped to Core Block.
- `audi` mapped to auditorium.
- `fee struct` mapped to fee structure.
- `ikgptu` mapped to IKG-PTU.
- `cse`, `ece`, `mech`, `ee`, and other department abbreviations.
- `open rn` and `open now` mapped to working hours.

This makes the assistant easier for real students to use because they do not need to type perfect official terms.

### 12. Conversational Context Support

The backend uses recent conversation turns to improve follow-up responses. For example, if the previous question was about campus locations and the next message is only "library" or "auditorium", the assistant can treat it as a location follow-up.

Context support includes:

- Loading the latest turns from the same session.
- Passing recent user and assistant messages to the AI provider.
- Expanding short queries with previous context.
- Avoiding false off-topic detection when the conversation is already DAVIET-related.

### 13. Campus Navigation and Location Assistance

The application includes campus location support for major DAVIET places. When a user asks about a location, the backend matches the destination and the frontend renders a location card.

Supported campus destinations include:

- Central Library / Knowledge Centre.
- Training and Placement Office.
- Lala Chanchal Dass DAVIET Auditorium.
- R and D Block.
- Core Block.
- Material Science Block.
- Sutlej Boys Hostel.
- Raavi Girls Hostel.
- Beas Hostel.
- Campus Canteen and Cafeteria.

Each location can include:

- Name.
- Aliases.
- Block or building.
- Floor.
- Description.
- Latitude and longitude.
- Google Maps search link.
- Embedded map link.

### 14. Interactive Location Cards

The frontend displays campus navigation results using a dedicated location card component.

Location card features include:

- Destination name.
- Block badge.
- Floor badge.
- Short location description.
- Embedded Google Map iframe.
- Show or hide map toggle.
- Open in Google Maps link.

This makes location-related responses more visual and useful than plain text.

### 15. Dynamic Knowledge for Fees and PTU Information

The backend includes a dynamic knowledge catalog for information that may change more often, such as fee structure and IKG-PTU affiliation details.

Dynamic catalog features include:

- B.Tech and academic fee structure information.
- Hostel and mess charge guidance.
- IKG-PTU affiliation and academic regulation information.
- Scholarship and academic calendar related context.
- Syncing verified dynamic items into MongoDB when the database is available.
- Query-time matching for fee, tuition, PTU, charges, cost, and scholarship terms.

### 16. AI Provider Flexibility

The backend has a provider-agnostic AI service. This allows the project to work with different AI providers through environment configuration.

Supported provider styles include:

- Local Ollama model.
- OpenAI-compatible cloud providers.
- Native Gemini API style through Google Generative Language endpoint.
- Native Anthropic Claude style.

This makes the system flexible for both local development and cloud deployment.

### 17. Grounded Answer Generation

The AI receives a carefully built prompt containing:

- System role as DAVIET Smart Campus AI Assistant.
- Current local campus time in IST.
- Live campus operating status.
- Verified DAVIET context from retrieval.
- Recent conversation history.
- Optional campus location metadata.
- Student question.

The assistant is instructed to answer naturally while staying grounded in the verified DAVIET context.

### 18. Live Campus Time Awareness

The backend calculates current DAVIET local time using Indian Standard Time. It adds campus operating status to the AI prompt.

This helps answer questions like:

- Is college open now?
- What are the working hours?
- Is the library open today?
- What happens on Saturday or Sunday?

The system distinguishes between weekdays, after-hours, Saturdays, Sundays, academic class timings, administrative office status, and hostels being available 24/7.

### 19. Fallback and Safety Behavior

The assistant is designed to avoid hallucinated DAVIET facts.

Fallback behavior includes:

- Greeting responses handled directly without calling AI.
- Unknown DAVIET questions return a safe message directing users to official DAVIET sources.
- Off-topic questions are redirected back to DAVIET-related help.
- If AI generation fails but retrieved context exists, the backend returns verified knowledge directly.
- If AI fails for a location question, the backend returns location details directly.
- AI provider failures are recorded in error audit storage when available.

### 20. Source Links

Assistant responses can include source links. The frontend displays sources after the streamed answer finishes.

Source link data includes:

- Source title.
- Source URL.
- Category.
- Last updated date when available.

This improves trust because users can verify answers from the referenced source.

### 21. API Endpoints

The backend exposes a clean FastAPI API.

Implemented endpoints include:

- `POST /api/auth/signup` for student registration.
- `POST /api/auth/login` for student login.
- `GET /api/auth/me` for checking the current user profile.
- `POST /api/chat` for normal chat response.
- `POST /api/chat/stream` for streaming chat response.
- `GET /api/chat/sessions` for listing authenticated user sessions.
- `GET /api/chat/sessions/{session_id}` for loading one session.
- `DELETE /api/chat/sessions/{session_id}` for deleting one session.
- `GET /api/health` for API and MongoDB health status.

### 22. Health Monitoring

The health endpoint checks whether the backend process is running and whether MongoDB is available.

Health responses can show:

- `ok` when the database is connected.
- `degraded` when the API is running but MongoDB is unavailable.

This allows the frontend or developer to quickly understand whether the app is fully operational or partially degraded.

### 23. MongoDB Integration

The backend uses MongoDB through the async Motor client.

MongoDB is used for:

- User accounts.
- Chat history.
- Chat sessions.
- Error audit records.
- Dynamic knowledge items.
- Campus locations.

The app creates useful indexes for:

- Chat session ID.
- Chat creation time.
- Knowledge category.
- Knowledge updated time.
- Knowledge keywords.
- Error audit timestamp.
- Error audit type.
- Campus location name.
- Campus location aliases.

### 24. Database Degraded Mode

The backend is built to keep the API running even if MongoDB is unavailable at startup.

In degraded mode:

- The API still starts.
- Health check reports database unavailable.
- Chat can still answer from local knowledge where possible.
- Chat history may not save.
- Auth service can temporarily use in-memory fallback for users.
- Error handling avoids crashing the whole app.

This improves reliability during local development and deployment issues.

### 25. Frontend API Client

The frontend includes a centralized API service.

It handles:

- Base API URL configuration through `VITE_API_BASE_URL`.
- Default local backend URL fallback.
- JSON request headers.
- Authorization bearer token injection.
- Signup, login, and profile requests.
- Chat requests.
- Streaming chat requests.
- Session list, load, and delete requests.
- Health check requests.
- Friendly error messages from backend responses.

### 26. Theme Support

The application supports light and dark themes.

Theme features include:

- Theme stored in local storage.
- Theme applied to the document root through `data-theme`.
- Toggle available on landing page and chat page.
- Persistent preference across reloads.

### 27. Responsive and User-Friendly UI

The frontend is designed with a polished student-facing interface.

UI features include:

- Professional landing page layout.
- Responsive chat shell.
- Sidebar for conversation history.
- Mobile drawer behavior.
- Clear icon usage through Lucide React.
- Campus-themed visual assets.
- Error banners.
- Loading dots.
- Copy response button.
- Floating assistant button.
- Auth modal with tabs.
- Accessible button labels for important actions.

### 28. Input Validation

Both frontend and backend perform validation.

Validation examples include:

- Empty chat messages are rejected.
- Chat messages above 4000 characters are rejected.
- Empty email or password is rejected.
- Signup requires name of minimum length.
- Signup requires password of minimum length.
- Signup requires matching confirmation password.
- Invalid session IDs are rejected.

### 29. Environment-Based Configuration

The backend is configured through environment variables.

Important configuration values include:

- MongoDB URI.
- Database name.
- CORS origins.
- AI provider.
- AI model.
- AI API key.
- AI timeout.
- Knowledge base directory.
- Collection names.
- Log level.

The frontend can be configured with:

- `VITE_API_BASE_URL` for backend API URL.

This makes the same project suitable for local development and deployment.

### 30. Deployment Readiness

The project includes Render deployment configuration and has been successfully deployed.

Deployment setup includes:

- Backend service with FastAPI and Uvicorn.
- Frontend static service with Vite build output.
- Environment variables for backend and frontend.
- Configurable production database URI.
- Configurable frontend API base URL.

Live deployment links:

- Frontend: https://ai-campus-147j.onrender.com/
- Backend: https://daviet-ai-campus-backend.onrender.com

## Technical Architecture

The project follows a clear full-stack structure:

- React frontend handles user interface, routing, auth modal, chat UI, sessions, and streaming display.
- FastAPI backend handles API routes, validation, retrieval, AI generation, authentication, database access, and health checks.
- MongoDB stores users, chat history, sessions, dynamic knowledge, and audit data.
- JSON knowledge files provide verified DAVIET information.
- AI providers generate natural responses using retrieved context.

## Detailed System Design

The system has been designed using a modular architecture. Each major responsibility is separated into a different layer. This makes the project easier to maintain, test, debug, and extend in the future.

### Frontend Layer

The frontend layer is responsible for the complete user experience. It manages page navigation, theme switching, authentication modal, chat interface, API calls, streaming response handling, session sidebar, guest session storage, and rendering of sources and location cards.

The frontend does not directly access the database. It communicates only with the backend API. This keeps the application secure and organized because database logic remains on the server side.

The frontend also improves usability by showing loading indicators, friendly error messages, response copy buttons, and structured answer formatting. These details make the assistant feel like a complete application rather than a basic chatbot.

### Backend Layer

The backend layer is the main decision-making part of the application. It receives requests from the frontend, validates the input, checks authentication, retrieves relevant data, calls the AI provider, saves chat history, and returns structured responses.

The backend is divided into API routes, services, repositories, schemas, models, and core configuration. This separation helps keep the code clean. For example, API routes handle HTTP requests, services handle business logic, and repositories handle database or knowledge access.

### Database Layer

MongoDB is used as the database layer. It stores data in flexible document format, which is suitable for chat applications because each chat turn may include text, sources, location objects, provider details, timestamps, and user information.

The online MongoDB setup allows the deployed application to save and retrieve user data even after redeployment or server restart. This is important for persistent login and private chat history.

### AI and Retrieval Layer

The AI and retrieval layer is the intelligence part of the application. The retrieval service searches verified DAVIET knowledge and selects the most relevant context. The AI service then generates a natural answer using that context.

This design is better than sending the question directly to an AI model because it reduces hallucination. The model receives factual DAVIET data before answering.

## Database Design

The database design supports users, chat history, sessions, knowledge, locations, and audits.

### Users Collection

The users collection stores student account information. It includes user ID, name, email, hashed password, salt, and account creation date. Passwords are stored in hashed form rather than plain text.

### Chat History Collection

The chat history collection stores each conversation turn. Each record can include:

- Session ID.
- User email.
- User message.
- Assistant response.
- Response sources.
- Location object if available.
- AI provider.
- AI model.
- Creation timestamp.

This structure allows the application to reconstruct a full conversation when a user opens an old session.

### Knowledge Collection

The knowledge collection is used for dynamic knowledge items such as fee and PTU information. This allows important frequently changing information to be stored online and used during retrieval.

### Campus Locations Collection

The campus locations collection stores verified campus destination details. These include destination name, aliases, block, floor, description, and map coordinates. The location service can use this information for navigation-related queries.

### Error Audit Collection

The error audit collection stores backend failure details such as AI provider failure, database read failure, or database write failure. This helps in debugging and improving reliability.

## Frontend Implementation Details

The frontend implementation was a major part of the project. The goal was to build an interface that feels simple for students while still supporting advanced features like authentication, streaming, chat history, and map cards.

### Landing Page Implementation

The landing page acts as the entry point of the application. It uses DAVIET branding and presents the assistant as a Smart Campus Portal. It includes navigation links, quick topic cards, user authentication controls, theme toggle, and a floating chat button.

The quick topic cards were designed to reduce user effort. Instead of thinking about how to phrase a question, a user can click a topic such as Fee Structure or Campus Navigation and the app automatically starts a relevant chat prompt.

### Chat Page Implementation

The chat page is designed as the main working area of the assistant. It includes a session sidebar, chat header, message window, error banner, and input box. The chat page receives an initial prompt from the landing page when a topic card is clicked.

When a message is sent, the frontend immediately displays the user message, starts loading, and then updates the assistant response as streaming tokens arrive from the backend.

### Authentication Modal Implementation

The authentication modal supports both login and signup in the same component. It includes tabs for switching modes, validation messages, password visibility toggle, loading state, and error handling.

After successful login or signup, the frontend stores the auth token and updates the user state. The landing page then shows the logged-in user's profile instead of login buttons.

### Session Sidebar Implementation

The session sidebar displays previous chat sessions. For logged-in users, sessions are loaded from the backend. For guest users, sessions are loaded from browser session storage.

The sidebar allows users to:

- Start a new chat.
- Open an existing chat.
- Delete a chat session.
- View recent session titles.
- Continue previous conversations.

### Streaming Implementation

The frontend uses the browser fetch API and reads the response stream. It decodes Server-Sent Events from the backend and handles metadata, token, and done events.

This gives the user a real-time experience where the answer appears gradually. It also allows sources and location data to be attached to the response.

## Backend Implementation Details

The backend implementation was developed to support reliability, modularity, and verified answers.

### FastAPI Application Setup

FastAPI was used to create the backend application. The app includes CORS middleware so the deployed frontend can communicate with the deployed backend. During startup, the backend attempts to connect to MongoDB, create indexes, sync dynamic knowledge, and sync campus locations.

If MongoDB is unavailable, the backend does not crash. Instead, it starts in degraded mode so health checks and local knowledge-based responses can still work.

### Authentication Service

The authentication service handles signup, login, token creation, and token verification. During signup, the password is salted and hashed before storage. During login, the entered password is hashed again and compared with the stored hash.

Tokens are used so the frontend can make authenticated requests. This allows the backend to identify which user owns which chat sessions.

### Chat Service

The chat service is the central orchestration layer. It handles the complete flow of a user question:

1. Create or reuse a session ID.
2. Check if the message is a greeting.
3. Load recent conversation history.
4. Match campus location if applicable.
5. Fetch dynamic knowledge items if needed.
6. Retrieve verified knowledge base items.
7. Generate an AI answer.
8. Save the chat turn.
9. Return sources and location details.

This service also handles fallbacks if the AI provider fails.

### Retrieval Service

The retrieval service searches the DAVIET knowledge base. It normalizes the query, expands aliases, handles typos, removes stopwords, scores knowledge items, and returns the most relevant results.

This is one of the most important parts of the project because it controls what information is sent to the AI model.

### Location Service

The location service detects location-related questions and matches them with known campus destinations. It supports aliases and fuzzy matching, so it can understand terms like "audi", "tpo", "ug blok", and "lib".

When a location is found, the backend returns structured location data and the frontend displays it using a visual location card.

### AI Service

The AI service abstracts different AI providers. This means the rest of the backend does not need to know whether the response is generated by Ollama, Gemini, Claude, or another compatible provider.

The AI prompt includes verified context and instructions to behave like a DAVIET Smart Campus assistant. This makes the final response more useful and more controlled.

## Deployment Process

The deployment process involved setting up the backend, frontend, database, and environment variables.

### Backend Deployment

The backend was deployed on Render as a web service. The backend uses Uvicorn to run the FastAPI application. Environment variables were configured for MongoDB URI, database name, CORS origins, AI provider, AI model, API key, and log level.

Backend live URL:

https://daviet-ai-campus-backend.onrender.com

### Frontend Deployment

The frontend was deployed on Render as a static site. The React app is built using Vite, and the production build is served as the deployed frontend.

Frontend live URL:

https://ai-campus-147j.onrender.com/

### Frontend-Backend Connection

The deployed frontend was configured with the deployed backend URL. This allows the frontend application to send authentication, chat, streaming, session, and health requests to the live backend API.

### MongoDB Online Connection

MongoDB online database was configured so the deployed backend can store persistent application data. This includes user accounts, chat history, sessions, dynamic knowledge, and campus location records.

## Testing and Verification

Testing was done by checking the main user flows and backend behavior.

The following flows were verified:

- Opening the landing page.
- Opening the chat assistant.
- Sending a normal question.
- Receiving streamed AI response.
- Viewing source links.
- Asking location-related questions.
- Viewing location cards.
- Signing up as a user.
- Logging in with user credentials.
- Maintaining authenticated state.
- Saving chat sessions for logged-in users.
- Loading previous sessions.
- Deleting sessions.
- Running the backend health check.
- Connecting frontend to deployed backend.
- Connecting backend to online MongoDB.

Testing also included checking the fallback behavior. If a query is not related to DAVIET, the assistant guides the user back to campus-related questions. If verified information is missing, the assistant avoids guessing and suggests checking official sources.

## Challenges Faced

Several challenges were faced during the project development.

### 1. Connecting Frontend and Backend

One challenge was connecting the frontend and backend correctly in both local and deployed environments. The frontend needs the correct API base URL, and the backend needs correct CORS settings. This was handled using environment variables.

### 2. MongoDB Online Setup

Setting up MongoDB online required configuring the connection URI, database name, collections, and environment variables. It was important to ensure that both local and deployed backend could connect properly.

### 3. Reliable AI Answers

A normal AI chatbot can generate unsupported information. To solve this, retrieval was added before generation. The backend first searches verified DAVIET data and then sends that data to the AI model.

### 4. Handling Student Typing Style

Students may use short forms or type spelling mistakes. To handle this, aliases and fuzzy matching were added. This improved retrieval and location matching.

### 5. Streaming Response Handling

Streaming responses required extra handling on both frontend and backend. The backend sends SSE events, while the frontend reads and processes those events in real time.

### 6. Deployment Configuration

Deployment required separate configuration for frontend, backend, MongoDB, and AI provider. The environment variables had to be set correctly for the deployed services to work together.

## Learning Outcomes

This project helped in learning and applying multiple real-world development concepts.

Important learning outcomes include:

- Full-stack application development.
- React component-based frontend development.
- FastAPI backend development.
- REST API design.
- Server-Sent Events streaming.
- User authentication flow.
- Password hashing and token-based login.
- MongoDB online database setup.
- Database indexing.
- Environment variable management.
- Frontend-backend integration.
- AI provider integration.
- Retrieval-Augmented Generation.
- Deployment on Render.
- Debugging local and production configuration issues.


## User Flow

1. User opens the DAVIET Smart Campus Portal.
2. User can explore predefined topic cards or directly open the AI assistant.
3. User may continue as guest or sign in/sign up.
4. User asks a campus-related question.
5. Backend validates the message.
6. Backend loads recent conversation context.
7. Backend checks for greeting or location intent.
8. Backend retrieves relevant DAVIET knowledge.
9. Backend adds dynamic catalog information if required.
10. Backend sends verified context to the configured AI provider.
11. Frontend receives response as a stream.
12. Assistant answer is displayed with source links and optional location card.
13. If logged in, the conversation is saved privately to MongoDB.

## Knowledge Areas Covered

The assistant can answer questions related to:

- Institute background.
- AICTE approval and IKG-PTU affiliation.
- Academic programs.
- Engineering departments.
- Admissions.
- Eligibility and intake.
- Fee structure.
- Scholarships and university-related information.
- Library timings and services.
- Hostels and mess.
- Campus infrastructure.
- Training and placements.
- Contact details.
- Committees and student support.
- Grievance redressal.
- Working hours.
- Campus navigation.

## Key Backend Components

- `main.py`: FastAPI app creation, CORS setup, startup lifecycle, service initialization.
- `config.py`: Environment-based settings.
- `mongodb.py`: MongoDB connection, health check, and index creation.
- `auth.py`: Authentication API routes.
- `chat.py`: Chat, streaming, session, and deletion API routes.
- `auth_service.py`: Signup, login, password hashing, and token handling.
- `chat_service.py`: Main orchestration for retrieval, AI, history, location, and fallback logic.
- `retrieval_service.py`: Knowledge ranking, alias expansion, and typo-aware retrieval.
- `location_service.py`: Campus destination matching and location metadata.
- `web_retrieval_service.py`: Dynamic fee/PTU catalog and official-domain live fetch helper.
- `ai_service.py`: AI provider abstraction for Ollama, cloud, Gemini, and Claude-style providers.
- `chat_repository.py`: MongoDB chat persistence and privacy filtering.
- `knowledge_repository.py`: JSON knowledge loading.

## Key Frontend Components

- `App.jsx`: Main route switching between landing and chat.
- `LandingPage.jsx`: DAVIET portal homepage and quick topic cards.
- `ChatPage.jsx`: Main chat layout.
- `useChat.js`: Chat state, streaming, sessions, guest storage, and message sending.
- `api.js`: Frontend API client.
- `AuthContext.jsx`: Auth state and token management.
- `AuthModal.jsx`: Login/signup interface.
- `SessionSidebar.jsx`: Conversation history sidebar.
- `ChatWindow.jsx`: Chat message display area.
- `ChatInput.jsx`: User message input.
- `MessageBubble.jsx`: User and assistant message rendering.
- `SourceLinks.jsx`: Response source references.
- `LocationCard.jsx`: Campus navigation card with map support.
- `ErrorBanner.jsx`: Error display.
- `LoadingDots.jsx`: Loading indicator.

## Work Completed This Week

This week, the project reached a strong full-stack stage with the following completed features:

- Worked on complete frontend development using React and Vite.
- Worked on backend API development using FastAPI.
- Set up MongoDB online database for storing users, chat history, sessions, dynamic knowledge, and campus data.
- Configured environment variables for local and production usage.
- Developed a modern DAVIET landing page.
- Added quick topic cards for common student queries.
- Built a complete chat interface.
- Added streaming AI response support.
- Added guest mode with session storage.
- Added signup and login modal.
- Added authenticated user profile handling.
- Added private MongoDB-backed chat history.
- Added session sidebar with load and delete features.
- Implemented verified knowledge retrieval from JSON files.
- Added typo-aware alias matching.
- Added campus location detection.
- Added location cards with Google Maps support.
- Added dynamic fee and PTU knowledge catalog.
- Added provider-flexible AI service.
- Added fallback behavior for unknown, off-topic, and AI failure cases.
- Added health endpoint with degraded database status.
- Added environment-based configuration for local and production usage.
- Added Render deployment configuration.
- Deployed the backend API on Render.
- Deployed the frontend application on Render.
- Connected the deployed frontend with the deployed backend API.

## Suggested Screenshots to Include in PDF

To make the final PDF more complete and visually clear, the following screenshots can be added while converting this report into a designed PDF:

1. Landing page of DAVIET Smart Campus AI Assistant.
2. Topic cards section showing Academics, Fee Structure, Hostels, Admissions, and other options.
3. Login/signup modal.
4. Chat interface with a normal DAVIET query.
5. Streaming answer shown in the chat window.
6. Source links under an AI response.
7. Campus navigation response with location card and map.
8. Chat session sidebar showing previous conversations.
9. Render frontend deployment dashboard.
10. Render backend deployment dashboard.
11. MongoDB database collections screen.
12. Backend health endpoint response.

These screenshots will help demonstrate that the project is not only designed theoretically but is also implemented, connected to a database, and deployed online.

## Weekly Progress Explanation

During this project period, work was not limited to only one part of the application. Time was divided between frontend design, backend logic, database setup, AI integration, and deployment.

On the frontend side, major time was spent designing the landing page and chat interface. The aim was to make the application look professional and easy to use for students. The landing page was improved with DAVIET branding, topic cards, theme support, and user login state. The chat page was improved with streaming messages, session sidebar, copy response option, error handling, and location card support.

On the backend side, time was spent creating the FastAPI structure, authentication routes, chat routes, health route, retrieval service, location service, AI service, and MongoDB repositories. Backend development also included input validation, response models, fallback handling, and service-level organization.

For database work, MongoDB online setup was completed. Collections and indexes were planned according to project needs. The database supports persistent user accounts, chat sessions, chat turns, dynamic knowledge, locations, and audit logs.

For deployment, both frontend and backend were deployed on Render. The production environment variables were configured so the deployed frontend can communicate with the deployed backend and the deployed backend can connect with MongoDB and AI provider settings.

This makes the project complete as a deployed full-stack AI application rather than only a local prototype.

## Current Status

The application is functional and deployed as a full-stack smart campus assistant. The frontend can route users between landing page, guest chat, and authenticated chat. The backend can process questions, retrieve relevant DAVIET data, generate AI responses, stream answers, return sources, detect campus locations, and save user-specific chat history.

The system is available publicly through Render using the deployed frontend and backend URLs. The database is configured online using MongoDB, so deployed users can access persistent authentication and chat history features. The project is also suitable for local testing with proper environment variables for MongoDB, AI provider, CORS, and frontend API URL.

## Future Improvements

Planned or possible future improvements include:

- Add an admin dashboard to update knowledge base entries from the browser.
- Add role-based access for students, faculty, and administrators.
- Improve campus navigation with full route directions.
- Add voice input and voice output.
- Add multilingual support for Hindi and Punjabi.
- Add file upload for college notices or PDFs.
- Add automatic scheduled sync from official DAVIET and IKG-PTU sources.
- Add analytics for most asked student questions.
- Add feedback buttons for answer quality.
- Add stronger production secret management for auth token signing.
- Add automated tests for frontend components.
- Add richer PDF or report export from chat sessions.

## Conclusion

The DAVIET Smart Campus AI Assistant is now a feature-rich campus helpdesk application. It combines AI conversation, verified knowledge retrieval, user authentication, session history, location assistance, dynamic fee information, and a polished frontend experience. The project demonstrates how an educational institute can use AI to provide fast, reliable, and student-friendly information while still keeping official data as the foundation of every answer.
