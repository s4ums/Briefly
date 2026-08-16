# Briefly

> Transform conversations into actionable insights.

An AI Meeting Intelligence Platform that transcribes meeting recordings, extracts action items, decisions, and deadlines, and lets you chat with your meeting history using RAG.

## Stack

- **Frontend:** React, TypeScript, Vite, TailwindCSS — deployed to Vercel
- **Backend:** FastAPI, SQLAlchemy (async), Alembic — deployed to Render (free tier)
- **Database:** Neon PostgreSQL with pgvector
- **Auth & Storage:** Supabase
- **AI:** Groq (Whisper STT + LLM), sentence-transformers (embeddings)

## Local Development

### Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

Visit `http://localhost:5173` — it should show "Backend status: connected".

## Project Status

Built incrementally, one milestone at a time. See `docs/` for the full architectural review, SRS, and milestone roadmap (Milestones 1–12 core, Milestone 13 optional speaker diarization).
