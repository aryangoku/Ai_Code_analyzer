from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Load .env from the backend directory so GITHUB_CLIENT_ID etc. are available
load_dotenv(Path(__file__).resolve().parent / ".env")

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analyzer import analyze_repo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CodePulse", version="0.4.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class RepoRequest(BaseModel):
    repo_url: str


def _normalize_github_url(url: str) -> str:
    url = url.strip()
    if not url:
        raise ValueError("Repository URL is required.")
    if "github.com" not in url:
        raise ValueError("Please provide a valid GitHub repository URL.")
    if not url.startswith("http"):
        url = "https://github.com/" + url.lstrip("/")
    return url


@app.get("/")
def root():
    return {"app": "CodePulse", "docs": "/docs", "health": "/health"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/analyze")
def analyze(data: RepoRequest):
    try:
        repo_url = _normalize_github_url(data.repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    try:
        return analyze_repo(repo_url)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")