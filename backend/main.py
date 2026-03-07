from fastapi import FastAPI
from pydantic import BaseModel
from analyzer import analyze_repo
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class RepoRequest(BaseModel):
    repo_url: str


@app.post("/analyze")
def analyze(data: RepoRequest):
    return analyze_repo(data.repo_url)