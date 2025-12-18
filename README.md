# Agentic Loan Orchestrator

This is a hackathon-ready prototype for an Agentic Loan Orchestrator using FastAPI, LangGraph, and React.

## Folder Structure
- `backend/`: FastAPI application, Agents, Mock Data.
- `frontend/`: React + Vite application.

## Setup Instructions

### Backend
1. Navigate to directory:
   ```bash
   cd backend
   ```
2. Create virtual environment and install dependencies:
   ```bash
   pip install -r ../requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn backend.main:app --reload
   ```
   Server will start at `http://127.0.0.1:8000`.

### Frontend
1. Navigate to directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   npm install -D tailwindcss postcss autoprefixer
   npx tailwindcss init -p
   npm install mermaid
   ```
3. Run the dev server:
   ```bash
   npm run dev
   ```
   App will start at `http://localhost:5173`.

## Architecture
- **Master Agent**: Orchestrates the flow.
- **Sales Agent**: Handles conversation.
- **Verification Agent**: Checks `customers.json`.
- **Underwriting Agent**: Runs `underwriting_rules.py`.
- **Sanction Agent**: Generates PDFs.
