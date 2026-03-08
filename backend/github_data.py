import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


def _owner_repo(repo_url):
    repo_path = (
        repo_url.replace("https://github.com/", "")
        .replace("http://github.com/", "")
        .strip("/")
    )
    parts = [p for p in repo_path.split("/") if p]
    return (parts[0], parts[1]) if len(parts) >= 2 else (None, None)


def _headers():
    h = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


def get_repo_data(repo_url):
    try:
        owner, repo = _owner_repo(repo_url)
        if not owner or not repo:
            return {"stars": 0, "forks": 0, "language": "Unknown", "issues": 0}
        api = f"https://api.github.com/repos/{owner}/{repo}"
        r = requests.get(api, headers=_headers(), timeout=10)
        data = r.json()
        if "message" in data or r.status_code != 200:
            return {"stars": 0, "forks": 0, "language": "Unknown", "issues": 0}
        return {
            "stars": data.get("stargazers_count", 0),
            "forks": data.get("forks_count", 0),
            "language": data.get("language", "Unknown"),
            "issues": data.get("open_issues_count", 0),
        }
    except Exception:
        return {"stars": 0, "forks": 0, "language": "Unknown", "issues": 0}


def get_commit_activity(repo_url):
    """Last 52 weeks of commit counts per day (Sun–Sat). Returns list of {week, total, days}."""
    try:
        owner, repo = _owner_repo(repo_url)
        if not owner or not repo:
            return []
        url = f"https://api.github.com/repos/{owner}/{repo}/stats/commit_activity"
        r = requests.get(url, headers=_headers(), timeout=15)
        if r.status_code == 202:
            return []  # Stats being computed
        if r.status_code != 200:
            return []
        data = r.json()
        return data if isinstance(data, list) else []
    except Exception:
        return []


def get_contributors(repo_url, per_page=30):
    """Top contributors with login, avatar_url, contributions."""
    try:
        owner, repo = _owner_repo(repo_url)
        if not owner or not repo:
            return []
        url = f"https://api.github.com/repos/{owner}/{repo}/contributors?per_page={per_page}"
        r = requests.get(url, headers=_headers(), timeout=10)
        if r.status_code != 200:
            return []
        data = r.json()
        return [
            {
                "login": c.get("login"),
                "avatar_url": c.get("avatar_url"),
                "contributions": c.get("contributions", 0),
            }
            for c in (data if isinstance(data, list) else [])
        ]
    except Exception:
        return []