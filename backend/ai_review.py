import os
import logging

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# All of these are called via the Groq SDK / Groq API only (no OpenAI API key).
# Llama IDs are enterprise-only now; free/developer production chat models are
# the gpt-oss IDs hosted by Groq. Override with GROQ_MODEL to pin one ID.
# https://console.groq.com/docs/models
_DEFAULT_GROQ_MODELS = (
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b",
    "groq/compound",
)


def _model_candidates() -> list[str]:
    preferred = (os.getenv("GROQ_MODEL") or "").strip()
    models: list[str] = []
    if preferred:
        models.append(preferred)
    for model in _DEFAULT_GROQ_MODELS:
        if model not in models:
            models.append(model)
    return models


_working_model: str | None = None


def _is_model_not_found(exc: Exception) -> bool:
    text = str(exc).lower()
    return "model_not_found" in text or "does not exist" in text or "do not have access" in text


def _groq_chat(system: str, user: str, max_tokens: int = 1024) -> str | None:
    """Call Groq chat completion. Returns content string or None on failure."""
    global _working_model
    if not GROQ_API_KEY:
        return None
    try:
        from groq import Groq
    except Exception as e:
        logger.warning("Groq SDK import failed: %s", e)
        return None

    client = Groq(api_key=GROQ_API_KEY)
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    candidates = _model_candidates()
    if _working_model and _working_model in candidates:
        candidates = [_working_model] + [m for m in candidates if m != _working_model]

    last_error: Exception | None = None
    for model in candidates:
        try:
            resp = client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.4,
            )
            _working_model = model
            return resp.choices[0].message.content.strip()
        except Exception as e:
            last_error = e
            if _is_model_not_found(e):
                logger.warning("Groq model unavailable (%s): %s", model, e)
                continue
            logger.warning("Groq API error (%s): %s", model, e)
            return None

    if last_error:
        logger.warning("Groq API error: all candidate models failed: %s", last_error)
    return None


def architecture_review(code_sample: str, repo_name: str, language: str) -> dict:
    """Return AI architecture review with strengths, concerns, and suggestions."""
    if not code_sample:
        return {"error": "No code sample found for AI review."}

    system = (
        "You are a senior software architect. Analyze the code provided and give a concise, "
        "repo-specific architecture review. Return EXACTLY this format:\n\n"
        "STRENGTHS:\n- bullet 1\n- bullet 2\n\n"
        "CONCERNS:\n- bullet 1\n- bullet 2\n\n"
        "SUGGESTIONS:\n- bullet 1\n- bullet 2\n\n"
        "Keep each section to 2-4 bullets. Be specific to this code, not generic."
    )
    user = (
        f"Repository: {repo_name}\nPrimary language: {language}\n\n"
        f"Code sample:\n```\n{code_sample[:6000]}\n```"
    )
    raw = _groq_chat(system, user, max_tokens=800)
    if not raw:
        return {"error": "GROQ_API_KEY missing or API call failed."}

    sections = {"strengths": [], "concerns": [], "suggestions": []}
    current = None
    for line in raw.splitlines():
        lower = line.strip().lower()
        if lower.startswith("strength"):
            current = "strengths"
        elif lower.startswith("concern"):
            current = "concerns"
        elif lower.startswith("suggestion"):
            current = "suggestions"
        elif line.strip().startswith("-") and current:
            sections[current].append(line.strip().lstrip("- ").strip())
    return sections


def generate_recommendation(
    repo_name: str, language: str, score: float, complexity: float, total_files: int
) -> str:
    """Return a concise, repo-specific AI recommendation paragraph."""
    system = (
        "You are a senior software engineer. Given repository metrics, provide a single concise "
        "paragraph (3-5 sentences) with specific, actionable advice to improve this codebase. "
        "Reference the actual metrics. Do not use bullet points."
    )
    user = (
        f"Repository: {repo_name}\n"
        f"Language: {language}\n"
        f"Health score: {score}/100\n"
        f"Avg cyclomatic complexity: {complexity}\n"
        f"Total analyzed files: {total_files}\n"
    )
    return _groq_chat(system, user, max_tokens=300)


def summarize_repo(readme_text: str, repo_name: str) -> str | None:
    """Generate a 2-3 sentence summary of the repository from its README."""
    if not readme_text or len(readme_text.strip()) < 30:
        return None
    system = (
        "You are a technical writer. Given a repository README, produce a 2-3 sentence summary "
        "that explains WHAT the project does and WHO it is for. Be precise and concise. "
        "Do not start with 'This repository...' — use the project name instead."
    )
    user = f"Repository: {repo_name}\n\nREADME:\n{readme_text[:4000]}"
    return _groq_chat(system, user, max_tokens=200)
