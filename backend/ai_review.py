import os
import logging

logger = logging.getLogger(__name__)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"


def _groq_chat(system: str, user: str, max_tokens: int = 1024) -> str | None:
    """Call Groq chat completion. Returns content string or None on failure."""
    if not GROQ_API_KEY:
        return None
    try:
        from groq import Groq

        client = Groq(api_key=GROQ_API_KEY)
        resp = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            max_tokens=max_tokens,
            temperature=0.4,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        logger.warning("Groq API error: %s", e)
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
