import os
import time
import jwt
import requests
from urllib.parse import quote
from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse

router = APIRouter(prefix="/auth", tags=["auth"])

JWT_SECRET = os.getenv("JWT_SECRET", "dev-insight-secret-change-in-production")
JWT_ALGORITHM = "HS256"
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")


def _get_redirect_uri() -> str:
    """Callback URL for GitHub OAuth. Must match exactly what you set in GitHub OAuth App."""
    explicit = os.getenv("GITHUB_REDIRECT_URI", "").strip()
    if explicit:
        return explicit.rstrip("/")
    base = os.getenv("API_URL", "http://localhost:8000").strip().rstrip("/")
    return f"{base}/auth/callback"


def _encode_token(login: str, github_id: str, avatar_url: str | None = None, name: str | None = None) -> str:
    payload = {
        "sub": str(github_id),
        "login": login,
        "avatar_url": avatar_url,
        "name": name,
        "exp": int(time.time()) + 7 * 24 * 3600,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def get_current_user(authorization: str | None = None) -> dict | None:
    if not authorization or not authorization.startswith("Bearer "):
        return None
    token = authorization.replace("Bearer ", "").strip()
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except Exception:
        return None


@router.get("/login")
def login():
    if not GITHUB_CLIENT_ID:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured (missing GITHUB_CLIENT_ID)")
    redirect_uri = _get_redirect_uri()
    # GitHub requires redirect_uri to be exactly what's registered; encode for query string
    encoded_uri = quote(redirect_uri, safe="")
    url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={encoded_uri}"
        "&scope=read:user"
    )
    return RedirectResponse(url=url)


@router.get("/callback")
def callback(code: str | None = None, error: str | None = None):
    if error:
        return RedirectResponse(url=f"{FRONTEND_URL}?auth_error={error}")
    if not code:
        return RedirectResponse(url=f"{FRONTEND_URL}?auth_error=no_code")
    if not GITHUB_CLIENT_SECRET:
        raise HTTPException(status_code=503, detail="GitHub OAuth not configured")

    redirect_uri = _get_redirect_uri()
    r = requests.post(
        "https://github.com/login/oauth/access_token",
        data={
            "client_id": GITHUB_CLIENT_ID,
            "client_secret": GITHUB_CLIENT_SECRET,
            "code": code,
            "redirect_uri": redirect_uri,
        },
        headers={"Accept": "application/json"},
        timeout=10,
    )
    data = r.json()
    if "error" in data:
        return RedirectResponse(url=f"{FRONTEND_URL}?auth_error={data.get('error', 'unknown')}")
    access_token = data.get("access_token")
    if not access_token:
        return RedirectResponse(url=f"{FRONTEND_URL}?auth_error=no_token")

    user_r = requests.get(
        "https://api.github.com/user",
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=10,
    )
    user = user_r.json()
    login = user.get("login", "user")
    github_id = user.get("id", "")
    avatar_url = user.get("avatar_url")
    name = user.get("name")

    token = _encode_token(login, str(github_id), avatar_url, name)
    return RedirectResponse(url=f"{FRONTEND_URL}?token={token}")


@router.get("/callback-url")
def callback_url():
    """Return the redirect_uri this app uses. Add this exact URL in GitHub OAuth App → Authorization callback URL."""
    return {"redirect_uri": _get_redirect_uri()}


@router.get("/me")
def me(authorization: str | None = None):
    user = get_current_user(authorization)
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {
        "login": user.get("login"),
        "avatar_url": user.get("avatar_url"),
        "name": user.get("name"),
        "id": user.get("sub"),
    }
