# Claude Instructions for Pregnancy Safety Radar (BumpRadar)

## Project Context
This is the Pregnancy Safety Radar (BumpRadar) application - a tool to help pregnant users check product safety.

## Workflow Preferences

### End Session Protocol
When the user says "end session":
1. Update CLAUDE.md with any relevant project patterns, decisions, or instructions learned during the session
2. Update memory.md with important learnings and lessons
3. Save any recurring patterns or conventions discovered during the session
4. Document any architectural decisions or important context for future sessions

## Project Structure
- `backend/` - Python backend with FastAPI
  - `app/agents/` - Agent modules: orchestrator, safety_classifier, ocr_agent, product_scanner, qa_agent, research_agent
  - `app/api/v1/endpoints/` - API endpoints: scan, admin
  - `app/core/` - Core functionality including rate_limit.py
- `frontend/` - Frontend application with server.py
- `skills/` - Custom Claude skills (frontend-design)
- `.claude-plugin/` - Claude plugin configuration

## Recent Updates (as of 2026-03-19)
- Multi-agent system implemented: OCR, product scanner, QA, and research agents
- Enhanced orchestrator for coordinating agents
- Rate limiting system added
- Admin API endpoints created
- Frontend significantly redesigned with Python server
- Image upload compression added to prevent 413 errors
- Mobile access configured via local network (HTTP server on port 3000)
- OpenAI Vision API integrated for photo OCR

## Running the App

### Dependencies
Core dependencies needed (minimal for development):
```bash
pip install fastapi uvicorn sqlalchemy pydantic pydantic-settings openai python-dotenv pillow python-multipart
```

### Configuration
- OpenAI API key required for photo scanning mode
- Set in `backend/.env`: `OPENAI_API_KEY=sk-...`
- Text and Barcode modes work without API key

### Starting Servers
**Backend (Port 8000):**
```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload --timeout-keep-alive 30
```

**Frontend (Port 3000):**
```bash
cd frontend
python simple_server.py
```

**Or use startup scripts:**
- `start_app.bat` (Windows)
- `start_app.sh` (Bash)

### Mobile Access
- Frontend: `http://<local-ip>:3000`
- Backend API: `http://<local-ip>:8000`
- Devices must be on same WiFi network

## Technical Decisions

### Image Upload Handling
- **Problem:** Large base64 images causing 413 errors
- **Solution:** Client-side compression in `frontend/index.html`
  - Resize to max 1200px width/height
  - Compress to JPEG at 70% quality
  - Reduces payload by 80-90%

### OCR Agent
- Uses OpenAI GPT-4o-mini Vision API
- Timeout set to 30 seconds
- Returns helpful error if API key not configured
- Location: `backend/app/agents/ocr_agent.py`

### Frontend Server
- Simple HTTP server (no SSL) for easier mobile testing
- CORS enabled for cross-origin requests
- Auto-detects API endpoint based on hostname
- Location: `frontend/simple_server.py`
