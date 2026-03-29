# MVP Development Mandates: Voice Command Recognition System

## Core Principles
- **Design First (Single Source of Truth)**: ALL architectural decisions, database schemas, and workflows MUST be documented in the `.memory-bank/` directory BEFORE any implementation code is written. 
- **Memory Bank Compliance**: The code must strictly follow the specifications defined in `.memory-bank/`. If a design flaw is found during coding, UPDATE the `.memory-bank/` documentation first, and only then change the code.
- **Strict Prompt & AI Logging**: The Olympiad task strictly requires logging AI usage. You MUST maintain a `.memory-bank/ai_prompts_log.md` file. Every major generation, architecture decision, or code block creation must be logged there with the task solved and the prompt used.
- **Mermaid for Visuals**: All diagrams (UML Use Case, DFD, ERD, Flowcharts) must be written strictly using Markdown + Mermaid.js syntax inside `.memory-bank` documents.
- **Ask When Unsure**: If a task requirement is ambiguous (e.g., UI layout details, audio conversion trade-offs), ASK the user immediately. Do not guess on critical MVP components.

## Technology Stack Standards
- **Backend & Frontend**: Use **Flask** with **Jinja2** templates. NO heavy frontend frameworks (No React, Next.js, or Vue).
- **UI/Styling**: Use plain HTML5, Vanilla JavaScript, and Bootstrap 5 (via CDN). 
- **Audio Capture**: Use Vanilla JS `MediaRecorder API` on the client side to capture microphone audio and send it via `fetch` to the backend.
- **Database**: Use **SQLite** via `Flask-SQLAlchemy`.
- **Auth**: Use `Flask-Login` for role-based access control (Admin, Operator).
- **Speech-to-Text**: Use the `vosk` Python package with a lightweight Russian model. Handle necessary audio conversions (e.g., using `pydub` or `wave` to convert WebM/Ogg from the browser to WAV Mono 16kHz for VOSK) on the backend.

## Development Pipeline (Strict Order)
You must execute the project in the following phases. Do not jump to the next phase without completing the current one.

### Phase 1: Architecture & Design (The `.memory-bank` phase)
1. Initialize `.memory-bank/` directory.
2. Create `database_schema.md` (Infological and Datalogical models, complete with Mermaid ERD diagrams, data types, and keys).
3. Create `system_architecture.md` (Mermaid DFD, components interaction, tech stack description).
4. Create `use_cases.md` (Mermaid UML Use Case diagrams for Operator and Admin scenarios as per MVP requirements).
5. Create `api_endpoints.md` (Description of Flask routes and expected payloads).

### Phase 2: Implementation (The Code phase)
1. Setup Flask boilerplate and SQLite models strictly matching `database_schema.md`.
2. Implement Auth (Login, Roles).
3. Implement Frontend (Jinja templates, Bootstrap UI, Vanilla JS audio recording).
4. Implement Audio Processing & VOSK Integration (handling 8-digit and alphanumeric IDs, and specific commands like "Зарегистрировать", "Начать обработку", etc.).
5. Ensure atomic commits/saves and keep `.memory-bank` updated if codebase diverges.

### Phase 3: Deliverables & Finalization (The Review phase)
1. Generate `README.md` with step-by-step deployment instructions for the examining expert.
2. Generate `USER_MANUAL.md` with a text script/test-cases for the demonstration video.
3. Compile all technical documentation from `.memory-bank` into a final format suitable for the 35-point design review criteria.

## Specific Domain Rules
- **Commands**: The system must accurately parse specific command phrases: "Зарегистрировать", "Начать обработку", "Отменить обработку", "Отменить регистрацию", "Завершить обработку".
- **Identifiers**: The system must extract 8-digit numeric sequences and alphanumeric combinations.
- **History**: Every audio recording, recognized text, timestamps, user ID, and operator confirmations MUST be saved in the SQLite database and displayed in the UI.
