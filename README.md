# CodePulse

AI-powered code analyzer for GitHub repositories. Paste a repo URL to get health scores, commit heatmaps, contributor stats, dependency graphs, and AI architecture review.

## Stack

- **Backend:** FastAPI, Python (Radon, Bandit, GitPython, optional OpenAI, JWT auth)
- **Frontend:** React, Tailwind CSS, Recharts, Framer Motion

## Quick start

### Backend

```bash
cd backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
# Optional: copy .env.example to .env
uvicorn main:app --reload
```

API: **http://127.0.0.1:8000** (docs at http://127.0.0.1:8000/docs).  
If you see "invalid response", make sure you include the port: **:8000** for the API, **:3000** for the app.

### Frontend

```bash
cd frontend
npm install
npm start
```

App: `http://localhost:3000`.

## Environment (optional)

| Variable | Where | Purpose |
|----------|--------|---------|
| `OPENAI_API_KEY` | backend | Enables AI architecture review panel |
| `GITHUB_TOKEN` | backend | Higher GitHub API rate limits (commit activity, contributors) |
| `GITHUB_CLIENT_ID` / `GITHUB_CLIENT_SECRET` | backend | GitHub OAuth (Login with GitHub) |
| `FRONTEND_URL` | backend | Where to redirect after OAuth (default: `http://localhost:3000`) |
| `API_URL` | backend | Public backend URL for OAuth callback (default: `http://127.0.0.1:8000`) |
| `JWT_SECRET` | backend | Secret for signing auth tokens |
| `REACT_APP_API_URL` | frontend | Backend URL (default: `http://127.0.0.1:8000`) |

## Features

- **GitHub OAuth login** – Sign in with GitHub (optional; analysis works without login)
- **Commit heatmap** – Last 52 weeks of commit activity (real GitHub stats)
- **Contributor graph** – Top contributors with avatars and commit counts
- **Engineering health score** – Overall, complexity, risk, security, and activity scores
- **Dependency graph** – Python import graph (nodes and edges)
- **AI architecture review panel** – Repo-specific OpenAI review when `OPENAI_API_KEY` is set (unique per repository)
- **AI recommendation** – Repo-specific suggestions (with or without OpenAI)
- **Health score** – From cyclomatic complexity
- **Risk score** – From complexity, issues, and large files
- **Security report** – Bandit output (expandable)
- **Repo stats** – Stars, forks, language, issues from GitHub

## Project structure

```
Ai_Code_analyzer/
├── backend/          # FastAPI, analyzer, auth, GitHub, AI review, dependency graph
├── frontend/         # React app (CRA, Tailwind)
└── README.md
```
