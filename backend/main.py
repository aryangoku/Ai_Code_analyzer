from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from github_clone import clone_repo
from analyzer import analyze_code
from github_info import get_repo_info

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/analyze")
def analyze(repo_url: str):

    repo_path = clone_repo(repo_url)

    metrics = analyze_code(repo_path)

    repo_info = get_repo_info(repo_url)

    return {
        "status": "success",
        "metrics": metrics,
        "repo": repo_info
    }